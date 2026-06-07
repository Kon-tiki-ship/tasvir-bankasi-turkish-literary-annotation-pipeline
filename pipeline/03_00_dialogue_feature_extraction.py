from pathlib import Path
import json
import re

# ===============================
# CONFIG
# ===============================

BASE_DIR = Path("data/stage_2.1")
INPUT_SUFFIX = ".clean_stage2.jsonl"
OUTPUT_SUFFIX = ".clean_stage3.jsonl"
OUTPUT_DIR = Path("data/stage_3")
OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

# ===============================
# REGEX
# ===============================

DIALOGUE_LINE_RX = re.compile(r"^\s*[—\-]\s*.+", re.MULTILINE)
QUOTED_DIALOGUE_RX = re.compile(r"[\"“‘].+?[\"”’]", re.DOTALL)
SENTENCE_SPLIT_RX = re.compile(r"[.!?…]+")

# ===============================
# CORE
# ===============================

def count_sentences(text: str) -> int:
    return len([p for p in SENTENCE_SPLIT_RX.split(text) if p.strip()])


def extract_dialogue_text(text: str) -> str:
    parts = []
    parts.extend(DIALOGUE_LINE_RX.findall(text))
    parts.extend(QUOTED_DIALOGUE_RX.findall(text))
    return " ".join(parts)


def compute_dialogue_metrics(text: str):
    total_chars = len(text)
    total_sentences = count_sentences(text)

    dialogue_text = extract_dialogue_text(text)
    dialogue_chars = len(dialogue_text)
    dialogue_sentences = count_sentences(dialogue_text)

    return {
        "dialogue_char_ratio": round(dialogue_chars / total_chars, 4) if total_chars else 0.0,
        "dialogue_sentence_ratio": round(dialogue_sentences / total_sentences, 4) if total_sentences else 0.0,
        "has_dialogue": dialogue_chars > 0
    }

# ===============================
# MAIN
# ===============================

def main():
    files = list(BASE_DIR.glob(f"*{INPUT_SUFFIX}"))

    for input_path in files:
        # 🔧 TEK DÜZELTME: output dosyası artık OUTPUT_DIR içinde
        output_path = OUTPUT_DIR / input_path.name.replace(
            INPUT_SUFFIX, OUTPUT_SUFFIX
        )

        ok, skipped = 0, 0

        with input_path.open("r", encoding="utf-8", errors="replace") as fin, \
             output_path.open("w", encoding="utf-8") as fout:

            for ln, line in enumerate(fin, 1):
                try:
                    record = json.loads(line)
                except json.JSONDecodeError:
                    skipped += 1
                    continue  # BOZUK SATIRI ATLA

                text = record.get("text", "")
                record.update(compute_dialogue_metrics(text))
                fout.write(json.dumps(record, ensure_ascii=False) + "\n")
                ok += 1

        print(
            f"✅ {input_path.name} → {output_path.name} | "
            f"ok: {ok}, skipped: {skipped}"
        )

if __name__ == "__main__":
    main()
