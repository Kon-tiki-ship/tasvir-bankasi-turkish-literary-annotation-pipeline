from __future__ import annotations

from pathlib import Path
import json
from collections import defaultdict

# =========================================================
# CONFIG
# =========================================================

INPUT_DIR = Path("data/stage_5_0")
OUTPUT_DIR = Path("data/stage_5_1")
OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

# --- TRIAGE EŞİKLERİ (ATMOSFER ODAKLI) ---
MIN_TOKEN_SCENE_STRONG = 120     # klasik sahne
MIN_TOKEN_DESCRIPTIVE = 70       # sessiz tasvir
MIN_NOUN_RATIO = 0.25            # tasvir yoğunluğu

VALID_COHERENCE_FLAGS = {"scene_candidate", "uncertain"}

# =========================================================
# PHASE 1 — MICRO_BLOCK_ID NORMALIZATION
# =========================================================

def normalize_micro_block_ids(records: list[dict]) -> list[dict]:
    """
    Aynı micro_block_id'ye sahip birden fazla kayıt varsa
    bunları _s1, _s2, ... suffix ile benzersiz hale getirir.
    """

    groups = defaultdict(list)

    for rec in records:
        key = (
            rec.get("parent_paragraph_id"),
            rec.get("micro_block_id")
        )
        groups[key].append(rec)

    normalized = []

    for (_, _), items in groups.items():
        if len(items) == 1:
            items[0]["id_normalized"] = False
            normalized.append(items[0])
            continue

        for idx, rec in enumerate(items, start=1):
            original_id = rec.get("micro_block_id")
            rec["micro_block_id"] = f"{original_id}_s{idx}"
            rec["id_normalized"] = True
            rec["id_normalization_index"] = idx
            normalized.append(rec)

    return normalized

# =========================================================
# PHASE 2 — TRIAGE (SCENE-DESCRIPTION-AWARE)
# =========================================================

def apply_triage(rec: dict) -> dict:
    reasons = []

    token_count = rec.get("token_count", 0)
    has_dialogue = rec.get("has_dialogue", False)
    coherence_flag = rec.get("coherence_flag")
    noun_ratio = rec.get("noun_ratio", 0.0)

    # --- KURAL A: Diyalog varsa (kısa bile olsa)
    if has_dialogue:
        reasons.append("has_dialogue")

    # --- KURAL B: Sahne geçişi / belirsizlik sinyali
    if coherence_flag in VALID_COHERENCE_FLAGS:
        reasons.append("coherence_flag")

    # --- KURAL C: Güçlü sahne (uzun blok)
    if token_count >= MIN_TOKEN_SCENE_STRONG:
        reasons.append("token_strong_scene")

    # --- KURAL D: Sessiz ama yoğun TASVİR (ASIL YENİ EK)
    if (
        not has_dialogue
        and token_count >= MIN_TOKEN_DESCRIPTIVE
        and noun_ratio >= MIN_NOUN_RATIO
    ):
        reasons.append("descriptive_block")

    rec["triage_candidate"] = bool(reasons)
    rec["triage_reasons"] = reasons
    rec["triage_stage"] = "05_00_record_normalization_and_selection"
    rec["triage_version"] = "scene_description_v2"

    return rec

# =========================================================
# MAIN ORCHESTRATOR
# =========================================================

def main():
    files = list(INPUT_DIR.glob("*.jsonl"))
    if not files:
        raise FileNotFoundError("stage_5_0 klasöründe jsonl dosyası bulunamadı.")

    for input_path in files:
        output_path = OUTPUT_DIR / input_path.name.replace(
            "stage_5_0", "stage_5_1"
        )

        records = []

        with input_path.open("r", encoding="utf-8") as fin:
            for line in fin:
                records.append(json.loads(line))

        # ---- FAZ 1: ID NORMALIZATION
        records = normalize_micro_block_ids(records)

        # ---- FAZ 2: SCENE-DESCRIPTION SELECTION
        records = [apply_triage(r) for r in records]

        with output_path.open("w", encoding="utf-8") as fout:
            for rec in records:
                fout.write(json.dumps(rec, ensure_ascii=False) + "\n")

        total = len(records)
        normalized = sum(1 for r in records if r.get("id_normalized"))
        triaged = sum(1 for r in records if r.get("triage_candidate"))
        descriptive = sum(
            1 for r in records if "descriptive_block" in r.get("triage_reasons", [])
        )

        print(
            f"✅ {input_path.name} → {output_path.name} | "
            f"toplam: {total}, "
            f"id_normalized: {normalized}, "
            f"triage_candidate: {triaged}, "
            f"descriptive_blocks: {descriptive}"
        )

# =========================================================

if __name__ == "__main__":
    main()
