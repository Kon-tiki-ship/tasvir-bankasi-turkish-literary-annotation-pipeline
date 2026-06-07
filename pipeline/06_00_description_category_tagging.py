from __future__ import annotations

from pathlib import Path
import json
import re
from typing import Callable

INPUT_DIR = Path("data/stage_5_2")
OUTPUT_DIR = Path("data/stage_5_4")
OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

LEXICAL_RULES = {
    "descr_human": {
        "keywords": [
            "yuz",
            "goz",
            "bakis",
            "sac",
            "biyik",
            "kirisik",
            "el",
            "eller",
            "vucut",
            "boy",
            "omuz",
            "durus",
            "kiyafet",
            "elbise",
            "ceket",
            "palto",
        ]
    },
    "descr_emotion": {
        "keywords": [
            "utan",
            "kork",
            "sevin",
            "mutlu",
            "uzgun",
            "bosluk",
            "heyecan",
            "kaygi",
            "huzun",
            "ofke",
            "mahcup",
        ]
    },
    "descr_location": {
        "keywords": [
            "oda",
            "sokak",
            "ev",
            "salon",
            "koridor",
            "bar",
            "meydan",
            "pansiyon",
            "bina",
        ]
    },
    "descr_nature": {
        "keywords": [
            "yagmur",
            "kar",
            "ruzgar",
            "hava",
            "agac",
            "orman",
            "gol",
            "cicek",
            "toprak",
        ]
    },
    "descr_action": {
        "keywords": [
            "yurudu",
            "kostu",
            "tuttu",
            "yaklasti",
            "cekildi",
            "bakindi",
            "kacti",
            "oturdu",
            "kalkti",
        ]
    },
    "descr_object": {
        "keywords": [
            "masa",
            "sandalye",
            "dolap",
            "defter",
            "kitap",
            "havlu",
            "catal",
            "esya",
            "lamba",
        ]
    },
    "descr_psychology": {
        "keywords": [
            "dusundum",
            "hissettim",
            "aklimdan",
            "zannettim",
            "fark ettim",
            "bana gore",
            "kanimca",
        ]
    },
    "descr_metaphor": {"keywords": ["gibi", "sanki", "adeta", "misali"]},
}

TOKEN_PATTERN = re.compile(r"[A-Za-zCÇGĞIİOÖSŞUÜa-zcçgğiıoösşuü]+", re.UNICODE)


def tr_lower(text: str) -> str:
    return text.translate(str.maketrans({"I": "ı", "İ": "i"})).lower()


def fold_turkish(text: str) -> str:
    mapping = str.maketrans(
        {
            "ç": "c",
            "ğ": "g",
            "ı": "i",
            "ö": "o",
            "ş": "s",
            "ü": "u",
            "Ç": "c",
            "Ğ": "g",
            "İ": "i",
            "I": "i",
            "Ö": "o",
            "Ş": "s",
            "Ü": "u",
        }
    )
    return tr_lower(text).translate(mapping)


def tokenize_folded(text: str) -> list[str]:
    return [fold_turkish(match.group(0)) for match in TOKEN_PATTERN.finditer(text)]


def _short_root_matcher(root: str, allowed_next: set[str]) -> Callable[[str], bool]:
    def match(token: str) -> bool:
        if not token.startswith(root):
            return False
        if token == root:
            return True
        if len(token) == len(root):
            return True
        next_char = token[len(root)]
        return next_char in allowed_next

    return match


SHORT_ROOT_MATCHERS: dict[str, Callable[[str], bool]] = {
    # keep: ev, evde, eve, evin, evler; reject: grev, evvel
    "ev": _short_root_matcher("ev", {"d", "t", "e", "i", "u", "l", "m", "n", "s", "y"}),
    # keep: el, elini, eliyle, elinde, eller; reject: otel, guzel
    "el": _short_root_matcher("el", {"i", "u", "l", "d", "t", "e", "a", "y"}),
    # keep: kar, karda, karda, karlı; reject: karar, karsi, karimi
    "kar": _short_root_matcher("kar", {"d", "t", "l", "y"}),
    # keep: bar, barda; reject: ibaret, beraber
    "bar": _short_root_matcher("bar", {"d", "t", "a", "i", "u", "l", "y"}),
    # keep: gol, golde; reject: golge
    "gol": _short_root_matcher("gol", {"d", "t", "l", "s", "y", "u", "i", "e", "a"}),
    # keep: boy, boyu, boyun; reject: boyanmis
    "boy": _short_root_matcher("boy", {"u", "i", "l", "d", "t", "s", "y"}),
    # keep: goz, gozleri; reject broad substring side effects
    "goz": _short_root_matcher("goz", {"u", "l", "d", "t", "e", "a", "i", "y"}),
}


