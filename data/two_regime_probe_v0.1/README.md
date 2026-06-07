# Two-Regime Probe v0.1

This directory contains a small public companion probe for validating the two-regime segment policy.

It is not a human-verified gold-eval split and is not a full benchmark.

## Target and replacement rule

- Target directory: `data/two_regime_probe_v0.1/`
- Replace rule: replace all `*.two_regime_probe_v0.1.jsonl` files together when regenerating this probe.
- Record count: 20
- Distribution: 4 records from each source dataset file
- Per-source composition: 2 event-bearing records with `brief_summary`, 2 summary-less valid non-event records with alternate evidence

## Files

| Probe file | Source file | Records |
|---|---|---:|
| `sabahattin_ali_kurk_mantolu_madonna.two_regime_probe_v0.1.jsonl` | `Sabahattin_Ali_Kurk_Mantolu_Madonna.dataset.jsonl` | 4 |
| `sait_faik_luzumsuz_adam.two_regime_probe_v0.1.jsonl` | `Sait_Faik_Luzumsuz_Adam.dataset.jsonl` | 4 |
| `sait_faik_sahmerdan.two_regime_probe_v0.1.jsonl` | `Sait_Faik_Sahmerdan.dataset.jsonl` | 4 |
| `sait_faik_sarnic.two_regime_probe_v0.1.jsonl` | `Sait_Faik_Sarnic.dataset.jsonl` | 4 |
| `sait_faik_semaver.two_regime_probe_v0.1.jsonl` | `Sait_Faik_Semaver.dataset.jsonl` | 4 |

## Validation

```bash
python tests/validate_jsonl_schema.py \
  --schema schemas/tasvir_record_schema.v0.1.json \
  --input data/two_regime_probe_v0.1 \
  --report data/reports/two_regime_probe_report_v0.1.json
```

Expected result:

```json
{"passed": true, "total_records": 20, "error_count": 0}
```

The generated report must include `summaryless_valid_records > 0` and `summaryless_invalid_records = 0`.

## Purpose

This probe exists because `brief_summary` is intentionally not a global field requirement. Event-bearing scenes require `brief_summary`; non-event state, emotion, atmosphere, descriptive, or structural fallback segments may omit it when alternate evidence is present.
