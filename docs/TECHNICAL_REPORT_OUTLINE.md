# Technical Report Outline

**Working title:**  
Tasvir Bankası: A Turkish Literary Scene-State-Description Dataset and Annotation Pipeline for Computational Narratology

**Target length:** 8–12 pages  
**Target genre:** technical report, preprint, workshop resource paper, academic portfolio document

---

## Abstract

Tasvir Bankası is a Turkish literary annotation dataset and pipeline designed to represent literary prose as structured narrative data. The project transforms rights-reviewed public-domain candidate Turkish prose into JSONL records with layers for scene segmentation, state-bearing units, dialogue signals, tense/morphology, and descriptive evidence. This report describes the motivation, dataset design, annotation layers, pipeline architecture, validation policy, access model, and limitations of the project. It positions Tasvir Bankası as a pilot research resource for Turkish literary NLP, computational narratology, and digital humanities.

---

## 1. Introduction

### Purpose

Introduce the problem: Turkish literary NLP lacks structured resources that model prose at the level of scene, state, dialogue, time, morphology, and descriptive evidence.

### Key claims

- Literary prose should not be reduced to raw text or token frequency.
- Turkish literary passages often carry scene, state, atmosphere, dialogue, and tense information simultaneously.
- A structured JSONL representation enables reproducible annotation and model-oriented analysis.

### Suggested paragraph

Turkish literary prose contains narrative structures that are not fully captured by general-purpose NLP resources. A passage may introduce a scene, maintain a psychological state, shift narrative time, carry indirect dialogue, or provide descriptive evidence without presenting a conventional event. Tasvir Bankası addresses this representational gap by introducing a scene-state-description annotation model for Turkish literary prose.

---

## 2. Background and related work

### Areas to cover

- Turkish NLP resources
- Historical Turkish / Ottoman Turkish resources
- Universal Dependencies and syntactic annotation
- PropBank / FrameNet-style semantic annotation
- discourse relation annotation
- literary NLP and computational narratology
- scene segmentation and narrative annotation
- TEI / CATMA / annotation tooling

### Framing

The report should acknowledge that Turkish NLP has several important linguistic resources, but it should clarify that these resources usually do not annotate literary prose as layered narrative units.

### Suggested transition

Existing Turkish NLP resources provide important foundations for tokenization, morphology, syntax, semantic roles, named entities, and discourse analysis. However, a literary passage-level annotation resource for scene-state-description modeling remains underdeveloped.

---

## 3. Dataset design

### Questions to answer

- What is a record?
- What is a text unit?
- What kinds of literary evidence can a text unit carry?
- Why JSONL?
- Why separate event-bearing and non-event textual units?

### Key concepts

- textual unit
- scene-bearing unit
- state-bearing unit
- dialogue-bearing unit
- tense-bearing unit
- descriptive-evidence-bearing unit
- curation ledger
- selection metadata

### Recommended explanation

A Tasvir Bankası record represents a literary text unit enriched with narrative and linguistic metadata. Records are not merely passages of prose; they are structured observations about how a passage functions within literary narration.

---

## 4. Annotation layers

### Main layers

| Layer | Description |
|---|---|
| `scene_segments` | Scene-bearing or scene-adjacent segmentation information |
| `scene_source` | Source and provenance information for scene extraction |
| `scene_edge` | Boundary behavior and transition evidence |
| `state_identity_profile` | State-bearing, emotion-bearing, or non-event textual status |
| `descriptive_profile` | Descriptive evidence and description-bearing properties |
| `descriptive_profile_enriched` | Additional descriptive-evidence signals |
| `descriptive_profile_enriched_filtered` | Filtered descriptive-evidence layer |
| `dialogue` | Dialogue-bearing or speech-related evidence |
| `tense` | Tense-bearing properties |
| `morphology` | Morphology-oriented features |
| `selection_metadata` | Split, validation, and selection information |

### Discussion points

- Why description is not secondary metadata.
- Why state-bearing units may not have event summaries.
- Why dialogue detection should include speech-related signals beyond quotation marks.
- Why tense and morphology matter for Turkish literary prose.

