# Gold-Smoke Subset v0.1

This directory contains the public 100-record schema-validated gold-smoke subset for Tasvir Bankası.

This subset is for installation and validation checks. It is not a human-verified gold-eval split.

## Target and replacement rule

- Target directory: `data/gold_smoke_v0.1/`
- Replace rule: replace all `*.gold_smoke_v0.1.jsonl` files together when regenerating this subset.
- Record count: 100
- Distribution: 20 records from each source dataset file

## Files

| Gold-smoke file | Source file | Records |
|---|---|---:|
| `sabahattin_ali_kurk_mantolu_madonna.gold_smoke_v0.1.jsonl` | `Sabahattin_Ali_Kurk_Mantolu_Madonna.dataset.jsonl` | 20 |
| `sait_faik_luzumsuz_adam.gold_smoke_v0.1.jsonl` | `Sait_Faik_Luzumsuz_Adam.dataset.jsonl` | 20 |
| `sait_faik_sahmerdan.gold_smoke_v0.1.jsonl` | `Sait_Faik_Sahmerdan.dataset.jsonl` | 20 |
| `sait_faik_sarnic.gold_smoke_v0.1.jsonl` | `Sait_Faik_Sarnic.dataset.jsonl` | 20 |
| `sait_faik_semaver.gold_smoke_v0.1.jsonl` | `Sait_Faik_Semaver.dataset.jsonl` | 20 |

## Validation

```bash
python tests/validate_jsonl_schema.py \
  --schema schemas/tasvir_record_schema.v0.1.json \
  --input data/gold_smoke_v0.1 \
  --report data/reports/dataset_profile_v0.1.json
```

Expected result: validation passes with 100 records and no duplicate `micro_block_id` values.

## Two-regime companion probe

Use `data/two_regime_probe_v0.1/` to explicitly test the summary-less non-event segment branch of the validator. That companion probe contains event-bearing records with `brief_summary` and summary-less valid non-event records with alternate evidence.
