"""Day 2: OCR text extraction.

Extracts raw text from an invoice/receipt PDF via pdfplumber, falling back
to pytesseract for scanned/image-only PDFs where pdfplumber finds no text
layer.
"""

from __future__ import annotations

import argparse
from pathlib import Path


def extract_text(path: Path) -> str:
    # TODO(day2): try pdfplumber first; if no text extracted, rasterize
    # pages and fall back to pytesseract.
    raise NotImplementedError


def main() -> None:
    parser = argparse.ArgumentParser(description="Extract OCR text from PDFs")
    parser.add_argument("input_dir", type=Path, help="Directory of PDF files")
    parser.add_argument("output_dir", type=Path, help="Directory to write .txt files")
    args = parser.parse_args()
    raise NotImplementedError


if __name__ == "__main__":
    main()
