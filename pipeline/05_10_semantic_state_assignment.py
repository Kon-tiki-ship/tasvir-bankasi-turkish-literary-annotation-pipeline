from __future__ import annotations

from pathlib import Path
import json
import os
import math
import time

from google import genai
from google.genai import types

# =========================================================
# CONFIG
# =========================================================

INPUT_DIR = Path("data/stage_5_1")
OUTPUT_DIR = Path("data/stage_5_2")
OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

EMBEDDING_MODEL = os.getenv("LLM_EMBEDDING_MODEL", "provider/default-semantic-embedding-model")
EMBEDDING_MODEL_PUBLIC_NAME = os.getenv("LLM_EMBEDDING_MODEL_PUBLIC_NAME", "provider_embedding_model_v1")

TOP_K = 3
MAX_RETRIES = 2
BACKOFF_BASE_SEC = 1.2


def get_required_env(*names: str) -> str:
    for name in names:
        value = os.getenv(name)
        if value:
            return value
    joined = " or ".join(names)
    raise RuntimeError(f"{joined} must be set in the environment before running this stage.")


client = genai.Client(api_key=get_required_env("LLM_API_KEY"))

# =========================================================
# STATE TAXONOMY (FINAL)
# =========================================================

STATE_LABELS = {
    # Internal States
    "inner_reflection": "A scene focused on internal thoughts, self-questioning, or introspection.",
    "existential_void": "A scene expressing emptiness, meaninglessness, or existential absence.",
    "self_deprecation": "A scene where the character devalues or diminishes themselves.",
    "melancholic_longing": "A quiet, restrained longing for someone or something unreachable.",
    "suppressed_resentment": "Unspoken frustration or resentment held internally.",
    "imaginative_escapism": "Retreat into imagination, memories, or inner fantasy.",
    "fatalistic_acceptance": "Passive acceptance of circumstances without resistance.",

    # Interpersonal Dynamics
    "social_discomfort": "Feeling out of place or uneasy in a social setting.",
    "awkward_silence": "Tense or uncomfortable silence between people.",
    "shared_intimacy": "Unspoken emotional closeness or mutual understanding.",
    "defensive_withdrawal": "Emotional retreat triggered by perceived threat or judgment.",
    "observational_scrutiny": "Careful, analytical observation of another person.",
    "misunderstood_connection": "Failed or distorted understanding between individuals.",

    # Ambient States
    "ambient_gloom": "Dark, heavy, or oppressive environmental atmosphere.",
    "detached_observation": "Emotionally neutral, camera-like observation of surroundings.",
    "nature_reflection": "Inner state mirrored through nature or landscape.",
    "bustling_solitude": "Loneliness experienced within a crowded or noisy environment.",
    "domestic_stagnation": "Static, repetitive, or suffocating domestic routine.",

    # Structural Transitions
    "transition_movement": "Movement between places without narrative event.",
    "narrative_pause": "Narrative halt for reflection or generalization.",
    "anticipation": "Waiting or emotional tension before an expected event.",
    "post_event_settling": "Emotional or ambient calm following an event.",
}

# =========================================================
# UTILS
# =========================================================

def embed(text: str) -> list[float]:
    resp = client.models.embed_content(
        model=EMBEDDING_MODEL,
        contents=text,
        config=types.EmbedContentConfig(
            task_type="semantic_similarity"
        ),
    )
    if hasattr(resp, "embedding"):
        return resp.embedding
    if hasattr(resp, "embeddings"):
        return resp.embeddings[0].values
    raise RuntimeError("Unknown embedding response format")


def cosine(a: list[float], b: list[float]) -> float:
    dot = sum(x*y for x, y in zip(a, b))
    na = math.sqrt(sum(x*x for x in a))
    nb = math.sqrt(sum(y*y for y in b))
    return dot / (na * nb + 1e-9)


# =========================================================
# PRE-EMBED LABELS (ANCHORS)
# =========================================================

LABEL_EMBEDDINGS = {}
for label, desc in STATE_LABELS.items():
    for attempt in range(MAX_RETRIES + 1):
        try:
            LABEL_EMBEDDINGS[label] = embed(desc)
            break
        except Exception:
            time.sleep(BACKOFF_BASE_SEC * (2 ** attempt))

# =========================================================
# PIPELINE
# =========================================================

for input_path in INPUT_DIR.glob("*.jsonl"):
    print(f"▶ Semantic state assignment: {input_path.name}")

    output_path = OUTPUT_DIR / input_path.name.replace(
        ".jsonl", "_state_identity.jsonl"
    )

    with input_path.open("r", encoding="utf-8") as f:
        records = [json.loads(line) for line in f if line.strip()]

    for r in records:
        text = (r.get("text") or "").strip()
        if not text:
            continue

        scene_vec = embed(text)

        scores = []
        for label, label_vec in LABEL_EMBEDDINGS.items():
            sim = cosine(scene_vec, label_vec)
            scores.append((label, round(sim, 4)))

        scores.sort(key=lambda x: x[1], reverse=True)

        r["state_identity_profile"] = {
            "top_states": scores[:TOP_K],
            "all_scores": scores,
            "embedding_model": EMBEDDING_MODEL_PUBLIC_NAME,
        }

    with output_path.open("w", encoding="utf-8") as out:
        for r in records:
            out.write(json.dumps(r, ensure_ascii=False) + "\n")

    print(f"✔ Written: {output_path.name}")

print("✅ Stage 05_10 — semantic state assignment completed.")
