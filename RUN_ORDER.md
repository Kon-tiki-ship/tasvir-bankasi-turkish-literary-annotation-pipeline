# Pipeline Execution Order

This document defines the authoritative execution order of the Tasvir Bankası core dataset pipeline.

File listing order in GitHub is not execution order. This file is the single source of truth for the 17-script core pipeline.

## Core dataset pipeline

1. `01_00_text_cleanup.py` — Cleans raw text and normalizes paragraph boundaries.
2. `02_00_paragraph_segmentation.py` — Converts cleaned text into paragraph-level JSONL records.
3. `02_10_microblock_segmentation.py` — Splits paragraphs into reusable micro-block records.
4. `03_00_dialogue_feature_extraction.py` — Computes dialogue density and dialogue-to-narration features.
5. `03_10_morphological_feature_extraction.py` — Extracts Turkish morphology statistics with Zemberek.
6. `03_20_tense_feature_extraction.py` — Adds tense and temporal features.
7. `04_00_scene_boundary_candidate_detection.py` — Detects candidate scene boundaries.
8. `04_10_scene_coherence_classification.py` — Classifies coherence across adjacent blocks.
9. `04_20_llm_scene_segmentation.py` — Performs API-assisted scene segmentation. Requires `LLM_API_KEY` for API-enabled execution.
10. `04_30_structural_fallback_triage.py` — Reviews structural fallback scene outputs without API calls.
11. `04_40_structural_fallback_refinement.py` — Refines selected structural fallback cases with API assistance. Requires `LLM_API_KEY` for API-enabled execution.
12. `04_50_scene_split_postprocessing.py` — Performs post-refinement cleanup and feature normalization.
13. `05_00_record_normalization_and_selection.py` — Normalizes micro-block identifiers and selects valid enrichment candidates.
14. `05_10_semantic_state_assignment.py` — Adds semantic state identity metadata. Requires `LLM_API_KEY` for API-enabled execution.
15. `06_00_description_category_tagging.py` — Assigns high-level descriptive categories.
16. `06_10_description_lexical_enrichment.py` — Adds explainable lexical evidence using Turkish morphology.
17. `06_20_description_evidence_filtering.py` — Filters and normalizes enriched lexical evidence.

## Pipeline file audit

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

## Notes

- All core stages communicate through relative repository paths.
- JSONL stages write one independent JSON object per line.
- API outputs are treated as untrusted input and validated downstream.
- `LLM_API_KEY` is the public-safe environment variable for API-enabled stages.
- Two-regime validation policy is unchanged: `brief_summary` is required only for event-bearing scene records; non-event/state/emotion/atmosphere/descriptive/structural-fallback records may be valid without `brief_summary` when accepted alternate evidence is present.
