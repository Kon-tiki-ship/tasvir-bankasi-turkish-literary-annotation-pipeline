from pathlib import Path
import json

# =====================================================
# CONFIG
# =====================================================

INPUT_DIR = Path("data/stage_4_1")
OUTPUT_DIR = Path("data/stage_4_2")
OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

SIM_THRESHOLD = 0.75
DIALOGUE_JUMP = 0.25
LONG_TOKEN_THRESHOLD = 800

# =====================================================
# CORE
# =====================================================

input_files = sorted(INPUT_DIR.glob("*.jsonl"))

if not input_files:
    raise FileNotFoundError(
        f"{INPUT_DIR.resolve()} içinde jsonl dosyası bulunamadı."
    )

for input_path in input_files:
    print(f"▶ İşleniyor: {input_path.name}")

    output_path = OUTPUT_DIR / input_path.name.replace(
        ".jsonl", "_with_scene_updates.jsonl"
    )

    # -------------------------------------------------
    # 1️⃣ PARAGRAFLARI OKU (index → record)
    # -------------------------------------------------
    paragraphs = []
    index_map = {}

    with input_path.open("r", encoding="utf-8") as f:
        for line in f:
            p = json.loads(line)
            paragraphs.append(p)
            index_map[p["paragraph_index"]] = p

    if len(paragraphs) < 2:
        print("  ⚠ Yetersiz paragraf, atlandı.")
        continue

    # -------------------------------------------------
    # 2️⃣ SAHNE SİNYALLERİNİ HESAPLA VE GÜNCELLE
    # -------------------------------------------------
    updates = 0

    for i in range(1, len(paragraphs)):
        prev_p = paragraphs[i - 1]
        curr_p = paragraphs[i]

        signals = {}

        sim_prev = curr_p.get("sim_prev")
        if sim_prev is not None and sim_prev < SIM_THRESHOLD:
            signals["sim_prev"] = sim_prev

        dr_prev = prev_p.get("dialogue_char_ratio", 0.0)
        dr_curr = curr_p.get("dialogue_char_ratio", 0.0)
        if abs(dr_curr - dr_prev) >= DIALOGUE_JUMP:
            signals["dialogue_jump"] = True

        tense_prev = prev_p.get("tense_mode")
        tense_curr = curr_p.get("tense_mode")
        if tense_prev and tense_curr and tense_prev != tense_curr:
            signals["tense_change"] = True

        if curr_p.get("token_count", 0) >= LONG_TOKEN_THRESHOLD:
            signals["token_pressure"] = True

        if not signals:
            continue

        edge_payload = {
            "edge_id": f"p{prev_p['paragraph_index']}->p{curr_p['paragraph_index']}",
            "prev_p_idx": prev_p["paragraph_index"],
            "curr_p_idx": curr_p["paragraph_index"],
            "prev_text": prev_p["text"],
            "curr_text": curr_p["text"],
            "signals": signals,
            "candidate": True
        }

        # 🔥 UPDATE — paragrafın ÜZERİNE YAZ
        curr_p.setdefault("scene_edge", {})
        curr_p["scene_edge"].update(edge_payload)
        updates += 1

    # -------------------------------------------------
    # 3️⃣ AYNI DOSYAYA TEMİZCE YAZ
    # -------------------------------------------------
    with output_path.open("w", encoding="utf-8") as out:
        for p in paragraphs:
            out.write(json.dumps(p, ensure_ascii=False) + "\n")

    print(f"  ✔ {updates} paragraf güncellendi → {output_path.name}")

print("✅ Paragraf + sahne bilgileri TEK DOSYADA birleştirildi.")
