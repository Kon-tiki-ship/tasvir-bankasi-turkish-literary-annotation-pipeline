# Tasvir Bankası: A Turkish Literary Scene-State-Description Dataset and Annotation Pipeline

Tasvir Bankası is not a style bank, author-imitation corpus, or prose-style cloning resource. It is a public-preview dataset engineering pipeline for scene/state/description-aware Turkish literary records.

Project owner and citation author: **Furkan Yaşar**.

## Public release

Public release version: `v0.1.0-public-preview`.

This repository is a pipeline-and-validation package. It is not a full dataset release.

## Scope of this public preview

Included public validation subsets:

- `data/gold_smoke_v0.1/`: 100-record schema-validated gold-smoke subset.
- `data/two_regime_probe_v0.1/`: 20-record companion probe containing both event-bearing scenes and summary-less valid non-event segments.

Neither subset is a human-verified gold-eval benchmark.

## Core pipeline boundary

The core dataset pipeline is the 17-script sequence defined in `RUN_ORDER.md` and implemented under `pipeline/`.

- Every core stage script is listed in `RUN_ORDER.md`.
- Every script in `pipeline/` belongs to the 17-stage core pipeline.

Pipeline scripts are stage executables (pipeline steps), not import-safe library modules. Public release excludes downstream demonstration scripts; every script under `pipeline/` is a core dataset construction stage.

## Two-regime validation policy

The public schema and validator enforce a two-regime rule:

- Event-bearing scene: `brief_summary` is required.
- Non-event state/emotion/description/state/structural-fallback segment: `brief_summary` may be omitted when accepted alternate evidence is present.
- Summary-less segment without alternate evidence: invalid.

## GitHub and Hugging Face release boundary

GitHub public preview and Hugging Face full dataset publication are separate surfaces.

- GitHub public preview: pipeline code, schema, validator, docs, citation metadata, and release-check subsets.
- Hugging Face dataset package: prepared separately as `v0.3.1-publication-polish` in the upload-ready bundle.

This GitHub repository itself is still a pipeline-and-validation public preview. Do not describe the GitHub repository as containing the full Hugging Face dataset.

## Installation

```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

## Validation commands

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

Expected gold-smoke summary:

```json
{"passed": true, "total_records": 100, "error_count": 0}
```

Expected two-regime probe summary:

```json
{"passed": true, "total_records": 20, "error_count": 0}
```

Expected two-regime probe policy checks:

- `summaryless_valid_records > 0`
- `summaryless_invalid_records = 0`

Release validation index:

- `data/reports/release_validation_index_v0.1.json`

Internal report note:

- `data/reports/dataset_profile_v0.1.json` may exist for backward compatibility but is not the primary public release validation report.

## License and permitted use

Tasvir Bankası is released as a **source-available non-commercial research release**.

This repository is public for research visibility, reproducibility review, education, and non-commercial evaluation. It is **not** an OSI-approved open-source commercial-use release.

- Pipeline code is licensed under the **PolyForm Noncommercial License 1.0.0**.
- Dataset records, derived annotations, schemas, reports, documentation, and sample data are licensed under **CC BY-NC 4.0**, unless otherwise noted.
- Commercial use is not permitted without explicit written permission from the author.

Commercial use includes, but is not limited to:

- commercial model training,
- commercial dataset generation,
- resale,
- paid API or SaaS integration,
- integration into paid products,
- commercial text-generation products,
- author-style cloning or imitation services,
- redistribution as part of a commercial dataset package.

See:

- `LICENSE.md`
- `CODE_LICENSE.md`
- `DATA_LICENSE.md`
- `TERMS_OF_USE.md`

## Citation

Use `CITATION.cff`.

Recommended citation string:

```text
Tasvir Bankası v0.1.0-public-preview, Furkan Yaşar.
```

## Release boundaries

This public preview excludes full source dataset packaging and does not mark a Hugging Face full release as complete.


## Version relationship

Pipeline and dataset versions are tracked separately.

- Public-safe pipeline package: `v0.1.0-public-preview`.
- Dataset release package: `v0.3.1-publication-polish`.

The v0.3.1 dataset is not a new pipeline run. It is a publication-polish release derived from the v0.3 curated package: filename normalization, source-inventory alignment, source-edition metadata recording, label-level gold-eval clarification, limitation-note strengthening, and regenerated manifest/checksum reports.
