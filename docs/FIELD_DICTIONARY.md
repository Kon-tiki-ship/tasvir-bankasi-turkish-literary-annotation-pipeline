# Field Dictionary

This document describes the public JSONL record contract for Tasvir Bankası record schema v0.1.

## Required core fields

| Field | Type | Meaning |
|---|---:|---|
| `story_id` | string | Stable story/work identifier. |
| `paragraph_id` | string | Stable paragraph identifier. |
| `paragraph_index` | integer | 1-based paragraph index within the story. |
| `total_paragraphs` | integer | Number of paragraphs in the source story/work. |
| `text` | string | Micro-block or paragraph text. Must not be empty. |
| `micro_block_id` | string | Unique record-level identifier. |
| `parent_paragraph_id` | string | Source paragraph from which the micro-block was derived. |
| `is_micro_block` | boolean | Whether the row represents a micro-block split. |
| `stage` | string | Pipeline stage marker carried by the record. |
| `dialogue_char_ratio` | number | Approximate ratio of dialogue characters to total characters. |
| `dialogue_sentence_ratio` | number | Approximate ratio of dialogue sentences to all sentences. |
| `has_dialogue` | boolean | Whether dialogue-like text is detected. |
| `token_count` | integer | Token count estimate. |
| `noun_ratio` | number | Estimated noun ratio. |
| `verb_ratio` | number | Estimated verb ratio. |
| `adj_ratio` | number | Estimated adjective ratio. |
| `adv_ratio` | number | Estimated adverb ratio. |
| `non_finite_verb_ratio` | number | Estimated non-finite verb ratio. |
| `tense_mode` | string | Dominant tense/mode label inferred by the pipeline. |
| `tense_distribution` | object | Distribution-like object for tense signals. |
| `tense_confidence` | number | Confidence-like value for the dominant tense/mode label. |
| `scene_segments` | object | Scene segmentation payload. Must contain `scenes`. |
| `scene_source` | string | Name of the stage/source that produced the scene segmentation. |
| `id_normalized` | boolean | Whether identifier normalization has been applied. |
| `triage_candidate` | boolean | Whether the record was selected for downstream enrichment. |
| `triage_reasons` | string array | Human-readable triage evidence labels. |
| `triage_stage` | string | Triage stage marker. |
| `triage_version` | string | Triage ruleset version. |
| `state_identity_profile` | object | State identity metadata. Must contain non-empty `top_states`. |

## Nested scene fields

Every object in `scene_segments.scenes` must contain:

| Field | Type | Requirement | Meaning |
|---|---:|---|---|
| `scene_index` | integer | Required | 1-based scene index inside the record. |
| `scene_type` | string | Required | Scene type label, for example `single_scene`. |
| `split_reason` | string | Required | Reason for keeping, splitting, or falling back. |
| `brief_summary` | string | Conditional | Required only for event-bearing scenes. Optional for non-event segments with alternate evidence. |

## Two-regime summary rule

`brief_summary` is not globally required. The validator applies these rules:

1. Event-bearing scenes require a non-empty `brief_summary`.
2. Structural fallback segments may omit `brief_summary` when `split_reason` or `fallback_review` explains the fallback and the record has alternate evidence.
3. State-bearing, emotion-bearing, atmosphere-bearing, and descriptive segments may omit `brief_summary` when profile evidence is present.
4. A summary-less segment without state, embedding, descriptive, atmosphere, emotion, or fallback evidence is a validation error.

## Required nested state identity field

`state_identity_profile.top_states` must be a non-empty list of pairs:

```json
["state_label", 0.75]
```

Each pair contains a string label and a numeric value. `state_identity_profile.all_scores` and `state_identity_profile.embedding_model` are treated as embedding-derived evidence when present.

## Optional fallback and descriptive fields

| Field | Type | Meaning |
|---|---:|---|
| `fallback_review` | object | Structural fallback review metadata such as `reason` and token count. |
| `descriptive_profile` | array | Category labels with short lexical reasons. |
| `descriptive_profile_enriched` | array | Category labels with noun/verb/adjective evidence. |
| `descriptive_profile_enriched_filtered` | array | Filtered category labels and lexical evidence. |

## Optional source metadata

Some files include `book_id` and `story_title`. These are useful metadata fields but are not required for schema v0.1 because not every source record contains them.

## Identifier rule

`micro_block_id` must be unique within the validated JSONL collection. The validator treats duplicate values as an error.


## Descriptive category note: `descr_metaphor`

`descr_metaphor` should be read as **metaphor / simile / comparison / analogy / figurative-marker evidence**. It indicates that the segment contains textual evidence such as `gibi`, `sanki`, `adeta`, or comparable figurative/comparison markers.

It should **not** be interpreted as a fully validated Conceptual Metaphor Theory annotation or as proof that the entire segment has been curator-verified as a conceptual metaphor. In v0.3.1, the curated gold-eval records linked to this field are label-level verified records, not full-record benchmark gold records.