def _match_single_keyword(tokens: list[str], normalized_text: str, keyword: str) -> bool:
    normalized_keyword = fold_turkish(keyword)
    if " " in normalized_keyword:
        return normalized_keyword in normalized_text

    if normalized_keyword == "ev":
        blocked_prefixes = ("evlat", "evlilik", "evvel")
        allowed_prefixes = ("evde", "evden", "eve", "evin", "evi", "evim", "evimiz", "evler", "evlere", "evlerde", "evlerden")
        return any(token == "ev" or token.startswith(allowed_prefixes) for token in tokens if not token.startswith(blocked_prefixes))

    if normalized_keyword == "el":
        allowed_prefixes = (
            "el",
            "eli",
            "elin",
            "eline",
            "elinde",
            "elini",
            "eliyle",
            "elim",
            "elimiz",
            "eller",
            "elleri",
            "ellerin",
            "ellerine",
            "elleriyle",
            "elden",
        )
        blocked_prefixes = ("elektr", "ellilik", "ellik", "elma")
        return any(
            (token == "el" or token.startswith(allowed_prefixes)) and not token.startswith(blocked_prefixes)
            for token in tokens
        )

    if normalized_keyword == "yuz":
        money_units = {"lira", "kurus", "tl"}
        number_tokens = {
            "bir",
            "iki",
            "uc",
            "dort",
            "bes",
            "alti",
            "yedi",
            "sekiz",
            "dokuz",
            "on",
            "yirmi",
            "otuz",
            "kirk",
            "elli",
            "altmis",
            "yetmis",
            "seksen",
            "doksan",
            "yuz",
            "bin",
        }
        for i, token in enumerate(tokens):
            if token not in {"yuz", "yuzu"} and not token.startswith(("yuzu", "yuzun", "yuzler")):
                continue
            prev_token = tokens[i - 1] if i > 0 else ""
            next_token = tokens[i + 1] if i + 1 < len(tokens) else ""
            if token == "yuz" and (next_token in money_units or prev_token in number_tokens):
                continue
            return True
        return False

    if normalized_keyword == "bar":
        allowed_prefixes = ("barda", "bardan", "bara", "barin", "barlar", "barlara", "barlarda")
        return any(token == "bar" or token.startswith(allowed_prefixes) for token in tokens)

    if normalized_keyword == "boy":
        return any(token == "boy" or token == "boyu" or token.startswith("boylu") for token in tokens)

    if normalized_keyword == "goz":
        return any(token == "goz" or token == "gozu" or token.startswith("gozler") for token in tokens)

    if normalized_keyword == "kar":
        allowed_prefixes = ("kar", "karda", "kardan", "karli", "karla", "karlik")
        blocked_prefixes = ("kari", "karim", "karis", "karar", "karsi", "karahisar", "karanl", "kara", "kardes")
        return any(
            (token == "kar" or token.startswith(allowed_prefixes)) and not token.startswith(blocked_prefixes)
            for token in tokens
        )

    if normalized_keyword == "yagmur":
        blocked_prefixes = ("yagmurluk",)
        return any(
            (token == "yagmur" or token.startswith(("yagmurlu", "yagmura", "yagmurda", "yagmurun")))
            and not token.startswith(blocked_prefixes)
            for token in tokens
        )

    if normalized_keyword == "tuttu":
        blocked_prefixes = ("tutturul", "tutturmus", "tutturulmus")
        return any(
            (token == "tuttu" or token.startswith(("tuttu", "tutup", "tutunca")))
            and not token.startswith(blocked_prefixes)
            for token in tokens
        )

    if normalized_keyword == "cicek":
        decor_context_tokens = {"motif", "motifli", "cizili", "cizilmis", "oyuncak", "gemi", "yaldizli", "uzerine", "uzerindeki"}
        has_decor_context = any(token in decor_context_tokens for token in tokens)
        if has_decor_context:
            return False
        return any(token == "cicek" or token.startswith(("cicekler", "cicegi", "cicegin", "cicekte")) for token in tokens)

    matcher = SHORT_ROOT_MATCHERS.get(normalized_keyword)
    if matcher:
        return any(matcher(token) for token in tokens)

    return any(token.startswith(normalized_keyword) for token in tokens)


def extract_reasons(text: str, keywords: list[str]) -> list[str]:
    reasons = set()
    normalized_text = fold_turkish(text)
    tokens = tokenize_folded(text)
    for keyword in keywords:
        if _match_single_keyword(tokens, normalized_text, keyword):
            reasons.add(fold_turkish(keyword))
    return sorted(reasons)


def build_descriptive_profile(text: str) -> list[dict]:
    profile: list[dict] = []
    for category, rule in LEXICAL_RULES.items():
        reasons = extract_reasons(text, rule["keywords"])
        if reasons:
            profile.append({"category": category, "reasons": reasons})
    return profile


def run_pipeline(input_dir: Path = INPUT_DIR, output_dir: Path = OUTPUT_DIR) -> None:
    output_dir.mkdir(parents=True, exist_ok=True)
    for input_path in input_dir.glob("*.jsonl"):
        print(f"[05_4] Descriptive tagging: {input_path.name}")
        output_path = output_dir / input_path.name.replace(".jsonl", "_descriptive.jsonl")

        with input_path.open("r", encoding="utf-8") as handle:
            records = [json.loads(line) for line in handle if line.strip()]

        for record in records:
            text = (record.get("text") or "").strip()
            if not text:
                continue
            profile = build_descriptive_profile(text)
            if profile:
                record["descriptive_profile"] = profile
            elif "descriptive_profile" in record:
                del record["descriptive_profile"]

        with output_path.open("w", encoding="utf-8") as out:
            for record in records:
                out.write(json.dumps(record, ensure_ascii=False) + "\n")

        print(f"[05_4] Written: {output_path.name}")

    print("[05_4] Completed.")


if __name__ == "__main__":
    run_pipeline()
