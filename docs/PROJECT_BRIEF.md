# Tasvir Bankası: Project Brief

**Project:** Tasvir Bankası  
**Release context:** Turkish literary scene-state-description dataset and annotation pipeline  
**Author:** Furkan Yaşar  
**Primary surfaces:** GitHub public-preview pipeline package, Hugging Face gated dataset package, Zenodo publication record  
**Primary field:** Turkish literary NLP, computational narratology, digital humanities, corpus annotation

---

## 1. One-paragraph summary

Tasvir Bankası is a Turkish literary annotation project that transforms rights-reviewed public-domain candidate Turkish prose into structured JSONL records. Instead of treating literary prose as undifferentiated raw text, the project models it as a layered field of narrative evidence. The annotation design distinguishes scene-bearing, state-bearing, dialogue-bearing, tense-bearing, morphology-bearing, and descriptive-evidence-bearing textual units. The full dataset is distributed as a gated non-commercial Hugging Face release, while the GitHub repository provides the public-safe annotation pipeline, schemas, validation tools, documentation, and limited smoke/probe samples.

---

## 2. Research motivation

Most Turkish NLP resources focus on general language modeling, syntactic annotation, named entity recognition, sentiment classification, or task-specific corpora. Literary prose, however, requires a different kind of representation. A literary passage may not simply express an event; it may also establish atmosphere, describe a place, mark a psychological state, shift narrative time, carry indirect dialogue, or prepare a later narrative function.

Tasvir Bankası addresses this gap by proposing a scene-state-description centered annotation model for Turkish literary prose. The project is especially relevant for research questions where raw text, token frequency, or document-level metadata are insufficient.

---

## 3. Core contribution

Tasvir Bankası contributes three linked research objects:

1. **A structured dataset concept** for Turkish literary prose.
2. **A public-safe annotation pipeline** for constructing and validating JSONL records.
3. **A reproducibility-oriented documentation package** that separates the GitHub pipeline package, the Hugging Face dataset package, and the Zenodo citation record.

The central contribution is not simply the collection of Turkish literary text. The central contribution is the transformation of literary prose into layered narrative data.

---

## 4. Annotation layers

The project distinguishes several kinds of textual evidence:

| Layer | Function |
|---|---|
| Scene segmentation | Identifies scene-bearing or scene-adjacent textual units |
| Scene source and edge metadata | Tracks provenance, boundary behavior, and scene transitions |
| State identity profile | Captures state-bearing, emotion-bearing, or non-event textual units |
| Descriptive profile | Marks description-bearing textual evidence |
| Enriched descriptive profile | Adds filtered descriptive-evidence signals |
| Dialogue | Marks dialogue-bearing or speech-related signals |
| Tense | Records tense-bearing properties |
| Morphology | Preserves morphology-oriented evidence |
| Selection metadata | Tracks split, validation, and selection status |
| Curation ledger | Records human review decisions and ambiguous cases |

---

## 5. Why this matters for Turkish literary NLP

Turkish literary prose presents several annotation challenges:

- frequent implicit subjects,
- complex tense and aspect behavior,
- rich morphology,
- indirect or embedded speech,
- descriptive passages without explicit events,
- state-bearing passages that lack conventional event summaries,
- scene boundaries that do not always align with paragraphs,
- literary ambiguity around metaphor, atmosphere, and psychological description.

A scene-state-description dataset makes these phenomena available for computational analysis.

---

## 6. Example research uses

Tasvir Bankası can support exploratory work on:

- scene-bearing versus non-scene classification,
- dialogue-bearing detection,
- descriptive-evidence detection,
- event-bearing versus state-bearing distinction,
- tense and morphology distribution in literary prose,
- literary scene segmentation,
- computational narratology for Turkish prose,
- digital humanities workflows for structured literary corpora,
- annotation schema design for non-English literary NLP.

---

## 7. Release boundary

The project intentionally separates release surfaces:

| Surface | Role |
|---|---|
| GitHub public-preview package | Pipeline, schema, validator, documentation, limited smoke/probe samples |
| Hugging Face gated dataset | Full non-commercial dataset package |
| Zenodo record | DOI-backed publication and citation surface |

The GitHub repository should not be described as containing the full Hugging Face dataset payload.

---

## 8. Current status

The project should be described as a pilot research resource and annotation pipeline, not as a mature community benchmark.

Recommended phrasing:

> Tasvir Bankası is a Turkish literary scene-state-description dataset and annotation pipeline for computational narratology and Turkish literary NLP.

Avoid describing it as:

- a full benchmark-grade gold corpus,
- a general-purpose Turkish LLM training dataset,
- a commercial model-training dataset,
- an author-imitation corpus,
- a style-cloning resource.

---

## 9. Immediate next steps

Recommended next-stage work:

1. Prepare a full technical report.
2. Add a field-by-field annotation guide.
3. Define baseline experiments.
4. Add a small reproducible evaluation script.
5. Collect external feedback from Turkish NLP and digital humanities researchers.
6. Prepare a workshop or resource-paper submission.

---

## 10. Suggested citation wording

For the full dataset publication record:

> Yaşar, F. (2026). *Tasvir Bankası v0.3.1: A Turkish Literary Scene-State-Description Dataset and Annotation Pipeline*. Zenodo. https://doi.org/10.5281/zenodo.20579958

For the GitHub public-preview pipeline package:

> Yaşar, F. (2026). *Tasvir Bankası: Turkish Literary Annotation Pipeline*. GitHub.
