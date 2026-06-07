# Hugging Face Release Readiness Note

Public release reference: `v0.1.0-public-preview`.

This document was originally created as a pre-release checklist for a future Hugging Face full dataset package. It is retained here as a **historical release-engineering note** for the GitHub public-preview repository.

## Current status in the upload-ready bundle

The Hugging Face dataset surface has since been prepared separately as:

```text
02_HUGGINGFACE_UPLOAD/tasvir-bankasi-turkish-literary-scene-state-description-v0.3.1/
```

That package is the intended Hugging Face upload root for `v0.3.1-publication-polish`.

## Boundary

- This GitHub repository remains a public-safe pipeline, schema, validator, documentation, and release-check subset package.
- The full train/gold-eval dataset is not part of this GitHub public-preview repository.
- The Hugging Face package has its own dataset card, license files, validation reports, file manifest, and checksums.

## Historical checklist outcome

| ID | Check | Final status for v0.3.1 upload bundle |
|---|---|---|
| HF-001 | Source text inventory maps each dataset file to one work and author. | Completed |
| HF-002 | Rights review table contains required source-level fields. | Completed |
| HF-003 | Candidate status uses non-final legal language. | Completed |
| HF-004 | Modern publisher paratext exclusion policy is documented. | Completed |
| HF-005 | Exact release files selected. | Completed in Hugging Face package |
| HF-006 | Full JSONL package validated. | Completed in Hugging Face package |
| HF-007 | Release-specific validation report generated. | Completed in Hugging Face package |
| HF-008 | Non-commercial data-license terms selected. | Completed |
| HF-009 | Hugging Face dataset card updated. | Completed in Hugging Face package |
| HF-010 | Package scan performed. | Completed for final upload package |

## Note

Source-edition rights language remains intentionally cautious. The package documents public-domain candidacy and excludes modern publisher paratext, but it does not make a legal determination.

Last updated for final upload package: `2026-06-07T10:50:54Z`.
