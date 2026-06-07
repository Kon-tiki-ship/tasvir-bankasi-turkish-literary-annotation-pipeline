# Descriptive Extraction Fix Notes

## Scope
- Fixed substring-based false positives in descriptive tagging.
- Kept all non-descriptive fields intact.
- Regenerated only:
  - `descriptive_profile`
  - `descriptive_profile_enriched`
  - `descriptive_profile_enriched_filtered`

## Root Cause
- Stage `06_00_description_category_tagging.py` previously used substring checks (`kw in lower`), which produced false matches:
  - `grev -> ev`
  - `otel -> el`
  - `güzel -> el`
  - `karar -> kar`
  - `karşı -> kar`
  - `Karahisarlı -> kar`
  - `gölge -> göl`
  - `boyanmış -> boy`
  - `tutan -> utan`
  - `ibarettir/beraber -> bar`

## Fix Strategy
- Replaced substring matching with token-aware matching.
- Added strict short-root guards for high-risk roots (`ev`, `el`, `kar`, `bar`, `gol`, `boy`, `goz`).
- Retained inflected forms for valid matches (e.g., `evde`, `elinde`, `karlı`, `gölde`, `gözleri`, `utandı`).
- Added regression tests for negative and positive examples.

## Edge-case Tightening (Second Pass)
- Tightened short-root handling to close remaining edge false positives:
  - `böyle -> boy` blocked
  - `boynuna / boyunlarına -> boy` blocked
  - `karısı -> kar` blocked
  - `evlatları -> ev` blocked
  - `bari -> bar` blocked
- Kept target positives:
  - `evde/eve/evin/evler`
  - `elini/eliyle/elleri`
  - `kar/karda/karlı`
  - `gölde/gölün`
  - `gözleri/gözü`
  - `utandı`
  - `barda/barın`
  - `boyu/boylu`

## Edge-case Final Pass (gold_smoke v0.2 audit set rules applied on current gold_smoke)
- `karısı/karısına/karısını` no longer triggers `kar` nature label.
- `elektriğini`, `güzelliğiyle`, `ellilik` no longer trigger `el`.
- Monetary quantity contexts (`altı yüz lira`, `yüz lira`, `iki yüz kuruş`) no longer trigger human `yuz`.
- `yağmurluk*` clothing/object context no longer triggers `yagmur`.
- `tutturulmuş*` no longer triggers `tuttu` action.
- Decorative flower contexts (`çiçek motifli`, `çiçek çizilmiş`, ship toy ornament) no longer trigger nature `cicek`; routed to human-review queue when context is decorative.

## Safety Rules
- No deletion of records.
- `text` unchanged.
- Non-descriptive fields unchanged (scene, triage, state identity, morphology/tense/dialogue).
- Previous backups preserved in:
  - `descriptive_profile_previous_backup`
  - `descriptive_profile_enriched_previous_backup`
  - `descriptive_profile_enriched_filtered_previous_backup`

## Regeneration Tool
- `tools/clean_and_regenerate_descriptive_fields.py`
- Backs up previous fields, removes dirty descriptive fields, and regenerates clean outputs.
