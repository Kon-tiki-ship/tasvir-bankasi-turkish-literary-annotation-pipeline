from pathlib import Path
import json
import re

from zemberek.morphology import TurkishMorphology

# ===============================
# CONFIG
# ===============================

INPUT_DIR = Path("data/stage_3")
OUTPUT_DIR = Path("data/stage_4")
OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

# ===============================
# ZEMBEREK (PYTHON)
# ===============================

morphology = TurkishMorphology.create_with_defaults()

# ===============================
# REGEX
# ===============================

# fiilimsi: isim-fiil, sıfat-fiil, zarf-fiil
NON_FINITE_RX = re.compile(r"(Inf|Part|Conv)", re.IGNORECASE)

# ===============================
# CORE
# ===============================

def compute_morpho_stats(text: str):
    """
    zemberek-python çıktısını format_string() üzerinden parse ederek
    morfolojik oranları hesaplar
    """

    analysis = morphology.analyze_sentence(text)

    counts = {
        "noun": 0,
        "verb": 0,
        "adj": 0,
        "adv": 0,
        "non_finite_verb": 0
    }

    token_count = 0

    for token_analysis in analysis:
        results = token_analysis.analysis_results
        if not results:
            continue

        token_count += 1

        # En olası analiz
        best = results[0]

        # Örnek çıktı:
        # hazırla:Verb+Prog1+A3sg+Past
        analysis_str = best.format_string()

        if ":Verb" in analysis_str:
            counts["verb"] += 1
            if NON_FINITE_RX.search(analysis_str):
                counts["non_finite_verb"] += 1

        elif ":Noun" in analysis_str:
            counts["noun"] += 1

        elif ":Adj" in analysis_str:
            counts["adj"] += 1

        elif ":Adv" in analysis_str:
            counts["adv"] += 1

    if token_count == 0:
        return {}

    return {
        "token_count": token_count,
        "noun_ratio": round(counts["noun"] / token_count, 4),
        "verb_ratio": round(counts["verb"] / token_count, 4),
        "adj_ratio": round(counts["adj"] / token_count, 4),
        "adv_ratio": round(counts["adv"] / token_count, 4),
        "non_finite_verb_ratio": round(
            counts["non_finite_verb"] / token_count, 4
        )
    }

# ===============================
# MAIN
# ===============================

def main():
    total_paragraphs = 0
    processed_files = 0

    for input_path in INPUT_DIR.glob("*.jsonl"):
        output_name = input_path.name.replace("stage3", "stage4")
        output_path = OUTPUT_DIR / output_name

        with input_path.open("r", encoding="utf-8") as fin, \
             output_path.open("w", encoding="utf-8") as fout:

            for line in fin:
                record = json.loads(line)
                text = record.get("text", "")

                morpho = compute_morpho_stats(text)
                record.update(morpho)

                fout.write(
                    json.dumps(record, ensure_ascii=False) + "\n"
                )

                total_paragraphs += 1

        processed_files += 1
        print(f"✅ Processed file: {input_path.name}")

    print(
        f"\n🎉 Stage 4 completed\n"
        f"📂 Files processed : {processed_files}\n"
        f"🧩 Paragraphs     : {total_paragraphs}"
    )


if __name__ == "__main__":
    main()
