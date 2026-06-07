# Tasvir Bankası: Turkish Literary Annotation Pipeline

**Tasvir Bankası** is a Turkish literary annotation pipeline for transforming public-domain prose into structured JSONL records that distinguish scene-bearing, state-bearing, dialogue-bearing, tense-bearing, and descriptive-evidence-bearing textual units.

This repository is the **public-safe GitHub release** of the annotation pipeline. It contains pipeline scripts, schemas, validation tools, documentation, source-rights review materials, and limited smoke/probe JSONL samples. It does **not** contain the full gated Hugging Face dataset payload.

Tasvir Bankası is **not** a style bank, author-imitation corpus, or prose-style cloning resource. It treats literary prose not as undifferentiated training text, but as a structured field of narrative functions.

Project owner and citation author: **Furkan Yaşar**.

---

## Public release

GitHub public-preview version: `v0.1.0-public-preview`.

This repository is a pipeline, schema, documentation, and validation-preview package. It is **not** the full dataset release.

The full gated dataset package is released separately as `v0.3.1`.

---

## Scope of this public preview

Included public validation subsets:

- `data/gold_smoke_v0.1/`: 100-record schema-validated gold-smoke subset.
- `data/two_regime_probe_v0.1/`: 20-record companion probe containing both event-bearing scenes and summary-less valid non-event segments.

Neither subset is a human-verified gold-eval benchmark.

The full gated dataset release described by the project contains:

- **2,172 train records**
- **92 label-level curated gold-eval records**
- **98 human curation ledger records**

These full dataset files are **not** distributed through this GitHub repository.

---

## Core pipeline boundary

The core dataset pipeline is the 17-script sequence defined in `RUN_ORDER.md` and implemented under `pipeline/`.

- Every core stage script is listed in `RUN_ORDER.md`.
- Every script in `pipeline/` belongs to the 17-stage core pipeline.

Pipeline scripts are stage executables, not import-safe library modules. Public release excludes downstream demonstration scripts; every script under `pipeline/` is a core dataset construction stage.

---

## Two-regime validation policy

The public schema and validator enforce a two-regime rule:

- Event-bearing scene: `brief_summary` is required.
- Non-event state/emotion/description/structural-fallback segment: `brief_summary` may be omitted when accepted alternate evidence is present.
- Summary-less segment without alternate evidence: invalid.

---

## GitHub and Hugging Face release boundary

GitHub public preview and Hugging Face full dataset publication are separate release surfaces.

- GitHub public preview: pipeline code, schema, validator, documentation, citation metadata, and release-check subsets.
- Hugging Face dataset package: full gated dataset release, tracked separately as `v0.3.1`.

Do not describe this GitHub repository as containing the full Hugging Face dataset.

---

## Installation

Linux/macOS:

```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

Windows PowerShell:

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
pip install -r requirements.txt
```

---

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

---

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

---

## Citation

Use `CITATION.cff` for this GitHub public-preview package.

Recommended GitHub citation string:

```text
Yaşar, F. (2026). Tasvir Bankası: Turkish Literary Annotation Pipeline (v0.1.0-public-preview). GitHub.
```

For the full dataset publication record, cite the Zenodo DOI once published.

---

## Release boundaries

This public preview excludes the full gated dataset payload and does not mark the Hugging Face full dataset release as contained inside this repository.

---

## Version relationship

Pipeline and dataset versions are tracked separately.

- Public-safe GitHub pipeline package: `v0.1.0-public-preview`.
- Full gated dataset package: `v0.3.1`.

The `v0.3.1` dataset release is not a new pipeline run. It is a publication-ready release derived from the `v0.3` curated package: filename normalization, source-inventory alignment, source-edition metadata recording, label-level gold-eval clarification, limitation-note strengthening, and regenerated manifest/checksum reports.
