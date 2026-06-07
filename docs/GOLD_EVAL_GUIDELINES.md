# Gold-Smoke and Two-Regime Release Check Guidelines

`data/gold_smoke_v0.1/` is a small schema-validated smoke subset for release testing. It is not a human-verified gold-eval split.

`data/two_regime_probe_v0.1/` is a companion release-check subset used to verify that the two-regime validator accepts summary-less non-event segments when alternate evidence is present.

## Gold-smoke composition

- Total records: 100
- Source files profiled: 5
- Records per source file: 20
- Format: JSONL
- Row rule: one independent JSON object per line

## Two-regime probe composition

- Total records: 20
- Source files profiled: 5
- Records per source file: 4
- Per-source composition: 2 event-bearing records with `brief_summary`, 2 summary-less valid non-event records with alternate evidence
- Format: JSONL
- Row rule: one independent JSON object per line

## Intended checks

Use the subsets to verify that:

1. JSONL rows parse line by line.
2. Required core fields are present.
3. Field types match `schemas/tasvir_record_schema.v0.1.json`.
4. `text` is non-empty.
5. `micro_block_id` values are unique across the validated collection.
6. `state_identity_profile.top_states` is non-empty.
7. Each scene object contains `scene_index`, `scene_type`, and `split_reason`.
8. `brief_summary` is present for event-bearing scenes.
9. Summary-less non-event segments have alternate state, embedding, descriptive, atmosphere, emotion, or fallback evidence.
10. Summary-less segments without alternate evidence are treated as errors.

## Two-regime validation

A missing `brief_summary` is not automatically an error. It becomes an error only when the scene is event-bearing or when the record lacks alternate non-event evidence.

The validator reports:

- `eventful_records`
- `event_bearing_scene_objects`
- `structural_fallback_segment_records`
- `state_bearing_segment_records`
- `emotion_bearing_segment_records`
- `atmosphere_bearing_segment_records`
- `descriptive_segment_records`
- `summaryless_valid_records`
- `summaryless_invalid_records`

## Full dataset status

The full profiled example inventory contains 2,172 records. Under the previous strict summary-only rule, 1,720 records were missing `scene_segments.scenes[].brief_summary`. Under the corrected two-regime validator, those summary-less records are valid when alternate evidence exists. A full dataset release still requires source-text rights review and a final release report.

## Non-goals

The smoke and probe subsets are not intended to measure model quality, genre coverage, author coverage, or full data distribution. They are intentionally small so that installation and validation can run quickly.

## Validation commands

Run from the repository root.

Gold-smoke subset:

```bash
python tests/validate_jsonl_schema.py \
  --schema schemas/tasvir_record_schema.v0.1.json \
  --input data/gold_smoke_v0.1 \
  --report data/reports/gold_smoke_report_v0.1.json
```

Two-regime probe:

```bash
python tests/validate_jsonl_schema.py \
  --schema schemas/tasvir_record_schema.v0.1.json \
  --input data/two_regime_probe_v0.1 \
  --report data/reports/two_regime_probe_report_v0.1.json
```

A valid gold-smoke subset should produce `passed: true`, `total_records: 100`, and `error_count: 0`.

A valid two-regime probe should produce `passed: true`, `total_records: 20`, `summaryless_valid_records > 0`, and `summaryless_invalid_records = 0`.

## Promotion to human-verified gold-eval

A future human-verified gold-eval split must be created through a separate annotation and adjudication process. At minimum, that process should include:

- human review of scene boundaries;
- human review of event-bearing `brief_summary` values;
- human review of non-event summary-less segment evidence;
- human review of `split_reason`;
- duplicate ID checks;
- source-text rights verification;
- NotebookLM-assisted review pass for edge-case consistency;
- human curator approval before publication;
- a new report version under `data/reports/`.
