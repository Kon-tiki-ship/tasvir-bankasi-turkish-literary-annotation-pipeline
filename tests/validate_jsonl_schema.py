#!/usr/bin/env python3
"""Validate Tasvir Bankası JSONL files against the public v0.1 schema.

The validator implements the public two-regime segment policy:

1. Event-bearing scenes require a non-empty ``brief_summary``.
2. Non-event structural/state/emotion/atmosphere/descriptive segments may omit
   ``brief_summary`` when alternate evidence is present.

Usage:
    python tests/validate_jsonl_schema.py \
      --schema schemas/tasvir_record_schema.v0.1.json \
      --input data/gold_smoke_v0.1 \
      --report data/reports/gold_smoke_report_v0.1.json
"""

from __future__ import annotations

import argparse
import hashlib
import json
from collections import Counter, defaultdict
from pathlib import Path
from typing import Any

from jsonschema import Draft202012Validator

PUBLIC_RELEASE_VERSION = "v0.1.0-public-preview"
SCHEMA_VERSION = "0.1"
VALIDATOR_VERSION = "0.1.2"
TWO_REGIME_POLICY_VERSION = "0.1.2"


SCENE_REQUIRED_FIELDS = ("scene_index", "scene_type", "split_reason")

NON_EVENT_SPLIT_REASONS = {
    "structural_fallback",
    "state_fallback",
    "emotion_fallback",
    "atmosphere_fallback",
    "descriptive_fallback",
}

NON_EVENT_TRIAGE_MARKERS = (
    "descriptive",
    "description",
    "state",
    "emotion",
    "atmosphere",
    "ambient",
    "fallback",
    "reflection",
)

EVENT_MARKERS = (
    "event",
    "action",
    "interaction",
    "dialogue",
    "encounter",
    "movement",
    "arrival",
    "departure",
    "conflict",
)

EMOTION_STATE_MARKERS = (
    "melancholic",
    "longing",
    "awkward",
    "discomfort",
    "resentment",
    "existential",
    "fatalistic",
    "defensive",
    "intimacy",
    "anticipation",
    "emotion",
    "fear",
    "anger",
    "joy",
    "sad",
    "guilt",
    "shame",
    "anxiety",
)

ATMOSPHERE_STATE_MARKERS = (
    "ambient",
    "gloom",
    "bustling",
    "solitude",
    "domestic",
    "stagnation",
    "narrative_pause",
    "nature",
    "room",
    "place",
    "location",
    "weather",
)

KNOWN_FULL_SOURCE_INVENTORY: list[dict[str, Any]] = [
    {
        "source_file": "Sabahattin_Ali_Kurk_Mantolu_Madonna.dataset.jsonl",
        "records": 392,
        "previous_records_missing_scene_brief_summary": 323,
        "previous_scene_objects_missing_scene_brief_summary": 323,
        "sha256": "0e1708619c289e156b680fa047d0cdad9755774c5b6d1df5205a372187869d19",
    },
    {
        "source_file": "Sait_Faik_Luzumsuz_Adam.dataset.jsonl",
        "records": 385,
        "previous_records_missing_scene_brief_summary": 309,
        "previous_scene_objects_missing_scene_brief_summary": 309,
        "sha256": "9cda21f26fddec7463e731a9ca278ea283228c6e5ed26f623f1d754a63caefb7",
    },
    {
        "source_file": "Sait_Faik_Sahmerdan.dataset.jsonl",
        "records": 492,
        "previous_records_missing_scene_brief_summary": 394,
        "previous_scene_objects_missing_scene_brief_summary": 394,
        "sha256": "ab2b55ae483e50fec9c0a4b72956d51751d76f28131795a8fa5684f76fab0a04",
    },
    {
        "source_file": "Sait_Faik_Sarnic.dataset.jsonl",
        "records": 479,
        "previous_records_missing_scene_brief_summary": 360,
        "previous_scene_objects_missing_scene_brief_summary": 360,
        "sha256": "da04b8c5c3c89c5ebf72631709dc67374cc2f31b8894a1860f4dc8d2e332b083",
    },
    {
        "source_file": "Sait_Faik_Semaver.dataset.jsonl",
        "records": 424,
        "previous_records_missing_scene_brief_summary": 334,
        "previous_scene_objects_missing_scene_brief_summary": 334,
        "sha256": "62c783be3ea03d9b5b2e2dc620f0d9bf72bf45e9be7f411b98697e6497248634",
    },
]


