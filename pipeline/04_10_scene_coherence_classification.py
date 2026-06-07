from pathlib import Path
import json

# ===============================
# CONFIG
# ===============================

INPUT_DIR = Path("data/stage_4_2")
OUTPUT_DIR = Path("data/stage_4_4")
OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

SIM_STRONG = 0.85
SIM_WEAK = 0.75
TENSE_CONF_MIN = 0.6

# ===============================
# CORE
# ===============================

for input_path in INPUT_DIR.glob("*with_scene_updates.jsonl"):
    print(f"▶ Coherence check: {input_path.name}")

    output_path = OUTPUT_DIR / input_path.name.replace(
        "with_scene_updates", "with_coherence"
    )

    paragraphs = []

    with input_path.open("r", encoding="utf-8") as f:
        for line in f:
            paragraphs.append(json.loads(line))

    for i in range(1, len(paragraphs)):
        prev_p = paragraphs[i - 1]
        curr_p = paragraphs[i]

        edge = curr_p.get("scene_edge")
        if not edge:
            continue

        signals = edge.get("signals", {})

        sim_prev = signals.get("sim_prev", 1.0)
        dialogue_jump = signals.get("dialogue_jump", False)
        tense_change = signals.get("tense_change", False)

        tense_conf = curr_p.get("tense_confidence", 0.0)
        token_pressure_prev = prev_p.get("token_count", 0) >= 800

        # -------------------------------------------------
        # 1️⃣ FALSE PARAGRAPH BOUNDARY
        # -------------------------------------------------
        if (
            dialogue_jump
            and sim_prev >= SIM_STRONG
            and not tense_change
            and token_pressure_prev
        ):
            curr_p["coherence_flag"] = "false_paragraph_boundary"
            curr_p["coherence_reason"] = (
                "Dialogue starts but semantic and temporal continuity is strong"
            )
            continue

        # -------------------------------------------------
        # 2️⃣ REAL SCENE CANDIDATE
        # -------------------------------------------------
        if (
            (tense_change and tense_conf >= TENSE_CONF_MIN)
            or (sim_prev < SIM_WEAK and dialogue_jump)
        ):
            curr_p["coherence_flag"] = "scene_candidate"
            curr_p["coherence_reason"] = "Strong narrative shift signals detected"
            continue

        # -------------------------------------------------
        # 3️⃣ UNCERTAIN → FLASH
        # -------------------------------------------------
        curr_p["coherence_flag"] = "uncertain"
        curr_p["coherence_reason"] = "Insufficient evidence for automatic decision"

    with output_path.open("w", encoding="utf-8") as out:
        for p in paragraphs:
            out.write(json.dumps(p, ensure_ascii=False) + "\n")

    print(f"  ✔ Written: {output_path.name}")

print("✅ Stage 04_2 Narrative Coherence Check completed.")
