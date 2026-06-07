from __future__ import annotations

from pathlib import Path
import json
import re

INPUT_DIR = Path("data/stage_5_4")
OUTPUT_DIR = Path("data/stage_5_8")
OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

try:
    from zemberek.morphology import TurkishMorphology  # type: ignore

    _MORPHOLOGY = TurkishMorphology.create_with_defaults()
except Exception:
    _MORPHOLOGY = None

CATEGORY_POS_MAP = {
    "descr_human": {"Noun", "Adj", "Verb"},
    "descr_emotion": {"Adj", "Verb"},
    "descr_location": {"Noun"},
    "descr_nature": {"Noun", "Adj"},
    "descr_action": {"Verb"},
    "descr_object": {"Noun"},
    "descr_psychology": {"Verb", "Adj"},
    "descr_metaphor": {"Adj"},
}

TOKEN_PATTERN = re.compile(r"[A-Za-zCÇGĞIİOÖSŞUÜa-zcçgğiıoösşuü]+", re.UNICODE)


def tr_lower(text: str) -> str:
    return text.translate(str.maketrans({"I": "ı", "İ": "i"})).lower()


def extract_morphology(text: str) -> list[tuple[str, str]]:
    if _MORPHOLOGY is None:
        # fallback: lightweight heuristic if zemberek is not available
        return [(tr_lower(m.group(0)), "Noun") for m in TOKEN_PATTERN.finditer(text)]

    results: list[tuple[str, str]] = []
    analysis = _MORPHOLOGY.analyze_sentence(text)
    for token_analysis in analysis:
        analyses = token_analysis.analysis_results
        if not analyses:
            continue
        best = analyses[0]
        analysis_str = best.format_string()
        stem = best.get_stem()
        if not stem:
            continue
        stem_lower = tr_lower(stem)
        if ":Verb" in analysis_str:
            pos = "Verb"
        elif ":Noun" in analysis_str:
            pos = "Noun"
        elif ":Adj" in analysis_str:
            pos = "Adj"
        else:
            continue
        results.append((stem_lower, pos))
    return results


def enrich_profile(text: str, base_profile: list[dict]) -> list[dict]:
    morph_data = extract_morphology(text)
    enriched_profile: list[dict] = []

    for block in base_profile:
        category = block.get("category")
        allowed_pos = CATEGORY_POS_MAP.get(category, set())

        nouns: set[str] = set()
        verbs: set[str] = set()
        adjectives: set[str] = set()

        for stem, pos in morph_data:
            if pos not in allowed_pos:
                continue
            if pos == "Noun":
                nouns.add(stem)
            elif pos == "Verb":
                verbs.add(stem)
            elif pos == "Adj":
                adjectives.add(stem)

        enriched_profile.append(
            {
                "category": category,
                "lexical_breakdown": {
                    "nouns": sorted(nouns),
                    "verbs": sorted(verbs),
                    "adjectives": sorted(adjectives),
                },
            }
        )

    return enriched_profile


def run_pipeline(input_dir: Path = INPUT_DIR, output_dir: Path = OUTPUT_DIR) -> None:
    output_dir.mkdir(parents=True, exist_ok=True)
    for input_path in input_dir.glob("*.jsonl"):
        print(f"[06_10] Description lexical enrichment: {input_path.name}")
        output_path = output_dir / input_path.name.replace(".jsonl", "_stage_5_8.jsonl")

        with input_path.open("r", encoding="utf-8") as handle:
            records = [json.loads(line) for line in handle if line.strip()]

        for record in records:
            text = record.get("text", "")
            base_profile = record.get("descriptive_profile")
            if not text or not base_profile:
                if "descriptive_profile_enriched" in record:
                    del record["descriptive_profile_enriched"]
                continue
            record["descriptive_profile_enriched"] = enrich_profile(text, base_profile)

        with output_path.open("w", encoding="utf-8") as out:
            for record in records:
                out.write(json.dumps(record, ensure_ascii=False) + "\n")

        print(f"[06_10] Written: {output_path.name}")

    print("[06_10] Completed.")


if __name__ == "__main__":
    run_pipeline()
