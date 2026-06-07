from __future__ import annotations

from pathlib import Path
import json

INPUT_DIR = Path("data/stage_5_8")
OUTPUT_DIR = Path("data/stage_5_8_1")
OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

MIN_TOKEN_LEN = 3

STEM_BLACKLIST = {"ker", "insa", "duma", "roma", "se", "te", "sey", "bir", "cok", "az", "her"}

SEMANTIC_WHITELISTS = {
    "descr_location": {"ev", "oda", "sokak", "yol", "bina", "salon", "bahce", "meydan", "koridor", "istasyon", "bar"},
    "descr_nature": {"yagmur", "kar", "ruzgar", "agac", "gol", "deniz", "orman", "hava", "toprak"},
    "descr_object": {"masa", "sandalye", "defter", "kapi", "pencere", "elbise", "kurk", "canta"},
}


def clean_tokens(tokens: list[str]) -> list[str]:
    cleaned: list[str] = []
    for token in tokens:
        if not token:
            continue
        if len(token) < MIN_TOKEN_LEN:
            continue
        if token in STEM_BLACKLIST:
            continue
        cleaned.append(token)
    return cleaned


def apply_semantic_filter(category: str, tokens: list[str]) -> list[str]:
    whitelist = SEMANTIC_WHITELISTS.get(category)
    if not whitelist:
        return tokens
    return [token for token in tokens if token in whitelist]


def filter_enriched_profile(enriched: list[dict]) -> list[dict]:
    filtered_profile: list[dict] = []
    for block in enriched:
        category = block.get("category")
        lex = block.get("lexical_breakdown", {})

        nouns = clean_tokens(lex.get("nouns", []))
        verbs = clean_tokens(lex.get("verbs", []))
        adjectives = clean_tokens(lex.get("adjectives", []))

        nouns = apply_semantic_filter(category, nouns)

        if not (nouns or verbs or adjectives):
            continue

        filtered_profile.append(
            {
                "category": category,
                "lexical_breakdown": {"nouns": nouns, "verbs": verbs, "adjectives": adjectives},
            }
        )
    return filtered_profile


def run_pipeline(input_dir: Path = INPUT_DIR, output_dir: Path = OUTPUT_DIR) -> None:
    output_dir.mkdir(parents=True, exist_ok=True)
    for input_path in input_dir.glob("*.jsonl"):
        print(f"[06_20] Filtering description evidence: {input_path.name}")
        output_path = output_dir / input_path.name.replace(".jsonl", "_stage_5_8_1.jsonl")

        with input_path.open("r", encoding="utf-8") as handle:
            records = [json.loads(line) for line in handle if line.strip()]

        for record in records:
            enriched = record.get("descriptive_profile_enriched")
            if not enriched:
                if "descriptive_profile_enriched_filtered" in record:
                    del record["descriptive_profile_enriched_filtered"]
                continue
            record["descriptive_profile_enriched_filtered"] = filter_enriched_profile(enriched)

        with output_path.open("w", encoding="utf-8") as out:
            for record in records:
                out.write(json.dumps(record, ensure_ascii=False) + "\n")

        print(f"[06_20] Written: {output_path.name}")

    print("[06_20] Completed.")


if __name__ == "__main__":
    run_pipeline()
