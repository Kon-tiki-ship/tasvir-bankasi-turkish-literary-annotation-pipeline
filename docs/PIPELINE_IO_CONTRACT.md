# Pipeline I/O Contract

This document defines the public-release input and output contract for the 17-script Tasvir Bankası core dataset pipeline.

## General contract

- All pipeline exchanges are file-based.
- Intermediate records are JSONL unless a stage explicitly reads or writes raw `.txt`.
- Each JSONL line must be an independent JSON object.
- Paths are relative to the repository root by default.
- Public scripts must not contain local absolute paths, committed API keys, tokens, private configuration, or personal machine paths.
- API-enabled scripts must read credentials from environment variables only.

## Environment variables

| Variable | Used by | Required when |
|---|---|---|
| `LLM_API_KEY` | `04_20_llm_scene_segmentation.py`, `04_40_structural_fallback_refinement.py`, `05_10_semantic_state_assignment.py` | Running API-assisted segmentation, structural fallback refinement, or embedding enrichment |

## Stage I/O table

| stage_number | script_filename | exists_in_pipeline_folder | input_paths | output_paths | requires_api | requires_external_tool | public_release_safe | notes |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 1 | `01_00_text_cleanup.py` | yes | `data/raw_text/*.txt` | `data/clean_text/*.txt` | no | no | yes | Uses relative defaults and CLI arguments. |
| 2 | `02_00_paragraph_segmentation.py` | yes | `data/clean_text/*.txt` | `data/stage_2/*.jsonl` | no | no | yes | Paragraph-level segmentation |
| 3 | `02_10_microblock_segmentation.py` | yes | `data/stage_2/*.jsonl` | `data/stage_2.1/*.jsonl` | no | no | yes | Micro-block splitting |
| 4 | `03_00_dialogue_feature_extraction.py` | yes | `data/stage_2.1/*.jsonl` | `data/stage_3/*.jsonl` | no | no | yes | Dialogue ratio analysis |
| 5 | `03_10_morphological_feature_extraction.py` | yes | `data/stage_3/*.jsonl` | `data/stage_4/*stage4.jsonl` | no | zemberek-python | yes | Requires local Zemberek Python package. |
| 6 | `03_20_tense_feature_extraction.py` | yes | `data/stage_4/*stage4.jsonl` | `data/stage_4_1/*.jsonl` | no | no | yes | Tense and temporal feature enrichment |
| 7 | `04_00_scene_boundary_candidate_detection.py` | yes | `data/stage_4_1/*.jsonl` | `data/stage_4_2/*with_scene_updates.jsonl` | no | no | yes | Candidate scene boundary detection |
| 8 | `04_10_scene_coherence_classification.py` | yes | `data/stage_4_2/*with_scene_updates.jsonl` | `data/stage_4_4/*.jsonl` | no | no | yes | Adjacent-block narrative coherence review |
| 9 | `04_20_llm_scene_segmentation.py` | yes | `data/stage_4_4/*.jsonl` | `data/stage_4_8/*_stage_4_8.jsonl` | yes | google-genai | yes | Reads LLM_API_KEY from the environment. |
| 10 | `04_30_structural_fallback_triage.py` | yes | `data/stage_4_8/*.jsonl` | `data/stage_4_9/*.jsonl` | no | no | yes | Structural fallback review |
| 11 | `04_40_structural_fallback_refinement.py` | yes | `data/stage_4_9/*.jsonl` | `data/stage_5/*.jsonl` | yes | google-genai | yes | Reads LLM_API_KEY from the environment. |
| 12 | `04_50_scene_split_postprocessing.py` | yes | `data/stage_5/*.jsonl` | `data/stage_5_0/*.jsonl` | no | zemberek-python | yes | Post-refinement cleanup and normalization |
| 13 | `05_00_record_normalization_and_selection.py` | yes | `data/stage_5_0/*.jsonl` | `data/stage_5_1/*.jsonl` | no | no | yes | Record normalization and triage |
| 14 | `05_10_semantic_state_assignment.py` | yes | `data/stage_5_1/*.jsonl` | `data/stage_5_2/*.jsonl` | yes | google-genai | yes | Reads LLM_API_KEY from the environment. |
| 15 | `06_00_description_category_tagging.py` | yes | `data/stage_5_2/*.jsonl` | `data/stage_5_4/*.jsonl` | no | no | yes | High-level descriptive category tagging |
| 16 | `06_10_description_lexical_enrichment.py` | yes | `data/stage_5_4/*.jsonl` | `data/stage_5_8/*.jsonl` | no | zemberek-python | yes | Lexical enrichment for descriptive evidence |
| 17 | `06_20_description_evidence_filtering.py` | yes | `data/stage_5_8/*.jsonl` | `data/stage_5_8_1/*.jsonl` | no | no | yes | Descriptive evidence filtering and normalization |

## Dataset validation boundary

The final public validation policy is two-regime:

- Event-bearing scene records require non-empty `brief_summary`.
- Summary-less non-event records are valid when they carry accepted alternate evidence such as state identity, embedding-derived profile, descriptive profile, atmosphere/emotion signal, or structural-fallback evidence.
- Summary-less records without accepted alternate evidence are validation errors.

The validator commands remain:

```bash
python tests/validate_jsonl_schema.py --schema schemas/tasvir_record_schema.v0.1.json --input data/gold_smoke_v0.1 --report data/reports/gold_smoke_report_v0.1.json
python tests/validate_jsonl_schema.py --schema schemas/tasvir_record_schema.v0.1.json --input data/two_regime_probe_v0.1 --report data/reports/two_regime_probe_report_v0.1.json
```
