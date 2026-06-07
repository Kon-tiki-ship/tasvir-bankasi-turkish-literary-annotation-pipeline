# Tasvir Bankası Public Release Patch v0.1.9 Public-Safe Pipeline Naming

This patch prepares the GitHub-oriented public pipeline package for release by removing downstream demonstration exposure and standardizing public-safe stage filenames.

## Public release target

`v0.1.0-public-preview`

Patch history remains documented only in this file.

## Scope

- Remove the root strategic `Readme.md` from the public archive.
- Remove downstream demonstration material from the public pipeline package.
- Standardize all core pipeline Python filenames with public-safe, function-based names.
- Update `README.md`, `RUN_ORDER.md`, and `docs/PIPELINE_OVERVIEW.md` to match the renamed stage files.
- Preserve the 17-script core pipeline count.
- Keep the release boundary focused on scene/state/description-aware dataset construction and validation.

No full dataset files are added. No Hugging Face full release is performed in this patch.

## Changed files

- `README.md`
- `RUN_ORDER.md`
- `PATCH_MANIFEST.md`
- `docs/PIPELINE_OVERVIEW.md`
- `.env.example`
- `data/reports/pipeline_file_audit_v0.1.json`
- `pipeline/*.py` filenames and public-safe internal stage labels

## Removed public material

- Root-level strategic `Readme.md`
- Downstream demonstration directory previously outside the core dataset pipeline

## Validation commands retained

```bash
python tests/validate_jsonl_schema.py --schema schemas/tasvir_record_schema.v0.1.json --input data/gold_smoke_v0.1 --report data/reports/gold_smoke_report_v0.1.json
python tests/validate_jsonl_schema.py --schema schemas/tasvir_record_schema.v0.1.json --input data/two_regime_probe_v0.1 --report data/reports/two_regime_probe_report_v0.1.json
```

Expected and required two-regime condition:

- `summaryless_valid_records > 0`
- `summaryless_invalid_records = 0`

## Core-pipeline boundary confirmation

- Core pipeline remains 17 scripts under `pipeline/`.
- `RUN_ORDER.md` and `pipeline/` alignment is preserved.
- Downstream demonstration scripts are not included in the public pipeline package.

## Identity and licensing preservation

- Project owner and citation author remain **Furkan Yaşar**.
- `LICENSE.md` and `CODE_LICENSE.md` define the source-available non-commercial research license model.
- `DATA_LICENSE.md` keeps code/data/source-text rights separation.
