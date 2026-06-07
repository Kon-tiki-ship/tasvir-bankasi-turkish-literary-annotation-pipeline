from __future__ import annotations

from pathlib import Path
import json
import re

from zemberek.morphology import TurkishMorphology

# =========================================================
# CONFIG
# =========================================================

INPUT_DIR = Path("data/stage_5")
OUTPUT_DIR = Path("data/stage_5_0")
OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

TARGET_SCENE_SOURCE = "llm_refinement_split_scene"

# =========================================================
# ZEMBEREK INIT
# =========================================================

morphology = TurkishMorphology.create_with_defaults()

# =========================================================
# REGEX – DIALOGUE
# =========================================================

DIALOGUE_LINE_RX = re.compile(r"^\s*[—\-]\s*.+", re.MULTILINE)
QUOTED_DIALOGUE_RX = re.compile(r"[\"“‘].+?[\"”’]", re.DOTALL)
SENTENCE_SPLIT_RX = re.compile(r"[.!?…]+")

# =========================================================
# REGEX – MORPHO / TENSE
# =========================================================

NON_FINITE_RX = re.compile(r"(Inf|Part|Conv)", re.IGNORECASE)

PAST_RX = re.compile(r"(di|dı|du|dü|ti|tı|tu|tü|mış|miş|muş|müş)$", re.IGNORECASE)
PRESENT_RX = re.compile(r"(yor|makta|mekte)$", re.IGNORECASE)
AORIST_RX = re.compile(r"(ar|er|r)$", re.IGNORECASE)

CLEAN_TOKEN_RX = re.compile(r"[^\wçğıöşü]", re.IGNORECASE)

# =========================================================
# HELPERS
# =========================================================

def count_sentences(text: str) -> int:
    return len([p for p in SENTENCE_SPLIT_RX.split(text) if p.strip()])


def extract_dialogue_text(text: str) -> str:
    parts = []
    parts.extend(DIALOGUE_LINE_RX.findall(text))
    parts.extend(QUOTED_DIALOGUE_RX.findall(text))
    return " ".join(parts)


def compute_dialogue_metrics(text: str) -> dict:
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


def compute_morpho_stats(text: str) -> dict:
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
        best = results[0]
        s = best.format_string()

        if ":Verb" in s:
            counts["verb"] += 1
            if NON_FINITE_RX.search(s):
                counts["non_finite_verb"] += 1
        elif ":Noun" in s:
            counts["noun"] += 1
        elif ":Adj" in s:
            counts["adj"] += 1
        elif ":Adv" in s:
            counts["adv"] += 1

    if token_count == 0:
        return {}

    return {
        "token_count": token_count,
        "noun_ratio": round(counts["noun"] / token_count, 4),
        "verb_ratio": round(counts["verb"] / token_count, 4),
        "adj_ratio": round(counts["adj"] / token_count, 4),
        "adv_ratio": round(counts["adv"] / token_count, 4),
        "non_finite_verb_ratio": round(counts["non_finite_verb"] / token_count, 4)
    }


def normalize_tokens(text: str):
    raw = text.split()
    return [
        CLEAN_TOKEN_RX.sub("", t.lower())
        for t in raw
        if t.strip()
    ]


def detect_tense(text: str) -> dict:
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

# =========================================================
# MAIN ORCHESTRATOR
# =========================================================

def main():
    files = list(INPUT_DIR.glob("*.jsonl"))
    if not files:
        raise FileNotFoundError("stage_5 klasöründe jsonl dosyası bulunamadı.")

    for input_path in files:
        output_path = OUTPUT_DIR / input_path.name.replace(
            "stage_5", "stage_5_1"
        )

        total, fixed = 0, 0

        with input_path.open("r", encoding="utf-8") as fin, \
             output_path.open("w", encoding="utf-8") as fout:

            for line in fin:
                total += 1
                record = json.loads(line)

                if record.get("scene_source") != TARGET_SCENE_SOURCE:
                    fout.write(json.dumps(record, ensure_ascii=False) + "\n")
                    continue

                text = record.get("text", "")

                record.update(compute_dialogue_metrics(text))
                record.update(compute_morpho_stats(text))
                record.update(detect_tense(text))

                record["cleanup_stage"] = "04_50_scene_split_postprocessing"
                record["stats_recomputed"] = True

                # eski fallback kararını geçersiz kıl
                if "fallback_review" in record:
                    record["fallback_review"]["invalidated"] = True
                    record["fallback_review"]["reason"] = "stats_recomputed"

                fout.write(json.dumps(record, ensure_ascii=False) + "\n")
                fixed += 1

        print(
            f"✅ {input_path.name} → {output_path.name} | "
            f"toplam: {total}, düzeltildi: {fixed}"
        )


if __name__ == "__main__":
    main()
