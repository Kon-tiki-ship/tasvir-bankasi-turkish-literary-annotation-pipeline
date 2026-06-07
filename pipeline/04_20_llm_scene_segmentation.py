from __future__ import annotations

from pathlib import Path
import json
import os
import re
import time
from typing import Any, Dict

from google import genai
from google.genai import types

# =========================================================
# CONFIG
# =========================================================

INPUT_DIR = Path("data/stage_4_4")
OUTPUT_DIR = Path("data/stage_4_8")
OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

PRIMARY_LLM_MODEL = os.getenv("LLM_SCENE_PRIMARY_MODEL", "provider/default-scene-segmentation-model")
FALLBACK_LLM_MODEL = os.getenv("LLM_SCENE_FALLBACK_MODEL", "provider/default-scene-refinement-model")

LONG_TOKEN_THRESHOLD = 400
HUGE_TOKEN_THRESHOLD = 800

MAX_OUT_NORMAL_FLASH = 600
MAX_OUT_LONG_FLASH   = 300
MAX_OUT_REFINEMENT          = 1200

MAX_RETRIES = 1
BACKOFF_BASE_SEC = 1.25

MAX_CONTEXT_CHARS = 180


def get_required_env(*names: str) -> str:
    for name in names:
        value = os.getenv(name)
        if value:
            return value
    joined = " or ".join(names)
    raise RuntimeError(f"{joined} must be set in the environment before running this stage.")


client = genai.Client(api_key=get_required_env("LLM_API_KEY"))

# =========================================================
# SYSTEM PROMPTS
# =========================================================

SYSTEM_PROMPT_FULL = """
You are a narrative editor.

Preserve narrative coherence and segment text into scenes.
Do NOT split by length.

Split only if there is a clear change in:
- location
- time
- narrator
- event focus
- interaction mode

Dialogue continuation alone is NOT a split reason.

If the text is a micro-block:
- brief_summary MUST be a single short sentence (max 15 words)

This text may include themes of sadness or death.
Analyze structurally without judgment.

Return ONLY valid JSON.

FORMAT:
{
  "scenes": [
    {
      "scene_index": 1,
      "scene_type": "single_scene" | "new_scene",
      "brief_summary": "summary",
      "split_reason": "reason"
    }
  ]
}
""".strip()

SYSTEM_PROMPT_STRUCTURAL = """
You are a narrative structure analyzer.

Rules:
- Identify scene boundaries only
- Do NOT write summaries
- Do NOT repeat or paraphrase the text
- Keep split_reason extremely short (max 5–8 words)

This text may include themes of sadness or death.
Analyze structurally without judgment.

Return ONLY valid JSON.

FORMAT:
{
  "scenes": [
    {
      "scene_index": 1,
      "scene_type": "single_scene" | "new_scene",
      "split_reason": "short reason"
    }
  ]
}
""".strip()

# =========================================================
# HELPERS
# =========================================================

_JSON_RX = re.compile(r"\{.*\}", re.DOTALL)

def extract_json(raw: str) -> Dict[str, Any]:
    m = _JSON_RX.search(raw)
    if not m:
        raise ValueError("JSON object not found")
    return json.loads(m.group())

def safe_text(resp: Any) -> str:
    if getattr(resp, "text", None):
        return resp.text
    parts = []
    for c in getattr(resp, "candidates", []) or []:
        for p in getattr(getattr(c, "content", None), "parts", []) or []:
            if getattr(p, "text", None):
                parts.append(p.text)
    return "\n".join(parts)

def build_prompt(prev_context: str, curr_text: str) -> str:
    return f"""
Previous context (optional signal only):
<<<
{prev_context}
>>>

Current block:
<<<
{curr_text}
>>>

Task:
Analyze and return scene segmentation strictly in JSON.
""".strip()

# =========================================================
# MODEL CALL
# =========================================================

def call_llm(prompt: str, *, model: str, system_prompt: str, max_out: int) -> Dict[str, Any]:
    resp = client.models.generate_content(
        model=model,
        contents=prompt,
        config=types.GenerateContentConfig(
            system_instruction=system_prompt,
            temperature=0.1,
            max_output_tokens=max_out,
            response_mime_type="application/json",
        ),
    )
    raw = safe_text(resp)
    if not raw:
        raise ValueError("Empty model response")
    return extract_json(raw)

