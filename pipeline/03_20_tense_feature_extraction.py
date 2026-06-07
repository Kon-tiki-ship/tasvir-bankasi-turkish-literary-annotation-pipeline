from pathlib import Path
import json
import re

# ===============================
# CONFIG
# ===============================

INPUT_DIR = Path("data/stage_4")
OUTPUT_DIR = Path("data/stage_4_1")
OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

# -------------------------------
# TÜRKÇE KİP İPUÇLARI
# (ekler kelime SONUNDA aranır)
# -------------------------------

PAST_RX = re.compile(
    r"(di|dı|du|dü|ti|tı|tu|tü|mış|miş|muş|müş)$",
    re.IGNORECASE
)

PRESENT_RX = re.compile(
    r"(yor|makta|mekte)$",
    re.IGNORECASE
)

AORIST_RX = re.compile(
    r"(ar|er|r)$",
    re.IGNORECASE
)

# -------------------------------
# TOKEN TEMİZLEME REGEX
# -------------------------------

CLEAN_TOKEN_RX = re.compile(r"[^\wçğıöşü]", re.IGNORECASE)

# ===============================
# HELPERS
# ===============================

def normalize_tokens(text: str):
    """
    Noktalama ve özel karakterlerden arındırılmış,
    küçük harfe çevrilmiş token listesi üretir.
    """
    raw_tokens = text.split()
    tokens = [
        CLEAN_TOKEN_RX.sub("", t.lower())
        for t in raw_tokens
        if t.strip()
    ]
    return tokens


def detect_tense(text: str):
    tokens = normalize_tokens(text)

    past = sum(1 for t in tokens if PAST_RX.search(t))
    present = sum(1 for t in tokens if PRESENT_RX.search(t))
    aorist = sum(1 for t in tokens if AORIST_RX.search(t))

    total = past + present + aorist

    if total == 0:
        return {
            "tense_mode": "unknown",
            "tense_distribution": {},
            "tense_confidence": 0.0
        }

    dist = {
        "past": round(past / total, 3),
        "present": round(present / total, 3),
        "aorist": round(aorist / total, 3)
    }

    dominant = max(dist, key=dist.get)

    return {
        "tense_mode": dominant,
        "tense_distribution": dist,
        "tense_confidence": dist[dominant]
    }

# ===============================
# CORE
# ===============================

# daha esnek glob (clean_stage3.jsonl dahil)
input_files = sorted(INPUT_DIR.glob("*stage4.jsonl"))

if not input_files:
    raise FileNotFoundError(
        f"{INPUT_DIR.resolve()} içinde *stage4.jsonl dosyası bulunamadı."
    )

for input_path in input_files:
    print(f"▶ İşleniyor: {input_path.name}")

    output_path = OUTPUT_DIR / input_path.name.replace(
        "stage4.jsonl", "stage4_with_tense.jsonl"
    )

    with input_path.open("r", encoding="utf-8") as fin, \
         output_path.open("w", encoding="utf-8") as fout:

        for line in fin:
            rec = json.loads(line)

            tense_info = detect_tense(rec.get("text", ""))
            rec.update(tense_info)

            fout.write(json.dumps(rec, ensure_ascii=False) + "\n")

    print(f"  ✔ Yazıldı: {output_path.name}")
