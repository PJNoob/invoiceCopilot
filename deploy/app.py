"""Day 6: FastAPI deployment wrapper.

Exposes the extraction and QA pipeline over HTTP: `/extract` (OCR + LLM
extraction) and `/qa` (grounded question answering). This is the
guaranteed Day 6 deliverable; `sagemaker_deploy.py` is the stretch goal.
"""

from __future__ import annotations

from fastapi import FastAPI

from src.schema import InvoiceExtraction

app = FastAPI(title="Invoice/Receipt Copilot")


@app.post("/extract", response_model=InvoiceExtraction)
def extract(file_bytes: bytes) -> InvoiceExtraction:
    # TODO(day6): run src.ocr.extract_text then src.extract.extract_invoice
    raise NotImplementedError


@app.post("/qa")
def qa(question: str, file_bytes: bytes) -> dict:
    # TODO(day6): run src.ocr.extract_text then src.qa.answer_question
    raise NotImplementedError
