from __future__ import annotations

import argparse
import importlib.util
import json
from collections import Counter
from pathlib import Path
from typing import Any


DESCRIPTIVE_FIELDS = [
    "descriptive_profile",
    "descriptive_profile_enriched",
    "descriptive_profile_enriched_filtered",
]

BACKUP_MAP = {
    "descriptive_profile": "descriptive_profile_previous_backup",
    "descriptive_profile_enriched": "descriptive_profile_enriched_previous_backup",
    "descriptive_profile_enriched_filtered": "descriptive_profile_enriched_filtered_previous_backup",
}

RISK_PAIRS = [
    ("grev", "ev"),
    ("otel", "el"),
    ("güzel", "el"),
    ("karımı", "kar"),
    ("karar", "kar"),
    ("karşı", "kar"),
    ("Karahisarlı", "kar"),
    ("gölge", "gol"),
    ("boyanmış", "boy"),
    ("tutan", "utan"),
    ("ibarettir", "bar"),
    ("beraber", "bar"),
    ("karısı", "kar"),
    ("karısına", "kar"),
    ("karısını", "kar"),
    ("elektriğini", "el"),
    ("güzelliğiyle", "el"),
    ("ellilik", "el"),
    ("altı yüz lira", "yuz"),
    ("yüz lira", "yuz"),
    ("iki yüz kuruş", "yuz"),
    ("yağmurluk", "yagmur"),
    ("tutturulmuş", "tuttu"),
    ("çiçek motifli", "cicek"),
    ("çiçek çizilmiş", "cicek"),
]


def load_module(module_path: Path, module_name: str):
    spec = importlib.util.spec_from_file_location(module_name, module_path)
    if spec is None or spec.loader is None:
        raise RuntimeError(f"Cannot load module: {module_path}")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def extract_reasons(profile: list[dict]) -> set[str]:
    out: set[str] = set()
    for block in profile:
        for reason in block.get("reasons", []):
            out.add(reason)
    return out


def contains_false_pair(text: str, reason: str, stage05_4) -> bool:
    folded_text = stage05_4.fold_turkish(text)
    folded_reason = stage05_4.fold_turkish(reason)
    return folded_reason in folded_text


def record_needs_human_check(profile: list[dict]) -> bool:
    # conservative marker for empty profile after regeneration from non-empty previous
    return len(profile) == 0


def find_human_review_items(record: dict[str, Any], old_reasons: set[str], new_reasons: set[str]) -> list[dict[str, Any]]:
    text = (record.get("text") or "").lower()
    source_file = record.get("__source_file", "")
    micro_block_id = record.get("micro_block_id", "")
    queue: list[dict[str, Any]] = []

    if "çiçek" in text and ("motif" in text or "çizil" in text or "oyuncak" in text or "yaldız" in text):
        queue.append(
            {
                "source_file": source_file,
                "micro_block_id": micro_block_id,
                "issue_type": "decorative_nature_ambiguity",
                "suspected_false_label": "cicek",
                "suspected_source_phrase": "çiçek motif/çizili/dekoratif bağlam",
                "recommended_action": "prefer_non_nature_and_manual_review",
                "notes": "Decorative flower motif likely object/decor, not live nature signal.",
            }
        )
    return queue


def process_file(path: Path, stage05_4, stage05_8, stage05_8_1, report: dict[str, Any], curation_ledger: list[dict[str, Any]]) -> None:
    lines = path.read_text(encoding="utf-8").splitlines()
    updated_lines: list[str] = []

    for line in lines:
        if not line.strip():
            continue
        record = json.loads(line)
        original = json.loads(line)
        record["__source_file"] = path.name

        previous_present = False
        for field in DESCRIPTIVE_FIELDS:
            backup_field = BACKUP_MAP[field]
            if field in record:
                previous_present = True
                if backup_field not in record:
                    record[backup_field] = record[field]
                del record[field]

        text = (record.get("text") or "").strip()
        profile = stage05_4.build_descriptive_profile(text) if text else []
        if profile:
            record["descriptive_profile"] = profile

        enriched = stage05_8.enrich_profile(text, profile) if (text and profile) else []
        if enriched:
            record["descriptive_profile_enriched"] = enriched

        filtered = stage05_8_1.filter_enriched_profile(enriched) if enriched else []
        if filtered:
            record["descriptive_profile_enriched_filtered"] = filtered

        changed = record != original
        if changed:
            report["records_cleaned"] += 1
        else:
            report["unchanged_records"] += 1

        old_reasons = extract_reasons(original.get("descriptive_profile", []))
        new_reasons = extract_reasons(record.get("descriptive_profile", []))
        removed = old_reasons - new_reasons

        for removed_reason in removed:
            report["removed_reason_counts"][removed_reason] += 1

        for suspect_word, suspect_label in RISK_PAIRS:
            if suspect_label in old_reasons and suspect_label not in new_reasons:
                if contains_false_pair(suspect_word, suspect_label, stage05_4):
                    report["false_positive_removed"] += 1
                    report["false_positive_label_counts"][suspect_label] += 1

        if previous_present and record_needs_human_check(profile):
            report["human_review_needed"] += 1

        curation_ledger.extend(find_human_review_items(record, old_reasons, new_reasons))
        del record["__source_file"]

        updated_lines.append(json.dumps(record, ensure_ascii=False))

    path.write_text("\n".join(updated_lines) + "\n", encoding="utf-8")


def main() -> None:
    parser = argparse.ArgumentParser(description="Clean and regenerate descriptive fields safely.")
    parser.add_argument("--input", action="append", required=True, help="Input directory containing JSONL files. Can be repeated.")
    parser.add_argument("--report", required=True, help="Output report JSON path.")
    parser.add_argument("--human-review-report", required=False, help="Optional output JSON path for human review queue.")
    args = parser.parse_args()

    repo_root = Path(__file__).resolve().parents[1]
    stage05_4 = load_module(repo_root / "pipeline" / "06_00_description_category_tagging.py", "stage05_4")
    stage05_8 = load_module(repo_root / "pipeline" / "06_10_description_lexical_enrichment.py", "stage05_8")
    stage05_8_1 = load_module(repo_root / "pipeline" / "06_20_description_evidence_filtering.py", "stage05_8_1")

    report: dict[str, Any] = {
        "records_cleaned": 0,
        "unchanged_records": 0,
        "false_positive_removed": 0,
        "removed_reason_counts": Counter(),
        "false_positive_label_counts": Counter(),
        "human_review_needed": 0,
        "processed_files": [],
    }
    curation_ledger: list[dict[str, Any]] = []

    for input_dir in args.input:
        directory = Path(input_dir)
        for file_path in sorted(directory.glob("*.jsonl")):
            process_file(file_path, stage05_4, stage05_8, stage05_8_1, report, curation_ledger)
            report["processed_files"].append(str(file_path))

    output_path = Path(args.report)
    output_path.parent.mkdir(parents=True, exist_ok=True)
    serializable_report = {
        **report,
        "removed_reason_counts": dict(sorted(report["removed_reason_counts"].items())),
        "false_positive_label_counts": dict(sorted(report["false_positive_label_counts"].items())),
    }
    output_path.write_text(json.dumps(serializable_report, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(f"Report written: {output_path}")

    if args.human_review_report:
        hr_path = Path(args.human_review_report)
        hr_path.parent.mkdir(parents=True, exist_ok=True)
        hr_path.write_text(json.dumps(curation_ledger, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
        print(f"Human review queue written: {hr_path}")


if __name__ == "__main__":
    main()
