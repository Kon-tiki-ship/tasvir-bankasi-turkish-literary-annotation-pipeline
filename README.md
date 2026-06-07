# Tasvir Bankası: Turkish Literary Annotation Pipeline

[![GitHub release](https://img.shields.io/badge/release-v0.1.1--public--preview-blue)](https://github.com/Kon-tiki-ship/tasvir-bankasi-turkish-literary-annotation-pipeline/releases)
[![Dataset](https://img.shields.io/badge/Hugging%20Face-gated%20dataset-yellow)](https://huggingface.co/datasets/Kon-tiki-ship/tasvir-bankasi-turkish-literary-scene-state-description-dataset)
[![DOI](https://img.shields.io/badge/DOI-10.5281%2Fzenodo.20579958-blue)](https://doi.org/10.5281/zenodo.20579958)
[![Data license](https://img.shields.io/badge/data-CC%20BY--NC%204.0-lightgrey)](DATA_LICENSE.md)
[![Code license](https://img.shields.io/badge/code-PolyForm%20Noncommercial%201.0.0-lightgrey)](CODE_LICENSE.md)

**Tasvir Bankası** is a Turkish literary annotation pipeline for transforming rights-reviewed public-domain candidate Turkish prose into structured JSONL records.

It distinguishes:

- scene-bearing textual units,
- state-bearing textual units,
- dialogue-bearing textual units,
- tense-bearing textual units,
- descriptive-evidence-bearing textual units.

This GitHub repository is the **public-safe pipeline release**. It contains pipeline scripts, schemas, validation tools, documentation, source-rights review materials, and limited smoke/probe JSONL samples.

It **does not** contain the full gated Hugging Face dataset payload.

Project owner and citation author: **Furkan Yaşar**.

---

## Quick links

| I want to... | Go to |
|---|---|
| Inspect the public annotation pipeline | This GitHub repository |
| Download the public-preview pipeline release | [GitHub releases](https://github.com/Kon-tiki-ship/tasvir-bankasi-turkish-literary-annotation-pipeline/releases) |
| Access the full gated dataset | [Hugging Face dataset](https://huggingface.co/datasets/Kon-tiki-ship/tasvir-bankasi-turkish-literary-scene-state-description-dataset) |
| Cite the publication dataset | [Zenodo DOI](https://doi.org/10.5281/zenodo.20579958) |
| Check sample JSONL records | `data/gold_smoke_v0.1/` and `data/two_regime_probe_v0.1/` |
| Check the core pipeline order | `RUN_ORDER.md` |
| Inspect the schema | `schemas/tasvir_record_schema.v0.1.json` |
| Run validation | `tests/validate_jsonl_schema.py` |
| Read terms of use | `TERMS_OF_USE.md` |

---

## What this repository is

This repository is:

- a public-safe annotation pipeline package,
- a schema and validation package,
- a reproducibility-review package,
- a limited public-preview sample package,
- a companion release for the full gated Hugging Face dataset.

It is intended for:

- Turkish literary NLP,
- computational narratology,
- digital humanities,
- corpus annotation research,
- non-commercial reproducibility review,
- education and research evaluation.

---

## What this repository is not

Tasvir Bankası is **not**:

- a style bank,
- an author-imitation corpus,
- a prose-style cloning resource,
- a commercial model-training corpus,
- a general-purpose Turkish language model dataset,
- a full benchmark-grade gold corpus,
- a replacement for legal source-rights review.

The project treats literary prose not as undifferentiated training text, but as a structured field of narrative functions.

---

## Public release

GitHub public-preview version:

```text
v0.1.1-public-preview
```

This repository is a pipeline, schema, documentation, and validation-preview package.

The full gated dataset package is released separately as:

```text
v0.3.1
```

The GitHub pipeline package and the Hugging Face dataset package are tracked separately.

---

## Version relationship

| Release surface | Version | Role |
|---|---:|---|
| GitHub public-safe pipeline package | `v0.1.1-public-preview` | Pipeline, schema, validator, documentation, smoke/probe samples |
| Hugging Face full gated dataset package | `v0.3.1` | Full dataset release |
| Zenodo publication record | `10.5281/zenodo.20579958` | Citation and publication manifest record |

The `v0.3.1` dataset release is not a new pipeline run. It is a publication-ready release derived from the `v0.3` curated package through filename normalization, source-inventory alignment, source-edition metadata recording, label-level gold-eval clarification, limitation-note strengthening, and regenerated manifest/checksum reports.

---

## Scope of this public preview

Included public validation subsets:

```text
data/gold_smoke_v0.1/
data/two_regime_probe_v0.1/
```

| Public subset | Description |
|---|---|
| `data/gold_smoke_v0.1/` | 100-record schema-validated gold-smoke subset |
| `data/two_regime_probe_v0.1/` | 20-record companion probe containing both event-bearing scenes and summary-less valid non-event segments |

Neither subset is a human-verified full gold-eval benchmark.

The full gated dataset release described by the project contains:

```text
train_record_count: 2172
curated_gold_eval_v0.3_count: 92
curation_ledger_v0.3_count: 98
pending_queue_count: 0
```

These full dataset files are **not** distributed through this GitHub repository.

---

## Related resources

Full gated Hugging Face dataset release:

```text
https://huggingface.co/datasets/Kon-tiki-ship/tasvir-bankasi-turkish-literary-scene-state-description-dataset
```

Zenodo publication record and DOI:

```text
https://doi.org/10.5281/zenodo.20579958
```

GitHub public-preview releases:

```text
https://github.com/Kon-tiki-ship/tasvir-bankasi-turkish-literary-annotation-pipeline/releases
```

---

## Repository layout

```text
.
├── data/
│   ├── gold_smoke_v0.1/
│   ├── two_regime_probe_v0.1/
│   └── reports/
├── docs/
├── pipeline/
├── schemas/
│   └── tasvir_record_schema.v0.1.json
├── tests/
│   └── validate_jsonl_schema.py
├── tools/
├── CITATION.cff
├── CODE_LICENSE.md
├── DATA_LICENSE.md
├── LICENSE
├── LICENSE.md
├── PATCH_MANIFEST.md
├── README.md
├── RUN_ORDER.md
├── TERMS_OF_USE.md
└── requirements.txt
```

---

## Dataset concept

Tasvir Bankası models Turkish literary prose as structured narrative data.

A literary text unit may carry different kinds of evidence:

| Layer | Purpose |
|---|---|
| Scene segmentation | Identifies scene-bearing or scene-adjacent units |
| Scene source / edge metadata | Tracks scene provenance and boundary behavior |
| State identity profile | Marks state-bearing, emotion-bearing, or non-event textual units |
| Descriptive profile | Captures description-bearing textual units |
| Enriched descriptive evidence | Adds filtered descriptive-evidence signals |
| Dialogue | Marks dialogue-bearing or speech-related signals |
| Tense | Records tense-bearing properties |
| Morphology | Preserves morphology-oriented features |
| Selection metadata | Tracks validation, split, and selection information |

Representative field families include:

```text
scene_segments
scene_source
scene_edge
state_identity_profile
descriptive_profile
descriptive_profile_enriched
descriptive_profile_enriched_filtered
dialogue
tense
morphology
selection_metadata
```

---

## Example JSONL record shape

The following is a simplified illustrative shape. It is not a full schema replacement.

```json
{
  "record_id": "tb_preview_0001",
  "source_id": "public_domain_candidate_source",
  "text_unit": "Example Turkish literary prose unit...",
  "scene_segments": {
    "is_scene_bearing": true,
    "scene_boundary": "stable"
  },
  "dialogue": {
    "has_dialogue": false
  },
  "tense": {
    "dominant_tense": "past"
  },
  "morphology": {
    "has_finite_verb": true
  },
  "descriptive_profile": {
    "has_descriptive_evidence": true,
    "description_type": [
      "space",
      "atmosphere"
    ]
  },
  "state_identity_profile": {
    "is_state_bearing": true
  },
  "selection_metadata": {
    "split": "public_preview",
    "validation_status": "schema_validated"
  }
}
```

For the authoritative structure, inspect:

```text
schemas/tasvir_record_schema.v0.1.json
```

---

## Pipeline overview

The core dataset pipeline is the 17-script sequence defined in:

```text
RUN_ORDER.md
```

and implemented under:

```text
pipeline/
```

Pipeline boundary:

- Every core stage script is listed in `RUN_ORDER.md`.
- Every script in `pipeline/` belongs to the 17-stage core pipeline.
- Pipeline scripts are stage executables, not import-safe library modules.
- Public release excludes downstream demonstration scripts.
- Every script under `pipeline/` is a core dataset construction stage.

Simplified flow:

```text
Rights-reviewed Turkish literary prose
        |
        v
Text-unit preparation
        |
        v
Scene / non-scene decision
        |
        +--> dialogue signals
        +--> tense / morphology
        +--> state identity
        +--> descriptive evidence
        +--> curation ledger
        |
        v
Schema-validated JSONL records
```

---

## Two-regime validation policy

The public schema and validator enforce a two-regime rule:

| Record type | `brief_summary` policy |
|---|---|
| Event-bearing scene | `brief_summary` is required |
| Non-event state/emotion/description/structural-fallback segment | `brief_summary` may be omitted when accepted alternate evidence is present |
| Summary-less segment without alternate evidence | Invalid |

This policy prevents non-event descriptive or state-bearing literary units from being incorrectly rejected only because they lack conventional event summaries.

---

## Descriptive extraction policy

Descriptive extraction is regression-tested and cleaned against known lexical false-positive families.

Ambiguous edge cases are routed to the curation ledger.

The `descr_metaphor` field should be read as evidence for metaphor, simile, analogy, comparison, or figurative-marker behavior. It should **not** be interpreted as a complete conceptual-metaphor analysis layer.

---

## Curation policy

Records requiring semantic judgment are stored in the curation ledger.

The full gated dataset release includes:

```text
data/curation_ledger/human_review_curation_ledger_v0.3.jsonl
```

The curation ledger preserves curator decisions such as:

```text
resolved_true_metaphor_marker
resolved_removed_false_label
approved_for_gold_eval
```

Current release status:

```text
pending = 0
```

---

## Gold-eval policy

The full gated dataset release includes:

```text
data/gold_eval/curated_gold_eval_v0.3.jsonl
```

This file contains 92 curated records.

It is a **label-level evaluation seed**, not a full-record benchmark-grade gold corpus.

Most records are marked with:

```json
"gold_scope": "single_label_verified"
```

This means that the listed `curation.verified_dimensions` are curator-reviewed.

It does **not** mean that every field of the entire record is verified as a complete benchmark-grade annotation.

---

## GitHub and Hugging Face release boundary

GitHub public preview and Hugging Face full dataset publication are separate release surfaces.

| Surface | Contains | Does not contain |
|---|---|---|
| GitHub public preview | Pipeline code, schema, validator, documentation, citation metadata, release-check subsets | Full gated dataset payload |
| Hugging Face dataset package | Full gated dataset release tracked as `v0.3.1` | GitHub development history |
| Zenodo publication record | DOI and publication manifest record | Full public unrestricted dataset payload |

Do **not** describe this GitHub repository as containing the full Hugging Face dataset.

---

## Source texts and rights status

Source texts are documented as rights-reviewed public-domain candidates under the Turkish death+70 rule.

This release does not constitute a legal determination.

Users are responsible for verifying source and jurisdictional status before reuse.

Modern publisher material, editor notes, introductions, afterwords, footnotes, simplified rewrites, cover matter, and other publisher-specific paratext are excluded from the intended source boundary.

Relevant documentation includes:

```text
docs/SOURCE_TEXT_INVENTORY.md
docs/SOURCE_RIGHTS_REVIEW_TABLE.md
docs/ZENODO_LICENSE_NOTE.md
```

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
{
  "passed": true,
  "total_records": 100,
  "error_count": 0
}
```

Expected two-regime probe summary:

```json
{
  "passed": true,
  "total_records": 20,
  "error_count": 0
}
```

Expected two-regime probe policy checks:

```text
summaryless_valid_records > 0
summaryless_invalid_records = 0
```

Release validation index:

```text
data/reports/release_validation_index_v0.1.json
```

Internal report note:

```text
data/reports/dataset_profile_v0.1.json
```

may exist for backward compatibility but is not the primary public release validation report.

---

## License and permitted use

Tasvir Bankası is released as a source-available non-commercial research release.

This repository is public for:

- research visibility,
- reproducibility review,
- education,
- non-commercial evaluation.

It is not an OSI-approved open-source commercial-use release.

| Component | License |
|---|---|
| Pipeline code | PolyForm Noncommercial License 1.0.0 |
| Dataset records | CC BY-NC 4.0 |
| Derived annotations | CC BY-NC 4.0 |
| Schemas | CC BY-NC 4.0 |
| Reports and documentation | CC BY-NC 4.0 |
| Sample data | CC BY-NC 4.0, unless otherwise noted |
| Commercial use | Not permitted without explicit written permission |

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

```text
LICENSE.md
CODE_LICENSE.md
DATA_LICENSE.md
TERMS_OF_USE.md
```

---

## Citation

Use `CITATION.cff` for this GitHub public-preview package.

Recommended GitHub citation string:

```text
Yaşar, F. (2026). Tasvir Bankası: Turkish Literary Annotation Pipeline (v0.1.1-public-preview). GitHub. https://github.com/Kon-tiki-ship/tasvir-bankasi-turkish-literary-annotation-pipeline
```

For the full dataset publication record, cite the Zenodo DOI:

```text
Yaşar, F. (2026). Tasvir Bankası v0.3.1: A Turkish Literary Scene-State-Description Dataset and Annotation Pipeline. Zenodo. https://doi.org/10.5281/zenodo.20579958
```

BibTeX-style reference:

```bibtex
@dataset{yasar_2026_tasvir_bankasi,
  author       = {Yaşar, Furkan},
  title        = {Tasvir Bankası v0.3.1: A Turkish Literary Scene-State-Description Dataset and Annotation Pipeline},
  year         = {2026},
  publisher    = {Zenodo},
  doi          = {10.5281/zenodo.20579958},
  url          = {https://doi.org/10.5281/zenodo.20579958}
}
```

---

## Known limitations

This release should be read with the following limitations:

- The GitHub repository does not contain the full gated dataset payload.
- Public smoke/probe subsets are for schema inspection and reproducibility review.
- Public subsets are not full human-verified gold-eval benchmarks.
- The full gold-eval file is a label-level evaluation seed, not a full-record benchmark-grade corpus.
- Source-rights documentation is provided for research transparency but does not constitute legal advice.
- The project is a pilot research resource, not a mature community benchmark.
- The annotation schema is designed for Turkish literary prose and should not be assumed to generalize to every genre without review.

---

## Recommended academic framing

Tasvir Bankası should be described as:

```text
a Turkish literary scene-state-description dataset and annotation pipeline for computational narratology and Turkish literary NLP.
```

A more detailed formulation:

```text
Tasvir Bankası provides a structured JSONL-based annotation resource for Turkish literary prose, with layers for scene segmentation, state-bearing textual units, dialogue signals, tense/morphology, and descriptive evidence.
```

Avoid describing it as:

```text
a full benchmark-grade gold corpus
a general Turkish LLM training dataset
a style-cloning resource
an author-imitation dataset
a commercial model-training corpus
```

---

## Contact and permission

For academic questions, citation issues, collaboration proposals, or commercial permission requests, contact the project owner:

```text
Furkan Yaşar
GitHub: https://github.com/Kon-tiki-ship
Hugging Face: https://huggingface.co/Kon-tiki-ship
```

Commercial use requires explicit written permission from the author.

---

## Summary

Tasvir Bankası provides a public-safe research pipeline and companion dataset release for Turkish literary NLP.

The GitHub repository contains:

```text
pipeline + schema + validator + documentation + public smoke/probe samples
```

The full dataset is hosted separately as a gated non-commercial Hugging Face release:

```text
https://huggingface.co/datasets/Kon-tiki-ship/tasvir-bankasi-turkish-literary-scene-state-description-dataset
```

The publication record is citable through Zenodo:

```text
https://doi.org/10.5281/zenodo.20579958
```
