#!/usr/bin/env python3
"""Stage 01: clean raw text files and normalize paragraph boundaries.

The script uses relative defaults and can be configured with CLI arguments.
No local absolute paths are required; all input and output locations are supplied through relative defaults or explicit CLI arguments.

Examples:
    python pipeline/01_00_text_cleanup.py
    python pipeline/01_00_text_cleanup.py --input-dir data/raw_text --output-dir data/clean_text
"""

from __future__ import annotations

import argparse
from pathlib import Path
import re


ONLY_NUMBER_LINE = re.compile(r"^\s*\d+\s*$")
ONLY_SYMBOL_LINE = re.compile(r"^\s*[>*]+\s*$")

# Join words split by a real hyphen across a line break: "ke-\nli" -> "keli".
HYPHEN_BREAK = re.compile(
    r"([A-Za-zÇĞİÖŞÜçğıöşü]+)-\s*\n\s*([A-Za-zÇĞİÖŞÜçğıöşü]+)"
)

# Replace soft line breaks inside prose with one space.
SOFT_LINE_BREAK = re.compile(
    r"([A-Za-zÇĞİÖŞÜçğıöşü])\s*\n\s*([A-Za-zÇĞİÖŞÜçğıöşü])"
)


def process_file(input_path: Path, output_path: Path, encoding: str = "utf-8") -> int:
    """Clean a single text file and write normalized paragraphs.

    Returns:
        Number of paragraphs written.
    """
    raw = input_path.read_text(encoding=encoding, errors="ignore")
    raw = raw.replace("\r\n", "\n").replace("\r", "\n")

    raw = HYPHEN_BREAK.sub(r"\1\2", raw)
    raw = SOFT_LINE_BREAK.sub(r"\1 \2", raw)

    lines = raw.split("\n")
    paragraphs: list[str] = []
    buffer: list[str] = []
    pending_comma = False

    def flush() -> None:
        nonlocal buffer, pending_comma
        if buffer:
            paragraph = " ".join(buffer).strip()
            if paragraph:
                paragraphs.append(paragraph)
        buffer = []
        pending_comma = False

    for line in lines:
        stripped = line.strip()

        if ONLY_NUMBER_LINE.match(stripped):
            continue
        if ONLY_SYMBOL_LINE.match(stripped):
            continue

        if stripped == "":
            if pending_comma:
                continue
            flush()
            continue

        if stripped.startswith("—"):
            flush()
            buffer.append(stripped)
            pending_comma = stripped.endswith(",")
            continue

        buffer.append(stripped)
        pending_comma = stripped.endswith(",")

    flush()

    output_path.parent.mkdir(parents=True, exist_ok=True)
    output_path.write_text("\n\n".join(paragraphs), encoding=encoding)
    return len(paragraphs)


def build_output_name(input_name: str, old_suffix: str, new_suffix: str) -> str:
    if old_suffix and old_suffix in input_name:
        return input_name.replace(old_suffix, new_suffix)
    return input_name


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Clean raw text files and normalize paragraph boundaries."
    )
    parser.add_argument(
        "--input-dir",
        default="data/raw_text",
        help="Directory containing input .txt files. Default: data/raw_text",
    )
    parser.add_argument(
        "--output-dir",
        default="data/clean_text",
        help="Directory for cleaned .txt outputs. Default: data/clean_text",
    )
    parser.add_argument(
        "--encoding",
        default="utf-8",
        help="Text encoding for input and output files. Default: utf-8",
    )
    parser.add_argument(
        "--old-suffix",
        default="_ocr_text_without_footnotes",
        help="Filename fragment to replace in output names.",
    )
    parser.add_argument(
        "--new-suffix",
        default="_final",
        help="Replacement filename fragment for output names.",
    )
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    input_dir = Path(args.input_dir)
    output_dir = Path(args.output_dir)

    if not input_dir.exists():
        raise FileNotFoundError(f"Input directory does not exist: {input_dir}")

    txt_files = sorted(input_dir.glob("*.txt"))

    if not txt_files:
        print("No .txt files found.")
        return 0

    for txt_path in txt_files:
        output_name = build_output_name(txt_path.name, args.old_suffix, args.new_suffix)
        output_path = output_dir / output_name
        count = process_file(txt_path, output_path, encoding=args.encoding)
        print(f"{txt_path.name} -> {output_path.name} | paragraphs: {count}")

    print("All files completed.")
    print(f"Output directory: {output_dir}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
