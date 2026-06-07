# Pipeline Overview

Tasvir Bankası uses a 17-script core dataset pipeline. This document mirrors `RUN_ORDER.md` and provides a public-release audit table.

The pipeline is a scene/state/description-aware Turkish literary dataset pipeline. It is not a style bank and not a downstream story-generation system.

## Public release

Release version: `v0.1.0-public-preview`.

## Core policy

- The core pipeline lives under `pipeline/`.
- Every script listed in `RUN_ORDER.md` must exist under `pipeline/`.
- Every script under `pipeline/` must be listed in `RUN_ORDER.md`.
- API-enabled stages read credentials only from environment variables. No `.env` file, key, token, or local credential file is committed.
- `LLM_API_KEY` is the environment variable for API-enabled stages.
- Two-regime validation is unchanged: event-bearing scenes require `brief_summary`; valid non-event state/emotion/atmosphere/descriptive/structural-fallback segments may omit `brief_summary` when accepted alternate evidence is present.

## Script execution model note

Core scripts are stage executables intended for run-order pipeline execution. They are not packaged as import-safe library modules and are documented as pipeline stages rather than reusable SDK functions.

## Pipeline audit table

| stage_number | script_filename | exists_in_pipeline_folder | input_paths | output_paths | requires_api | requires_external_tool | public_release_safe | notes |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 1 | `01_00_text_cleanup.py` | yes | `data/raw_text/*.txt` | `data/clean_text/*.txt` | no | no | yes | Uses relative defaults and CLI arguments. |
| 2 | `02_00_paragraph_segmentation.py` | yes | `data/clean_text/*.txt` | `data/stage_2/*.jsonl` | no | no | yes | Paragraph-level segmentation. |
| 3 | `02_10_microblock_segmentation.py` | yes | `data/stage_2/*.jsonl` | `data/stage_2.1/*.jsonl` | no | no | yes | Micro-block segmentation. |
| 4 | `03_00_dialogue_feature_extraction.py` | yes | `data/stage_2.1/*.jsonl` | `data/stage_3/*.jsonl` | no | no | yes | Dialogue feature extraction. |
| 5 | `03_10_morphological_feature_extraction.py` | yes | `data/stage_3/*.jsonl` | `data/stage_4/*stage4.jsonl` | no | yes | yes | Requires local Zemberek Python package. |
| 6 | `03_20_tense_feature_extraction.py` | yes | `data/stage_4/*stage4.jsonl` | `data/stage_4_1/*.jsonl` | no | no | yes | Tense and temporal feature extraction. |
| 7 | `04_00_scene_boundary_candidate_detection.py` | yes | `data/stage_4_1/*.jsonl` | `data/stage_4_2/*with_scene_updates.jsonl` | no | no | yes | Candidate scene boundary detection. |
| 8 | `04_10_scene_coherence_classification.py` | yes | `data/stage_4_2/*with_scene_updates.jsonl` | `data/stage_4_4/*.jsonl` | no | no | yes | Adjacent-block scene coherence classification. |
| 9 | `04_20_llm_scene_segmentation.py` | yes | `data/stage_4_4/*.jsonl` | `data/stage_4_8/*_stage_4_8.jsonl` | yes | yes | yes | Reads LLM_API_KEY from the environment. |
| 10 | `04_30_structural_fallback_triage.py` | yes | `data/stage_4_8/*.jsonl` | `data/stage_4_9/*.jsonl` | no | no | yes | Structural fallback triage. |
| 11 | `04_40_structural_fallback_refinement.py` | yes | `data/stage_4_9/*.jsonl` | `data/stage_5/*.jsonl` | yes | yes | yes | Reads LLM_API_KEY from the environment. |
| 12 | `04_50_scene_split_postprocessing.py` | yes | `data/stage_5/*.jsonl` | `data/stage_5_0/*.jsonl` | no | yes | yes | Post-refinement cleanup and normalization. |
| 13 | `05_00_record_normalization_and_selection.py` | yes | `data/stage_5_0/*.jsonl` | `data/stage_5_1/*.jsonl` | no | no | yes | Record normalization and selection. |
| 14 | `05_10_semantic_state_assignment.py` | yes | `data/stage_5_1/*.jsonl` | `data/stage_5_2/*.jsonl` | yes | yes | yes | Reads LLM_API_KEY from the environment. |
| 15 | `06_00_description_category_tagging.py` | yes | `data/stage_5_2/*.jsonl` | `data/stage_5_4/*.jsonl` | no | no | yes | High-level description category tagging. |
| 16 | `06_10_description_lexical_enrichment.py` | yes | `data/stage_5_4/*.jsonl` | `data/stage_5_8/*.jsonl` | no | yes | yes | Lexical enrichment for descriptive evidence. |
| 17 | `06_20_description_evidence_filtering.py` | yes | `data/stage_5_8/*.jsonl` | `data/stage_5_8_1/*.jsonl` | no | no | yes | Description evidence filtering and normalization. |

## Machine-readable audit

```text
data/reports/pipeline_file_audit_v0.1.json
```