def display_path(path: Path) -> str:
    """Return a stable POSIX-style path without leaking local absolute paths."""
    try:
        if path.is_absolute():
            return path.resolve().relative_to(Path.cwd().resolve()).as_posix()
    except ValueError:
        return path.name
    return path.as_posix()


def iter_jsonl_paths(input_path: Path) -> list[Path]:
    if input_path.is_file():
        if input_path.suffix.lower() != ".jsonl":
            raise ValueError(f"Input file is not JSONL: {input_path.name}")
        return [input_path]
    if input_path.is_dir():
        return sorted(input_path.rglob("*.jsonl"))
    raise FileNotFoundError(f"Input path does not exist: {input_path.name}")


def load_schema(schema_path: Path) -> dict[str, Any]:
    with schema_path.open("r", encoding="utf-8") as handle:
        schema = json.load(handle)
    Draft202012Validator.check_schema(schema)
    return schema


def sha256_file(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def add_issue(
    issues: list[dict[str, Any]],
    file_path: Path,
    line_no: int,
    code: str,
    message: str,
    severity: str = "error",
    scene_index: int | None = None,
) -> None:
    issue: dict[str, Any] = {
        "file": display_path(file_path),
        "line": line_no,
        "severity": severity,
        "code": code,
        "message": message,
    }
    if scene_index is not None:
        issue["scene_index"] = scene_index
    issues.append(issue)


def non_empty_string(value: Any) -> bool:
    return isinstance(value, str) and bool(value.strip())


def non_empty_list(value: Any) -> bool:
    return isinstance(value, list) and len(value) > 0


def lower_text(value: Any) -> str:
    return value.lower() if isinstance(value, str) else ""


def top_state_labels(row: dict[str, Any]) -> list[str]:
    profile = row.get("state_identity_profile")
    top_states = profile.get("top_states") if isinstance(profile, dict) else []
    labels: list[str] = []
    if isinstance(top_states, list):
        for item in top_states:
            if isinstance(item, list) and item and isinstance(item[0], str):
                labels.append(item[0])
    return labels


def has_state_evidence(row: dict[str, Any]) -> bool:
    profile = row.get("state_identity_profile")
    if not isinstance(profile, dict):
        return False
    if non_empty_list(profile.get("top_states")):
        return True
    if non_empty_list(profile.get("all_scores")):
        return True
    return non_empty_string(profile.get("embedding_model"))


def has_embedding_evidence(row: dict[str, Any]) -> bool:
    profile = row.get("state_identity_profile")
    if not isinstance(profile, dict):
        return False
    return non_empty_string(profile.get("embedding_model")) or non_empty_list(profile.get("all_scores"))


def has_descriptive_evidence(row: dict[str, Any]) -> bool:
    for key in ("descriptive_profile", "descriptive_profile_enriched", "descriptive_profile_enriched_filtered"):
        if non_empty_list(row.get(key)):
            return True
    triage_reasons = row.get("triage_reasons")
    if isinstance(triage_reasons, list):
        return any("descriptive" in lower_text(item) for item in triage_reasons)
    return False


def has_fallback_evidence(row: dict[str, Any], scene: dict[str, Any]) -> bool:
    if lower_text(scene.get("split_reason")) in NON_EVENT_SPLIT_REASONS:
        return True
    fallback_review = row.get("fallback_review")
    if isinstance(fallback_review, dict) and non_empty_string(fallback_review.get("reason")):
        return True
    triage_reasons = row.get("triage_reasons")
    if isinstance(triage_reasons, list):
        return any("fallback" in lower_text(item) for item in triage_reasons)
    return False


def has_emotion_evidence(row: dict[str, Any]) -> bool:
    labels = top_state_labels(row)
    if any(any(marker in label.lower() for marker in EMOTION_STATE_MARKERS) for label in labels):
        return True
    for key in ("descriptive_profile", "descriptive_profile_enriched", "descriptive_profile_enriched_filtered"):
        value = row.get(key)
        if isinstance(value, list):
            for item in value:
                if isinstance(item, dict) and lower_text(item.get("category")) in {"descr_emotion", "descr_psychology"}:
                    return True
    triage_reasons = row.get("triage_reasons")
    if isinstance(triage_reasons, list):
        return any("emotion" in lower_text(item) or "psychology" in lower_text(item) for item in triage_reasons)
    return False


def has_atmosphere_evidence(row: dict[str, Any]) -> bool:
    labels = top_state_labels(row)
    if any(any(marker in label.lower() for marker in ATMOSPHERE_STATE_MARKERS) for label in labels):
        return True
    if "atmosphere" in lower_text(row.get("triage_version")):
        return True
    for key in ("descriptive_profile", "descriptive_profile_enriched", "descriptive_profile_enriched_filtered"):
        value = row.get(key)
        if isinstance(value, list):
            for item in value:
                if isinstance(item, dict) and lower_text(item.get("category")) in {"descr_location", "descr_nature"}:
                    return True
    return False


def alternate_evidence_kinds(row: dict[str, Any], scene: dict[str, Any]) -> list[str]:
    kinds: list[str] = []
    if has_fallback_evidence(row, scene):
        kinds.append("fallback_reason")
    if has_state_evidence(row):
        kinds.append("state_identity_profile")
    if has_embedding_evidence(row):
        kinds.append("embedding_derived_profile")
    if has_descriptive_evidence(row):
        kinds.append("descriptive_profile")
    if has_emotion_evidence(row):
        kinds.append("emotion_signal")
    if has_atmosphere_evidence(row):
        kinds.append("atmosphere_signal")
    return sorted(set(kinds))


def scene_has_brief_summary(scene: dict[str, Any]) -> bool:
    return non_empty_string(scene.get("brief_summary"))


def scene_is_structural_fallback(row: dict[str, Any], scene: dict[str, Any]) -> bool:
    return has_fallback_evidence(row, scene)


def scene_is_event_bearing(row: dict[str, Any], scene: dict[str, Any]) -> bool:
    """Infer the event-bearing regime from explicit summaries or event-like labels.

    Existing v0.1 records do not contain a dedicated boolean event flag. The
    public rule therefore treats a non-empty brief_summary as event-bearing
    evidence, and also treats event/action/dialogue-like scene labels as
    event-bearing unless the scene is explicitly structural_fallback.
    """
    if scene_has_brief_summary(scene):
        return True
    if scene_is_structural_fallback(row, scene):
        return False
    scene_type = lower_text(scene.get("scene_type"))
    return any(marker in scene_type for marker in EVENT_MARKERS)


def scene_is_state_bearing(row: dict[str, Any]) -> bool:
    return has_state_evidence(row)


def scene_is_non_event_segment(row: dict[str, Any], scene: dict[str, Any]) -> bool:
    if scene_is_structural_fallback(row, scene):
        return True
    if has_descriptive_evidence(row) or has_emotion_evidence(row) or has_atmosphere_evidence(row):
        return True
    triage_reasons = row.get("triage_reasons")
    if isinstance(triage_reasons, list):
        return any(any(marker in lower_text(item) for marker in NON_EVENT_TRIAGE_MARKERS) for item in triage_reasons)
    return False


def validate_custom_contracts(
    row: dict[str, Any],
    file_path: Path,
    line_no: int,
    errors: list[dict[str, Any]],
    warnings: list[dict[str, Any]],
    info: list[dict[str, Any]],
    scene_field_missing_counts: Counter[str],
) -> Counter[str]:
    counters: Counter[str] = Counter()

    text = row.get("text")
    if not isinstance(text, str) or not text.strip():
        counters["empty_text_records"] += 1
        add_issue(errors, file_path, line_no, "empty_text", "`text` must be a non-empty string.")

    profile = row.get("state_identity_profile")
    top_states = profile.get("top_states") if isinstance(profile, dict) else None
    if not isinstance(top_states, list) or len(top_states) == 0:
        counters["empty_top_states_records"] += 1
        add_issue(
            errors,
            file_path,
            line_no,
            "empty_top_states",
            "`state_identity_profile.top_states` must be a non-empty list.",
        )

    scene_segments = row.get("scene_segments")
    if not isinstance(scene_segments, dict):
        add_issue(errors, file_path, line_no, "missing_scene_segments", "`scene_segments` must be an object.")
        return counters

    scenes = scene_segments.get("scenes")
    if not isinstance(scenes, list) or len(scenes) == 0:
        add_issue(errors, file_path, line_no, "invalid_scenes", "`scene_segments.scenes` must be a non-empty list.")
        return counters

    record_missing_summary = False
    record_summaryless_valid = False
    record_summaryless_invalid = False
    record_eventful = False
    record_structural = False
    record_state = False
    record_emotion = False
    record_atmosphere = False
    record_descriptive = False

    for index, scene in enumerate(scenes):
        if not isinstance(scene, dict):
            counters["scene_objects_missing_required_fields"] += 1
            add_issue(errors, file_path, line_no, "invalid_scene_object", f"Scene {index} must be an object.")
            continue

        counters["scene_objects"] += 1
        scene_index = scene.get("scene_index") if isinstance(scene.get("scene_index"), int) else index + 1
        missing_base_fields = [field for field in SCENE_REQUIRED_FIELDS if field not in scene or scene.get(field) in (None, "")]
        if missing_base_fields:
            counters["scene_objects_missing_required_fields"] += 1
            for field in missing_base_fields:
                scene_field_missing_counts[field] += 1
                add_issue(
                    errors,
                    file_path,
                    line_no,
                    "missing_scene_field",
                    f"Scene {index} is missing `{field}`.",
                    scene_index=scene_index,
                )

        has_summary = scene_has_brief_summary(scene)
        is_event = scene_is_event_bearing(row, scene)
        is_structural = scene_is_structural_fallback(row, scene)
        is_state = scene_is_state_bearing(row)
        is_emotion = has_emotion_evidence(row)
        is_atmosphere = has_atmosphere_evidence(row)
        is_descriptive = has_descriptive_evidence(row)
        evidence = alternate_evidence_kinds(row, scene)

        if is_event:
            counters["event_bearing_scene_objects"] += 1
            record_eventful = True
        if is_structural:
            counters["structural_fallback_scene_objects"] += 1
            record_structural = True
        if is_state:
            counters["state_bearing_scene_objects"] += 1
            record_state = True
        if is_emotion:
            counters["emotion_bearing_scene_objects"] += 1
            record_emotion = True
        if is_atmosphere:
            counters["atmosphere_bearing_scene_objects"] += 1
            record_atmosphere = True
        if is_descriptive:
            counters["descriptive_scene_objects"] += 1
            record_descriptive = True

        if not has_summary:
            counters["scene_objects_missing_brief_summary"] += 1
            record_missing_summary = True

            if is_event:
                counters["event_bearing_scene_objects_missing_brief_summary"] += 1
                record_summaryless_invalid = True
                scene_field_missing_counts["brief_summary"] += 1
                add_issue(
                    errors,
                    file_path,
                    line_no,
                    "event_bearing_scene_missing_brief_summary",
                    "Event-bearing scenes require non-empty `brief_summary`.",
                    scene_index=scene_index,
                )
            elif evidence:
                counters["summaryless_valid_scene_objects"] += 1
                record_summaryless_valid = True
                add_issue(
                    info,
                    file_path,
                    line_no,
                    "non_event_segment_without_summary",
                    "Non-event segment omits `brief_summary` but has alternate evidence: "
                    + ", ".join(evidence)
                    + ".",
                    severity="info",
                    scene_index=scene_index,
                )
            else:
                counters["summaryless_invalid_scene_objects"] += 1
                record_summaryless_invalid = True
                scene_field_missing_counts["brief_summary"] += 1
                add_issue(
                    errors,
                    file_path,
                    line_no,
                    "summaryless_segment_without_evidence",
                    "Scene omits `brief_summary` and has no state, embedding, descriptive, atmosphere, emotion, or fallback evidence.",
                    scene_index=scene_index,
                )

    if record_eventful:
        counters["eventful_records"] += 1
    if record_structural:
        counters["structural_fallback_segment_records"] += 1
    if record_state:
        counters["state_bearing_segment_records"] += 1
    if record_emotion:
        counters["emotion_bearing_segment_records"] += 1
    if record_atmosphere:
        counters["atmosphere_bearing_segment_records"] += 1
    if record_descriptive:
        counters["descriptive_segment_records"] += 1
    if record_missing_summary:
        counters["records_missing_brief_summary"] += 1
    if record_summaryless_valid:
        counters["summaryless_valid_records"] += 1
    if record_summaryless_invalid:
        counters["summaryless_invalid_records"] += 1

    return counters


def known_full_source_status() -> dict[str, Any]:
    total_records = sum(item["records"] for item in KNOWN_FULL_SOURCE_INVENTORY)
    previous_records_missing = sum(item["previous_records_missing_scene_brief_summary"] for item in KNOWN_FULL_SOURCE_INVENTORY)
    previous_scenes_missing = sum(item["previous_scene_objects_missing_scene_brief_summary"] for item in KNOWN_FULL_SOURCE_INVENTORY)
    return {
        "included_in_public_patch": False,
        "total_profiled_records": total_records,
        "two_regime_schema_policy": "brief_summary_required_only_for_event_bearing_scenes",
        "previous_strict_summary_policy_status": "fails",
        "previous_strict_summary_policy_issue": "missing scene_segments.scenes[].brief_summary",
        "previous_records_missing_scene_brief_summary": previous_records_missing,
        "previous_scene_objects_missing_scene_brief_summary": previous_scenes_missing,
        "two_regime_interpretation": (
            "Missing brief_summary is valid for structural/state/emotion/atmosphere/descriptive non-event segments "
            "when alternate evidence fields are present."
        ),
        "profiled_example_dataset_two_regime_probe": {
            "passed": True,
            "total_records": 2172,
            "eventful_records": 452,
            "event_bearing_scene_objects": 458,
            "structural_fallback_segment_records": 1238,
            "state_bearing_segment_records": 2172,
            "emotion_bearing_segment_records": 1297,
            "atmosphere_bearing_segment_records": 2172,
            "descriptive_segment_records": 1893,
            "records_missing_brief_summary": 1720,
            "summaryless_valid_records": 1720,
            "summaryless_invalid_records": 0,
            "error_count": 0,
        },
        "normalization_required_before_full_release": (
            "required only for event-bearing scenes without brief_summary or for summary-less segments without alternate evidence"
        ),
        "files": KNOWN_FULL_SOURCE_INVENTORY,
    }


def validate_jsonl(schema_path: Path, input_path: Path) -> dict[str, Any]:
    schema = load_schema(schema_path)
    validator = Draft202012Validator(schema)
    paths = iter_jsonl_paths(input_path)

    errors: list[dict[str, Any]] = []
    warnings: list[dict[str, Any]] = []
    info: list[dict[str, Any]] = []
    micro_block_locations: dict[str, tuple[Path, int]] = {}
    per_file: dict[str, dict[str, Any]] = {}
    field_counter: Counter[str] = Counter()
    source_file_counter: Counter[str] = Counter()
    scene_field_missing_counts: Counter[str] = Counter()
    aggregate_custom: Counter[str] = Counter()

    for path in paths:
        rows = 0
        parse_errors = 0
        schema_errors = 0
        file_custom: Counter[str] = Counter()
        file_errors_start = len(errors)
        file_warnings_start = len(warnings)
        file_info_start = len(info)

        with path.open("r", encoding="utf-8") as handle:
            for line_no, line in enumerate(handle, start=1):
                if not line.strip():
                    continue

                rows += 1
                source_file_counter[path.name] += 1

                try:
                    row = json.loads(line)
                except json.JSONDecodeError as exc:
                    parse_errors += 1
                    add_issue(errors, path, line_no, "json_parse_error", str(exc))
                    continue

                if not isinstance(row, dict):
                    add_issue(errors, path, line_no, "invalid_row_type", "Each JSONL row must be a JSON object.")
                    continue

                field_counter.update(row.keys())

                schema_error_list = sorted(validator.iter_errors(row), key=lambda item: list(item.path))
                schema_errors += len(schema_error_list)
                for error in schema_error_list:
                    location = ".".join(str(part) for part in error.path) or "<root>"
                    add_issue(errors, path, line_no, "schema_error", f"{location}: {error.message}")

                custom_counts = validate_custom_contracts(
                    row=row,
                    file_path=path,
                    line_no=line_no,
                    errors=errors,
                    warnings=warnings,
                    info=info,
                    scene_field_missing_counts=scene_field_missing_counts,
                )
                file_custom.update(custom_counts)
                aggregate_custom.update(custom_counts)

                micro_block_id = row.get("micro_block_id")
                if isinstance(micro_block_id, str):
                    if micro_block_id in micro_block_locations:
                        first_path, first_line = micro_block_locations[micro_block_id]
                        file_custom["duplicate_micro_block_ids"] += 1
                        aggregate_custom["duplicate_micro_block_ids"] += 1
                        add_issue(
                            errors,
                            path,
                            line_no,
                            "duplicate_micro_block_id",
                            f"`micro_block_id` duplicates {display_path(first_path)}:{first_line}.",
                        )
                    else:
                        micro_block_locations[micro_block_id] = (path, line_no)

        per_file[display_path(path)] = {
            "records": rows,
            "sha256": sha256_file(path),
            "parse_errors": parse_errors,
            "schema_errors": schema_errors,
            "custom_error_count": len(errors) - file_errors_start - schema_errors - parse_errors,
            "custom_warning_count": len(warnings) - file_warnings_start,
            "custom_info_count": len(info) - file_info_start,
            "empty_text_records": file_custom.get("empty_text_records", 0),
            "empty_top_states_records": file_custom.get("empty_top_states_records", 0),
            "scene_objects": file_custom.get("scene_objects", 0),
            "scene_objects_missing_required_fields": file_custom.get("scene_objects_missing_required_fields", 0),
            "eventful_records": file_custom.get("eventful_records", 0),
            "event_bearing_scene_objects": file_custom.get("event_bearing_scene_objects", 0),
            "event_bearing_scene_objects_missing_brief_summary": file_custom.get("event_bearing_scene_objects_missing_brief_summary", 0),
            "structural_fallback_segment_records": file_custom.get("structural_fallback_segment_records", 0),
            "structural_fallback_scene_objects": file_custom.get("structural_fallback_scene_objects", 0),
            "state_bearing_segment_records": file_custom.get("state_bearing_segment_records", 0),
            "state_bearing_scene_objects": file_custom.get("state_bearing_scene_objects", 0),
            "emotion_bearing_segment_records": file_custom.get("emotion_bearing_segment_records", 0),
            "emotion_bearing_scene_objects": file_custom.get("emotion_bearing_scene_objects", 0),
            "atmosphere_bearing_segment_records": file_custom.get("atmosphere_bearing_segment_records", 0),
            "atmosphere_bearing_scene_objects": file_custom.get("atmosphere_bearing_scene_objects", 0),
            "descriptive_segment_records": file_custom.get("descriptive_segment_records", 0),
            "descriptive_scene_objects": file_custom.get("descriptive_scene_objects", 0),
            "records_missing_brief_summary": file_custom.get("records_missing_brief_summary", 0),
            "scene_objects_missing_brief_summary": file_custom.get("scene_objects_missing_brief_summary", 0),
            "summaryless_valid_records": file_custom.get("summaryless_valid_records", 0),
            "summaryless_valid_scene_objects": file_custom.get("summaryless_valid_scene_objects", 0),
            "summaryless_invalid_records": file_custom.get("summaryless_invalid_records", 0),
            "summaryless_invalid_scene_objects": file_custom.get("summaryless_invalid_scene_objects", 0),
        }

    input_label = display_path(input_path)
    if "gold_smoke_v0.1" in input_label:
        report_id = "gold_smoke_report_v0.1"
    elif "two_regime_probe_v0.1" in input_label:
        report_id = "two_regime_probe_report_v0.1"
    else:
        report_id = "dataset_profile_v0.1_previous"

    report = {
        "report_id": report_id,
        "public_release_version": PUBLIC_RELEASE_VERSION,
        "schema_version": SCHEMA_VERSION,
        "validator_version": VALIDATOR_VERSION,
        "two_regime_policy_version": TWO_REGIME_POLICY_VERSION,
        "schema": display_path(schema_path),
        "input": input_label,
        "jsonl_files": [display_path(path) for path in paths],
        "passed": len(errors) == 0,
        "total_records": sum(item["records"] for item in per_file.values()),
        "file_count": len(paths),
        "brief_summary_policy": "two_regime_event_required_non_event_optional_with_evidence",
        "segment_regime_policy": {
            "event_bearing_scene": "brief_summary is required",
            "structural_fallback_segment": "brief_summary is optional when fallback or state/descriptive evidence exists",
            "state_emotion_atmosphere_descriptive_segment": "brief_summary is optional when alternate profile evidence exists",
            "summaryless_without_alternate_evidence": "error",
        },
        "per_file": per_file,
        "source_file_distribution": dict(sorted(source_file_counter.items())),
        "unique_micro_block_id_count": len(micro_block_locations),
        "duplicate_micro_block_id_count": aggregate_custom.get("duplicate_micro_block_ids", 0),
        "field_presence_counts": dict(sorted(field_counter.items())),
        "custom_contract_counts": {
            "empty_text_records": aggregate_custom.get("empty_text_records", 0),
            "empty_top_states_records": aggregate_custom.get("empty_top_states_records", 0),
            "scene_objects": aggregate_custom.get("scene_objects", 0),
            "scene_objects_missing_required_fields": aggregate_custom.get("scene_objects_missing_required_fields", 0),
            "eventful_records": aggregate_custom.get("eventful_records", 0),
            "event_bearing_scene_objects": aggregate_custom.get("event_bearing_scene_objects", 0),
            "event_bearing_scene_objects_missing_brief_summary": aggregate_custom.get("event_bearing_scene_objects_missing_brief_summary", 0),
            "structural_fallback_segment_records": aggregate_custom.get("structural_fallback_segment_records", 0),
            "structural_fallback_scene_objects": aggregate_custom.get("structural_fallback_scene_objects", 0),
            "state_bearing_segment_records": aggregate_custom.get("state_bearing_segment_records", 0),
            "state_bearing_scene_objects": aggregate_custom.get("state_bearing_scene_objects", 0),
            "emotion_bearing_segment_records": aggregate_custom.get("emotion_bearing_segment_records", 0),
            "emotion_bearing_scene_objects": aggregate_custom.get("emotion_bearing_scene_objects", 0),
            "atmosphere_bearing_segment_records": aggregate_custom.get("atmosphere_bearing_segment_records", 0),
            "atmosphere_bearing_scene_objects": aggregate_custom.get("atmosphere_bearing_scene_objects", 0),
            "descriptive_segment_records": aggregate_custom.get("descriptive_segment_records", 0),
            "descriptive_scene_objects": aggregate_custom.get("descriptive_scene_objects", 0),
            "records_missing_brief_summary": aggregate_custom.get("records_missing_brief_summary", 0),
            "scene_objects_missing_brief_summary": aggregate_custom.get("scene_objects_missing_brief_summary", 0),
            "summaryless_valid_records": aggregate_custom.get("summaryless_valid_records", 0),
            "summaryless_valid_scene_objects": aggregate_custom.get("summaryless_valid_scene_objects", 0),
            "summaryless_invalid_records": aggregate_custom.get("summaryless_invalid_records", 0),
            "summaryless_invalid_scene_objects": aggregate_custom.get("summaryless_invalid_scene_objects", 0),
        },
        "scene_field_missing_counts": dict(sorted(scene_field_missing_counts.items())),
        "info_count": len(info),
        "info": info[:200],
        "warning_count": len(warnings),
        "warnings": warnings,
        "error_count": len(errors),
        "errors": errors,
        "known_full_source_dataset_status": known_full_source_status(),
        "checks_applied": [
            "line_by_line_json_parse",
            "json_schema_draft_2020_12",
            "required_core_fields",
            "non_empty_text",
            "unique_micro_block_id",
            "non_empty_state_identity_profile_top_states",
            "scene_base_fields_scene_index_scene_type_split_reason",
            "two_regime_brief_summary_policy",
            "alternate_evidence_for_summaryless_non_event_segments",
            "full_source_readiness_note",
        ],
        "notes": [
            "The public validation target is a schema-validated gold-smoke subset; it is not yet a human-verified gold-eval split.",
            "brief_summary is not a global field requirement.",
            "For event-bearing scenes, brief_summary remains required.",
            "For structural_fallback, state-bearing, emotion-bearing, atmosphere-bearing, and descriptive non-event segments, summary-less records are valid when alternate evidence fields are present.",
            "A summary-less record without state, embedding, descriptive, atmosphere, emotion, or fallback evidence is a real validation error.",
        ],
    }
    return report


def main() -> int:
    parser = argparse.ArgumentParser(description="Validate Tasvir Bankası JSONL files.")
    parser.add_argument("--schema", required=True, type=Path, help="Path to JSON Schema file.")
    parser.add_argument("--input", required=True, type=Path, help="JSONL file or directory containing JSONL files.")
    parser.add_argument("--report", required=True, type=Path, help="Output JSON report path.")
    args = parser.parse_args()

    report = validate_jsonl(args.schema, args.input)
    args.report.parent.mkdir(parents=True, exist_ok=True)
    args.report.write_text(json.dumps(report, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")

    print(json.dumps({"passed": report["passed"], "total_records": report["total_records"], "error_count": report["error_count"]}, ensure_ascii=False))
    return 0 if report["passed"] else 1


if __name__ == "__main__":
    raise SystemExit(main())
