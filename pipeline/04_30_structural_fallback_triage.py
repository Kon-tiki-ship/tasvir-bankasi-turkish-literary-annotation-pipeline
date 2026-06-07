# =========================================================
# Stage 4_9 – Structural Fallback Review (NON-LLM)
# Purpose:
# - Identify which structural_fallback blocks are eligible
#   for LLM refinement model refinement
# - NO LLM calls
# - NO scene splitting
# - Metadata-only enrichment
# =========================================================

from pathlib import Path
import json

# =========================================================
# CONFIG
# =========================================================

INPUT_DIR  = Path("data/stage_4_8")
OUTPUT_DIR = Path("data/stage_4_9")
OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

TOKEN_THRESHOLD = 250  # Proven optimal threshold

# =========================================================
# PIPELINE
# =========================================================

for input_path in INPUT_DIR.glob("*.jsonl"):
    print(f"▶ Processing: {input_path.name}")

    output_path = OUTPUT_DIR / input_path.name.replace("4_8", "4_9")

    with input_path.open("r", encoding="utf-8") as f_in, \
         output_path.open("w", encoding="utf-8") as f_out:

        for line in f_in:
            row = json.loads(line)

            scenes = row.get("scene_segments", {}).get("scenes", [])
            token_count = int(row.get("token_count", 0))

            # Default: no fallback review
            fallback_review = None

            # Check structural_fallback
            if scenes and scenes[0].get("split_reason") == "structural_fallback":
                if token_count >= TOKEN_THRESHOLD:
                    fallback_review = {
                        "eligible_for_llm_refinement": True,
                        "priority": "high",
                        "reason": "high_token_structural_fallback",
                        "token_count": token_count
                    }
                else:
                    fallback_review = {
                        "eligible_for_llm_refinement": False,
                        "reason": "below_token_threshold",
                        "token_count": token_count
                    }

            if fallback_review is not None:
                row["fallback_review"] = fallback_review

            f_out.write(json.dumps(row, ensure_ascii=False) + "\n")

    print(f"✔ Written: {output_path.name}")

print("✅ Stage 4_9 – structural fallback review completed.")
