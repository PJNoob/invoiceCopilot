"""Day 3: Field-level evaluation scorer.

Compares predicted `InvoiceExtraction` output against hand-labeled gold
data in `data/eval/labels.json`, computing per-field exact-match accuracy
and an aggregate score, plus manually tagged failure types (wrong field,
hallucinated value, missed field).
"""

from __future__ import annotations

import argparse
import json
from pathlib import Path

from src.schema import InvoiceExtraction


def score_field(pred: object, gold: object) -> bool:
    # TODO(day3): exact-match comparison, with normalization for dates/
    # currency formatting as needed.
    raise NotImplementedError


def score_all(preds_path: Path, labels_path: Path) -> dict:
    # TODO(day3): load predictions + gold labels, score per field,
    # aggregate, and tag failure types.
    raise NotImplementedError


def main() -> None:
    parser = argparse.ArgumentParser(description="Score extraction predictions against gold labels")
    parser.add_argument("preds_path", type=Path)
    parser.add_argument("labels_path", type=Path, default=Path("data/eval/labels.json"), nargs="?")
    parser.add_argument("--output", type=Path, default=None, help="Where to write the scored results JSON")
    args = parser.parse_args()
    raise NotImplementedError


if __name__ == "__main__":
    main()