def segment_scenes(
    prompt: str,
    token_count: int,
    uncertain: bool,
    is_micro_block: bool,
) -> Dict[str, Any]:

    is_long = token_count >= LONG_TOKEN_THRESHOLD
    is_huge = token_count >= HUGE_TOKEN_THRESHOLD

    if is_long or uncertain:
        system_prompt = SYSTEM_PROMPT_STRUCTURAL
        max_out = MAX_OUT_LONG_FLASH
    else:
        system_prompt = SYSTEM_PROMPT_FULL
        max_out = MAX_OUT_NORMAL_FLASH

    # Mikro-bloklarda fallback modeli kapalı
    if is_micro_block:
        attempts = [(PRIMARY_LLM_MODEL, max_out)]
    else:
        attempts = [
            (PRIMARY_LLM_MODEL, max_out),
            (FALLBACK_LLM_MODEL, MAX_OUT_REFINEMENT),
        ]

    last_err = None

    for model, out_lim in attempts:
        for r in range(MAX_RETRIES + 1):
            try:
                return call_llm(
                    prompt,
                    model=model,
                    system_prompt=system_prompt,
                    max_out=out_lim,
                )
            except Exception as e:
                last_err = e
                time.sleep(BACKOFF_BASE_SEC * (2 ** r))

    # Mikro-blokta retry sonrası direkt yapısal fallback
    if is_micro_block:
        return {
            "scenes": [
                {
                    "scene_index": 1,
                    "scene_type": "single_scene",
                    "split_reason": "structural_fallback"
                }
            ]
        }

    return {
        "scenes": [
            {
                "scene_index": 1,
                "scene_type": "single_scene",
                "split_reason": "model_error"
            }
        ],
        "_error": str(last_err),
    }

# =========================================================
# PIPELINE
# =========================================================

for input_path in INPUT_DIR.glob("*.jsonl"):
    print(f"▶ Processing: {input_path.name}")
    output_path = OUTPUT_DIR / input_path.name.replace(".jsonl", "_stage_4_8.jsonl")

    paragraphs = []
    with input_path.open("r", encoding="utf-8") as f:
        for line in f:
            if line.strip():
                paragraphs.append(json.loads(line))

    for i, p in enumerate(paragraphs):
        flag = p.get("coherence_flag")
        token_count = int(p.get("token_count") or 0)
        is_micro_block = bool(p.get("is_micro_block"))

        if flag == "false_paragraph_boundary":
            p["scene_segments"] = None
            p["scene_source"] = "skipped_false_boundary"
            continue

        prev_context = ""
        if i > 0:
            prev_text = paragraphs[i - 1].get("text") or ""
            prev_context = prev_text[-MAX_CONTEXT_CHARS:]

        prompt = build_prompt(prev_context, p.get("text", ""))
        uncertain = flag == "uncertain"

        scenes = segment_scenes(
            prompt,
            token_count,
            uncertain,
            is_micro_block,
        )

        p["scene_segments"] = scenes

        if "_error" in scenes:
            p["scene_source"] = "forced_single_scene"
            p["scene_error"] = scenes.pop("_error")
        else:
            p["scene_source"] = "llm_dynamic"

    # =========================================================
    # MINI ZINCIR KURALI (ETIKET ONLY)
    # =========================================================

    for i in range(1, len(paragraphs) - 1):
        curr = paragraphs[i]
        prev = paragraphs[i - 1]
        nxt  = paragraphs[i + 1]

        if not curr.get("is_micro_block"):
            continue

        pid = curr.get("parent_paragraph_id")
        if not pid:
            continue

        if prev.get("parent_paragraph_id") != pid:
            continue
        if nxt.get("parent_paragraph_id") != pid:
            continue

        if (
            curr.get("scene_source") == "llm_dynamic"
            and prev.get("scene_source") == "llm_dynamic"
            and nxt.get("scene_source") == "llm_dynamic"
        ):
            try:
                curr_scene = curr["scene_segments"]["scenes"][0]["scene_type"]
                prev_scene = prev["scene_segments"]["scenes"][0]["scene_type"]
                next_scene = nxt["scene_segments"]["scenes"][0]["scene_type"]
            except Exception:
                continue

            if curr_scene == prev_scene == next_scene == "single_scene":
                curr["scene_chain"] = True

    with output_path.open("w", encoding="utf-8") as out:
        for p in paragraphs:
            out.write(json.dumps(p, ensure_ascii=False) + "\n")

    print(f"✔ Written: {output_path.name}")

print("✅ Stage 4_8 – optimized micro-block scene segmentation completed.")
