# Dataset Card Draft

## Dataset summary

Tasvir Bankası is a scene/state/description-aware Turkish literary dataset pipeline. It converts Turkish literary prose into JSONL records containing text, paragraph and micro-block identifiers, dialogue metrics, morphology-derived features, tense features, scene metadata, state identity metadata, and descriptive lexical evidence.

Tasvir Bankası is not a style bank, author-imitation corpus, or prose-style cloning resource.

Project owner and citation author: **Furkan Yaşar**.

## Release version

Public release: `v0.1.0-public-preview`.

This public preview does not publish the full dataset and does not mark the full dataset as ready.

## Public data in this release

The public package includes two small validation subsets:

```text
data/gold_smoke_v0.1/
data/two_regime_probe_v0.1/
```

`data/gold_smoke_v0.1/` contains 100 JSONL records, distributed as 20 records per profiled source file. It is a schema-validated smoke subset for release checks. It is not a human-verified gold-eval split.

`data/two_regime_probe_v0.1/` contains 20 JSONL records, distributed as 4 records per profiled source file. Each source contributes 2 event-bearing records with `brief_summary` and 2 summary-less valid non-event records with alternate evidence.

## Segment model

The dataset has a two-regime segment model.

1. **Event-bearing scenes** require `brief_summary`.
2. **Non-event segments** (state/emotion/description/atmosphere/reflection/structural fallback) may omit `brief_summary` when accepted alternate evidence exists.

`brief_summary` absence is therefore not automatically a dataset error.

## Validation

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

Expected public smoke result:

```json
{"passed": true, "total_records": 100, "error_count": 0}
```

Expected two-regime probe result:

```json
{"passed": true, "total_records": 20, "error_count": 0}
```

Expected two-regime probe policy checks:

- `summaryless_valid_records > 0`
- `summaryless_invalid_records = 0`

Release validation index:

```text
data/reports/release_validation_index_v0.1.json
```

Internal report note:

```text
data/reports/dataset_profile_v0.1.json may exist for backward compatibility; it is not the primary public release validation report.
```

## Full source dataset readiness

The profiled full example inventory contains 2,172 records. The full source dataset is not included in this public preview.

Full dataset publication still requires:

- full candidate validation on the exact release package;
- exact source-edition review;
- source-text rights review;
- final validation report from exact package contents;
- final data-license decision;
- NotebookLM-assisted gold-eval review;
- human curator approval;
- release-specific packaging review;
- finalized Hugging Face dataset card.

## Source inventory and rights-review status

See:

```text
docs/SOURCE_TEXT_INVENTORY.md
docs/SOURCE_RIGHTS_REVIEW_TABLE.md
docs/HUGGINGFACE_PRE_RELEASE_CHECKLIST.md
data/reports/source_rights_review_v0.1.json
data/reports/hf_pre_release_checklist_v0.1.json
```

Current status label:

```text
rights-reviewed public-domain candidate under Turkish death+70 rule
```

This status is not legal advice and not a final legal determination.

## Data licensing and rights

See `DATA_LICENSE.md`.

Summary:

- Pipeline code/scripts/tests: PolyForm Noncommercial License 1.0.0 (`CODE_LICENSE.md`). Dataset records, derived annotations, schemas, reports, documentation, and sample data: CC BY-NC 4.0 + `TERMS_OF_USE.md`.
- Public validation subset annotations and metadata: CC BY 4.0.
- Underlying literary source text is not relicensed by this repository.
- Full dataset publication remains blocked until rights review and final release packaging are complete.

## Citation

Use `CITATION.cff`.

Recommended citation string:

```text
Tasvir Bankası v0.1.0-public-preview, Furkan Yaşar.
```


## Version relationship

Pipeline and dataset versions are tracked separately.

- Public-safe pipeline package: `v0.1.0-public-preview`.
- Dataset release package: `v0.3.1-publication-polish`.

The v0.3.1 dataset is not a new pipeline run. It is a publication-polish release derived from the v0.3 curated package: filename normalization, source-inventory alignment, source-edition metadata recording, label-level gold-eval clarification, limitation-note strengthening, and regenerated manifest/checksum reports.