---

## 5. Pipeline architecture

### Questions to answer

- What does the pipeline take as input?
- What does it produce?
- What is the role of each stage?
- How is validation performed?
- How are ambiguous cases handled?

### High-level flow

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

### Public release boundary

The GitHub repository contains the public-safe pipeline, schema, validator, documentation, and limited smoke/probe samples. The full dataset payload is hosted separately as a gated non-commercial Hugging Face dataset.

---

## 6. Validation policy

### Core validation ideas

- Schema validation
- Two-regime policy
- Event-bearing versus non-event textual unit handling
- Summary-less valid records
- Curation ledger for ambiguous semantic cases

### Two-regime validation

| Record type | `brief_summary` policy |
|---|---|
| Event-bearing scene | Required |
| Non-event state/emotion/description/structural-fallback segment | May be omitted if alternate evidence is present |
| Summary-less segment without alternate evidence | Invalid |

### Rationale

Literary prose often includes meaningful descriptive or state-bearing units that do not behave like conventional event summaries. The validation policy should preserve these records rather than incorrectly reject them.

---

## 7. Dataset statistics

### Current statistics to include

- train records: 2,172
- curated gold-eval records: 92
- human curation ledger records: 98
- pending queue: 0

### Important qualification

The curated gold-eval subset should be described as a label-level evaluation seed, not as a full-record benchmark-grade gold corpus.

---

## 8. Rights, access, and licensing

### Key points

- Source texts are rights-reviewed public-domain candidates.
- The release does not constitute a legal determination.
- The full dataset is gated and non-commercial.
- Commercial model training, resale, paid API integration, and style-cloning uses require explicit permission.
- GitHub public-preview package and full Hugging Face dataset package are separate.

### Recommended language

The access model is designed to support research visibility and non-commercial reproducibility while reducing the risk of misuse in author-imitation, style-cloning, or commercial model-training settings.

---

## 9. Use cases

### Research use cases

- Turkish literary scene segmentation
- descriptive-evidence detection
- dialogue-bearing detection
- event-bearing versus state-bearing classification
- tense/morphology distribution analysis
- computational narratology
- digital humanities annotation workflows
- literary corpus construction
- Turkish literary NLP benchmarking in early-stage form

---

## 10. Baseline experiments

### Suggested first experiments

1. Dialogue-bearing detection
2. Descriptive-evidence detection
3. Scene-bearing versus non-scene classification
4. Event-bearing versus state-bearing distinction

### Suggested methods

- majority baseline
- rule-based baseline
- TF-IDF + logistic regression
- Turkish transformer baseline
- optional exploratory LLM zero-shot comparison

### Metrics

- accuracy
- precision
- recall
- F1
- macro-F1 for imbalanced classes
- confusion matrix
- qualitative error analysis

---

## 11. Limitations

### Required limitations

- Pilot research resource, not mature benchmark.
- Public-preview subsets are not full gold datasets.
- Gold-eval is label-level, not full-record verified.
- Source-rights review is not legal advice.
- Schema generalization beyond Turkish literary prose requires review.
- Some descriptive and metaphor-related fields should be interpreted as evidence markers, not complete literary theory annotations.

---

## 12. Conclusion

The conclusion should restate the contribution:

Tasvir Bankası provides a first structured step toward scene-state-description annotation for Turkish literary prose. It connects dataset construction, annotation schema design, validation policy, and reproducible public documentation. Its main value lies in making literary narrative units computationally inspectable without reducing them to raw text or style imitation.

---

## Appendix A: Recommended citation

Yaşar, F. (2026). *Tasvir Bankası v0.3.1: A Turkish Literary Scene-State-Description Dataset and Annotation Pipeline*. Zenodo. https://doi.org/10.5281/zenodo.20579958

---

## Appendix B: Recommended repository description

Tasvir Bankası is a Turkish literary scene-state-description dataset and annotation pipeline for computational narratology and Turkish literary NLP.
