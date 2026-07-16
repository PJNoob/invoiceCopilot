"""Shared extraction schema.

Single source of truth for the invoice/receipt extraction shape. Reused by
`src/extract.py` (validating LLM output), `eval/score.py` (comparing
predictions against hand-labeled gold data), and the Day 4-5 fine-tuning data
prep (target JSON shape for training pairs) — defined once here so all three
stay in sync.
"""

from __future__ import annotations

from typing import Optional

from pydantic import BaseModel


class LineItem(BaseModel):
    description: str
    quantity: Optional[float] = None
    unit_price: Optional[float] = None
    amount: Optional[float] = None


class InvoiceExtraction(BaseModel):
    vendor: Optional[str] = None
    invoice_date: Optional[str] = None
    invoice_number: Optional[str] = None
    total: Optional[float] = None
    tax: Optional[float] = None
    line_items: list[LineItem] = []
