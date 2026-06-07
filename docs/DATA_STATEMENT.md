# Data Statement

## Dataset name

Tasvir Bankası – Scene-Aware Turkish Literary Dataset Pipeline

## Release scope

This public release contains a small gold-smoke subset for validation and documentation review. It does not contain the full production dataset.

## Language

The current records are Turkish literary prose records.

## Data format

Records are stored as JSONL. Each line is an independent JSON object.

## Source type

The records are derived from literary prose texts processed through the public pipeline stages. The public subset is intended to be small and suitable for repository smoke tests.

## Processing overview

The pipeline performs:

- text cleaning
- paragraph segmentation
- micro-block segmentation
- dialogue ratio estimation
- Turkish morphology-based feature extraction
- tense feature extraction
- scene segmentation
- structural cleanup
- enrichment with descriptive categories and lexical evidence
- JSONL validation

## Personal data

The dataset is based on literary text, not collected user profiles or private communications. The release should not include private notes, local paths, API keys, or unpublished working configuration.

## Rights and redistribution

Before publishing or redistributing any text-derived examples, maintainers must confirm that the source texts are legally redistributable in the target jurisdiction. The software and documentation license does not automatically grant rights to redistribute source texts or text-derived dataset rows.

## Known limitations

- The gold-smoke subset is intentionally small.
- It should not be used as a representative benchmark.
- Morphology-derived fields may reflect limitations of the tokenizer and analyzer.
- Scene summaries are short operational metadata, not critical editions of the source texts.
