# Test Execution README

This README documents the execution order and commands for the delivered Python validation script.

## Execution order

1. Install dependencies.
2. Run `tests/validate_jsonl_schema.py` against the schema and JSONL subset.
3. Review the generated JSON report.

## Commands

```bash
python -m pip install -r requirements.txt

python tests/validate_jsonl_schema.py \
  --schema schemas/tasvir_record_schema.v0.1.json \
  --input data/gold_smoke_v0.1 \
  --report data/reports/dataset_profile_v0.1.json
```

The script exits with status code `0` when validation passes and `1` when validation fails.
