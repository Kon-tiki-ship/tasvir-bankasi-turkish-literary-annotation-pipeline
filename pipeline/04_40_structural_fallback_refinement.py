# =========================================================
# Stage 5 – Structural Fallback Refinement + PHYSICAL SPLIT
# (LLM refinement model)
#
# Purpose:
# - Refine ONLY high-priority structural_fallback blocks
# - IDENTIFY AND APPLY scene splits in this stage
# - Stage 5 PRODUCES final split scenes (NO Stage 6)
#
# Input : data/stage_4_9/*.jsonl
# Output: data/stage_5/*.jsonl
# =========================================================

from __future__ import annotations

from pathlib import Path
import json
import os
import re
import time
from typing import Any, Dict, List

from google import genai
from google.genai import types

# =========================================================
# CONFIG
# =========================================================

INPUT_DIR  = Path("data/stage_4_9")
OUTPUT_DIR = Path("data/stage_5")
OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

REFINEMENT_MODEL = os.getenv("LLM_REFINEMENT_MODEL", "provider/default-scene-refinement-model")

MAX_OUT_REFINEMENT = 800
MAX_RETRIES = 1
BACKOFF_BASE_SEC = 1.5

MAX_CONTEXT_CHARS = 200


def get_required_env(*names: str) -> str:
    for name in names:
        value = os.getenv(name)
        if value:
            return value
    joined = " or ".join(names)
    raise RuntimeError(f"{joined} must be set in the environment before running this stage.")


client = genai.Client(api_key=get_required_env("LLM_API_KEY"))

# =========================================================
# SYSTEM PROMPT
# =========================================================

SYSTEM_PROMPT_REFINEMENT = """
You are an expert narrative structure editor.

Task:
The given text block was kept as a single scene because it was too complex
for a smaller model. It likely contains MULTIPLE distinct scenes merged together.

Your job:
- Identify CLEAR scene boundaries based on:
  • Time jumps
  • Location changes
  • Major event or action shifts

Rules:
- Do NOT summarize the text
- Do NOT rewrite or paraphrase
- Do NOT invent content
- Do NOT split unless there is a strong structural signal

Output:
Return ONLY valid JSON.

FORMAT:
{
  "split_points": [
    "exact last 5–10 words of scene 1",
    "exact last 5–10 words of scene 2"
  ]
}

If no split is needed, return:
{ "split_points": [] }

IMPORTANT:
Split points MUST be exact substrings copied verbatim from the input text.
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
Previous context (signal only):
<<<
{prev_context}
>>>

Text to analyze:
<<<
{curr_text}
>>>

Return scene split points strictly in JSON.
""".strip()

def split_text_by_points(text: str, split_points: List[str]) -> List[str]:
    segments = []
    remaining = text

    for sp in split_points:
        idx = remaining.find(sp)
        if idx == -1:
            continue
        cut = idx + len(sp)
        segments.append(remaining[:cut].strip())
        remaining = remaining[cut:].strip()

    if remaining:
        segments.append(remaining)

    return segments

# =========================================================
# MODEL CALL
# =========================================================

def call_llm_refinement(prompt: str) -> Dict[str, Any]:
    resp = client.models.generate_content(
        model=REFINEMENT_MODEL,
        contents=prompt,
        config=types.GenerateContentConfig(
            system_instruction=SYSTEM_PROMPT_REFINEMENT,
            temperature=0.1,
            max_output_tokens=MAX_OUT_REFINEMENT,
            response_mime_type="application/json",
        ),
    )

    raw = safe_text(resp)
    if not raw:
        raise ValueError("Empty model response")

    return extract_json(raw)

# =========================================================
# PIPELINE
# =========================================================

for input_path in INPUT_DIR.glob("*.jsonl"):
    print(f"▶ Processing: {input_path.name}")

    output_path = OUTPUT_DIR / input_path.name.replace("4_9", "5")

    paragraphs: List[Dict[str, Any]] = []
    with input_path.open("r", encoding="utf-8") as f:
        for line in f:
            if line.strip():
                paragraphs.append(json.loads(line))

    output_rows: List[Dict[str, Any]] = []

    for i, p in enumerate(paragraphs):
        review = p.get("fallback_review", {})

        if not review.get("eligible_for_llm_refinement"):
            output_rows.append(p)
            continue

        prev_context = ""
        if i > 0:
            prev_text = paragraphs[i - 1].get("text") or ""
            prev_context = prev_text[-MAX_CONTEXT_CHARS:]

        prompt = build_prompt(prev_context, p.get("text", ""))

        last_err = None
        split_points: List[str] = []

        for r in range(MAX_RETRIES + 1):
            try:
                result = call_llm_refinement(prompt)
                split_points = result.get("split_points", [])
                break
            except Exception as e:
                last_err = e
                time.sleep(BACKOFF_BASE_SEC * (2 ** r))

        if not split_points:
            p["scene_source"] = "llm_refinement_single_scene"
            output_rows.append(p)
            continue

        segments = split_text_by_points(p["text"], split_points)

        for idx, seg in enumerate(segments, start=1):
            new_p = p.copy()
            new_p["text"] = seg
            new_p["scene_index"] = idx
            new_p["scene_source"] = "llm_refinement_split_scene"
            new_p["split_origin"] = "stage_5_pro"
            output_rows.append(new_p)

        time.sleep(1.5)

    with output_path.open("w", encoding="utf-8") as out:
        for row in output_rows:
            out.write(json.dumps(row, ensure_ascii=False) + "\n")

    print(f"✔ Written: {output_path.name}")

print("✅ Stage 5 – LLM refinement model refinement WITH physical split completed.")
