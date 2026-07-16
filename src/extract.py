"""Day 2: LLM-prompted structured extraction.

Prompts a free-tier model (via OpenRouter, OpenAI-compatible SDK) to return
structured JSON matching `src.schema.InvoiceExtraction`, with handling for
malformed/non-JSON model output.
"""

from __future__ import annotations

import argparse
from pathlib import Path

from src.schema import InvoiceExtraction


def extract_invoice(ocr_text: str) -> InvoiceExtraction:
    # TODO(day2): build extraction prompt against the InvoiceExtraction
    # schema, call the configured model, parse/repair JSON output.
    raise NotImplementedError


def main() -> None:
    parser = argparse.ArgumentParser(description="Run structured extraction over OCR'd docs")
    parser.add_argument("input_dir", type=Path, help="Directory of OCR .txt files")
    parser.add_argument("output_dir", type=Path, help="Directory to write extracted JSON")
    args = parser.parse_args()
    raise NotImplementedError


if __name__ == "__main__":
    main()
