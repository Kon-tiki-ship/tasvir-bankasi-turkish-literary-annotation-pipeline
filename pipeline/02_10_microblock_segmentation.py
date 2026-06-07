from pathlib import Path
import json
import re

# ===============================
# CONFIG
# ===============================

INPUT_DIR = Path("data/stage_2")
OUTPUT_DIR = Path("data/stage_2.1")
OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

MIN_BLOCK_CHARS = 400
MAX_BLOCK_CHARS = 800

# ===============================
# REGEX
# ===============================

BREAK_MARKERS_RX = re.compile(
    r"(?:^|\s)(Fakat|Ama|Ancak|Lakin|Halbuki|Ne var ki)\b",
    re.IGNORECASE
)

QUESTION_CLUSTER_RX = re.compile(
    r"(\?[\s\"]+)(?=[A-ZÇĞİÖŞÜ])"
)

# ===============================
# CORE
# ===============================

def split_micro_blocks(text: str) -> list[str]:
    blocks = []

    parts = []
    for seg in text.split(":"):
        if parts:
            parts[-1] += ":"
        parts.append(seg.strip())

    for part in parts:
        start = 0
        matches = list(BREAK_MARKERS_RX.finditer(part))

        if not matches:
            blocks.append(part.strip())
            continue

        for m in matches:
            end = m.start()
            if end - start >= MIN_BLOCK_CHARS:
                blocks.append(part[start:end].strip())
                start = end

        remainder = part[start:].strip()
        if remainder:
            blocks.append(remainder)

    final_blocks = []
    for block in blocks:
        if len(block) <= MAX_BLOCK_CHARS:
            final_blocks.append(block)
            continue

        splits = QUESTION_CLUSTER_RX.split(block)
        temp = ""
        for s in splits:
            temp += s
            if len(temp) >= MIN_BLOCK_CHARS:
                final_blocks.append(temp.strip())
                temp = ""

        if temp.strip():
            final_blocks.append(temp.strip())

    merged = []
    for b in final_blocks:
        if merged and len(b) < MIN_BLOCK_CHARS:
            merged[-1] += " " + b
        else:
            merged.append(b)

    return merged


# ===============================
# FILE PROCESSOR
# ===============================

def process_file(input_path: Path):
    output_name = input_path.name.replace(
        ".stage_2.jsonl", ".stage_2.1.jsonl"
    )
    output_path = OUTPUT_DIR / output_name

    total_blocks = 0
    bad_lines = 0

    with input_path.open("r", encoding="utf-8", errors="replace") as fin, \
         output_path.open("w", encoding="utf-8") as fout:

        for line_no, line in enumerate(fin, start=1):
            line = line.strip()
            if not line:
                continue

            try:
                rec = json.loads(line)
            except json.JSONDecodeError:
                bad_lines += 1
                print(
                    f"⚠ JSON hatası atlandı | "
                    f"{input_path.name} | satır {line_no}"
                )
                continue

            text = rec.get("text", "")
            if not text:
                continue

            micro_blocks = split_micro_blocks(text)

            for i, block in enumerate(micro_blocks, start=1):
                new_rec = rec.copy()
                new_rec["micro_block_id"] = (
                    f"{rec.get('paragraph_id','unk')}_mb{i:02d}"
                )
                new_rec["parent_paragraph_id"] = rec.get("paragraph_id")
                new_rec["text"] = block
                new_rec["is_micro_block"] = True
                new_rec["stage"] = "2.1"

                fout.write(
                    json.dumps(new_rec, ensure_ascii=False) + "\n"
                )
                total_blocks += 1

    print(
        f"✔ {input_path.name} → {output_name} | "
        f"micro-blocks: {total_blocks} | "
        f"atlanan satır: {bad_lines}"
    )


# ===============================
# MAIN
# ===============================

def main():
    files = sorted(INPUT_DIR.glob("*.jsonl"))

    if not files:
        print("⚠ stage_2 klasöründe jsonl dosyası yok.")
        return

    print(f"📂 İşlenecek dosya sayısı: {len(files)}")

    for path in files:
        process_file(path)

    print("✅ Stage 2 → Stage 2.1 tamamlandı.")


if __name__ == "__main__":
    main()
