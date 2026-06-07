# Source Text Inventory

Public release reference: `v0.3.1-publication-polish`.

This inventory maps each dataset file to a base literary work, author, original publication year, and the source-edition metadata recorded for this release. It is a bibliographic and technical documentation surface, not a legal opinion.

## Scope

- The inventory covers the five JSONL train files in the Hugging Face-oriented dataset package.
- Source-edition metadata is recorded from the user-provided copyright/title-page images when available.
- Modern publisher introductions, editor notes, cover matter, footnotes, afterwords, special edition material, and publisher-specific paratext are outside the dataset scope.
- Exact source-edition legal status remains **pending / not legally verified**. Missing or uncertain information is explicitly marked rather than inferred.

## Source inventory table

| source_id | dataset_file | work_title | author_name | author_years | original_publication_year | profiled_records | candidate_public_domain_start | source_publisher | source_edition_used | source_edition_year | printing_or_edition | ISBN | edition_metadata_status | exact_source_edition_status | release_scope |
|---|---|---|---|---|---:|---:|---|---|---|---|---|---|---|---|---|
| TB-SRC-001 | `Sabahattin_Ali_Kurk_Mantolu_Madonna.dataset.jsonl` | Kürk Mantolu Madonna | Sabahattin Ali | 1907-1948 | 1943 | 392 | 2019-01-01 | Yapı Kredi Yayınları | YKY edition; image-recorded bibliographic page | 2009 | 32nd printing, İstanbul, Ocak 2009; YKY 1st printing İstanbul, Şubat 1998; original 1st printing Remzi Kitabevi, 1943 | 978-975-363-802-7 | bibliographic_page_recorded_from_user_image | pending / not legally verified | base literary text only; edition-specific material excluded |
| TB-SRC-002 | `Sait_Faik_Luzumsuz_Adam.dataset.jsonl` | Lüzumsuz Adam | Sait Faik Abasıyanık | 1906-1954 | 1948 | 385 | 2025-01-01 | Yapı Kredi Yayınları | Bütün Eserleri / Sait Faik Abasıyanık, Delta 10, YKY 2987; editor Sevengül Sönmez | 2009 | 1st printing, İstanbul, Ekim 2009 | 978-975-08-1683-3 | bibliographic_page_recorded_from_user_image | pending / not legally verified | base literary text only; edition-specific material excluded |
| TB-SRC-003 | `Sait_Faik_Sahmerdan.dataset.jsonl` | Şahmerdan | Sait Faik Abasıyanık | 1906-1954 | 1940 | 492 | 2025-01-01 | Yapı Kredi Yayınları | Bütün Eserleri / Sait Faik Abasıyanık, Delta 10, YKY 2987; editor Sevengül Sönmez | 2009 | 1st printing, İstanbul, Ekim 2009 | 978-975-08-1683-3 | bibliographic_page_recorded_from_user_image | pending / not legally verified | base literary text only; edition-specific material excluded |
| TB-SRC-004 | `Sait_Faik_Sarnic.dataset.jsonl` | Sarnıç | Sait Faik Abasıyanık | 1906-1954 | 1939 | 479 | 2025-01-01 | Yapı Kredi Yayınları | Bütün Eserleri / Sait Faik Abasıyanık, Delta 10, YKY 2987; editor Sevengül Sönmez | 2009 | 1st printing, İstanbul, Ekim 2009 | 978-975-08-1683-3 | bibliographic_page_recorded_from_user_image | pending / not legally verified | base literary text only; edition-specific material excluded |
| TB-SRC-005 | `Sait_Faik_Semaver.dataset.jsonl` | Semaver | Sait Faik Abasıyanık | 1906-1954 | 1936 | 424 | 2025-01-01 | Yapı Kredi Yayınları | Bütün Eserleri / Sait Faik Abasıyanık, Delta 10, YKY 2987; editor Sevengül Sönmez | 2009 | 1st printing, İstanbul, Ekim 2009 | 978-975-08-1683-3 | bibliographic_page_recorded_from_user_image | pending / not legally verified | base literary text only; edition-specific material excluded |

## Source edition boundary

The dataset records are derived from the base literary works. The release does not include modern publisher introductions, editor notes, cover matter, footnotes, afterwords, special edition material, or publisher-specific paratext. Exact edition-level legal status is not asserted by this documentation.

## References and evidence basis

- User-provided bibliographic-page image for `Kürk Mantolu Madonna`: Yapı Kredi Yayınları 967 / Edebiyat 250; YKY 32nd printing, İstanbul, Ocak 2009; ISBN 978-975-363-802-7; original first printing Remzi Kitabevi, 1943.
- User-provided bibliographic-page screenshot for `Bütün Eserleri / Sait Faik Abasıyanık`: Yapı Kredi Yayınları 2987 / Delta 10; editor Sevengül Sönmez; 1st printing İstanbul, Ekim 2009; ISBN 978-975-08-1683-3.
- Public bibliographic checks were used only for original publication-year verification and author chronology. They do not override the pending/not-legally-verified source-edition status.
