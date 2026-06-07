# Annotation Guidelines

These guidelines define the expected human-review conventions for public Tasvir Bankası JSONL records.

## General principles

- Preserve the source text exactly in `text`.
- Do not add invented events or interpretations.
- Prefer short, factual labels over literary commentary.
- Keep each JSONL row independent.
- Use stable identifiers; do not rename existing IDs unless a normalization stage explicitly requires it.
- Treat the current `gold_smoke_v0.1` subset as a schema-validated smoke subset, not as a human-verified gold-eval split.

## Segment regimes

Tasvir records contain two validation regimes.

### Event-bearing scenes

An event-bearing scene contains an action, interaction, transition, or narratively reportable occurrence. It requires:

- `scene_index`
- `scene_type`
- `split_reason`
- `brief_summary`

The summary must be short, factual, and based only on the record text.

### Non-event segments

A non-event segment may encode state, emotion, description, atmosphere, reflection, or structural fallback. These segments may omit `brief_summary` when alternate evidence exists. Valid alternate evidence includes:

- `state_identity_profile.top_states`
- `state_identity_profile.all_scores`
- `state_identity_profile.embedding_model`
- `descriptive_profile`
- `descriptive_profile_enriched`
- `descriptive_profile_enriched_filtered`
- `fallback_review.reason`
- `scene_segments.scenes[].split_reason` with `structural_fallback`

Do not force event-style summaries onto non-event segments merely to satisfy a field. The absence of `brief_summary` can be correct when the segment is represented by state/descriptive/embedding-derived evidence.

## Scene segmentation

A record may contain one or more scenes under `scene_segments.scenes`.

A scene should be split only when there is a clear change in at least one of the following:

- location
- time
- narrator or focal viewpoint
- event focus
- interaction mode

Do not split only because the text is long.

## Known two-regime profile

The profiled full source inventory contains 2,172 records. Under the previous strict summary-only rule, 1,720 records were missing `brief_summary`. Under the corrected two-regime rule, those records are valid when they are structural/state/emotion/atmosphere/descriptive non-event segments with alternate evidence.

Records that have neither `brief_summary` nor alternate evidence remain invalid and require normalization or human review.

## State identity metadata

`state_identity_profile.top_states` should contain the most relevant state labels for the record. Labels must be stable strings. Numeric values must be numeric JSON values, not quoted strings.

## Descriptive categories

Use category labels consistently. Current public examples include:

- `descr_human`
- `descr_emotion`
- `descr_location`
- `descr_nature`
- `descr_action`
- `descr_object`
- `descr_psychology`
- `descr_metaphor`

Lexical evidence should be copied from or normalized from the text. Do not add evidence terms that cannot be traced to the record text or to the public preprocessing output.

## Quality flags for review

Mark a record for review when:

- `text` is empty or whitespace-only.
- `micro_block_id` is missing or duplicated.
- A scene object is missing `scene_index`, `scene_type`, or `split_reason`.
- An event-bearing scene is missing `brief_summary`.
- A summary-less non-event segment has no state, embedding, descriptive, atmosphere, emotion, or fallback evidence.
- `state_identity_profile.top_states` is empty.
- Descriptive categories are present but have no visible lexical evidence.
- Source-text rights status is not clear for public release.
