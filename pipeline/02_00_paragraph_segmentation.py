from pathlib import Path
import json
import re

# ===============================
# CONFIG
# ===============================

INPUT_DIR = Path("data/clean_text")          # temizlenmiş txt'ler
OUTPUT_DIR = Path("data/stage_2")         # paragraf çıktıları
OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

MIN_PARAGRAPH_CHARS = 40   # çok kısa paragrafları atmak için
NORMALIZE_SPACES = True

# ===============================
# REGEX
# ===============================

# Bir veya daha fazla boş satır = paragraf sınırı
PARA_SPLIT_RX = re.compile(r"\n\s*\n+")

# Satır içi fazla boşluklar
MULTI_SPACE_RX = re.compile(r"[ \t]+")

# ===============================
# CORE FUNCTIONS
# ===============================

def normalize_text(text: str) -> str:
    if NORMALIZE_SPACES:
        text = MULTI_SPACE_RX.sub(" ", text)
    return text.strip()


def split_paragraphs(text: str):
    raw_paragraphs = PARA_SPLIT_RX.split(text)
    paragraphs = []

    for p in raw_paragraphs:
        p = normalize_text(p)
        if len(p) < MIN_PARAGRAPH_CHARS:
            continue
        paragraphs.append(p)

    return paragraphs


def process_file(path: Path):
    text = path.read_text(encoding="utf-8")
    paragraphs = split_paragraphs(text)

    story_id = path.stem
    total = len(paragraphs)

    records = []
    for idx, para in enumerate(paragraphs, start=1):
        records.append({
            "story_id": story_id,
            "paragraph_id": f"{story_id}_p{idx:03d}",
            "paragraph_index": idx,
            "total_paragraphs": total,
            "text": para
        })

    return records


# ===============================
# MAIN
# ===============================

def main():
    for txt_file in INPUT_DIR.glob("*.txt"):
        records = process_file(txt_file)

        # 🔹 çıktı dosya adı: orijinal_ad_stage2.jsonl
        out_name = f"{txt_file.stem}_stage2.jsonl"
        out_path = OUTPUT_DIR / out_name

        with out_path.open("w", encoding="utf-8") as f:
            for rec in records:
                f.write(json.dumps(rec, ensure_ascii=False) + "\n")

        print(f"✅ {txt_file.name} → {out_name} ({len(records)} paragraphs)")


if __name__ == "__main__":
    main()
