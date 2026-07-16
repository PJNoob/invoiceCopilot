# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project

This repo is a 7-day portfolio sprint building an Invoice/Receipt Copilot: OCR + LLM extraction → eval harness (LangSmith) → LoRA fine-tune → deployed FastAPI endpoint → SQL anomaly detection. The full day-by-day plan, scope, assumptions, and success criteria live in `plan.md` — read it before starting work in this repo.

**Keep `plan.md` in sync**: check off `[ ]` action items as `[x]` once they're actually completed (code written and run, not just started).

## Environment

- Python via `venv` + `requirements.txt` (no poetry/uv/conda).
- API keys (OpenRouter/HuggingFace, LangSmith, W&B) go in a `.env` file (gitignored) loaded via `python-dotenv` — never hardcode keys or commit them.

## Structure (per plan.md)

- `src/` — pipeline code (`ocr.py`, `extract.py`, `qa.py`, `anomaly.py`)
- `data/raw/`, `data/eval/`, `data/train/` — sample docs, hand-labeled eval set, fine-tuning data
- `eval/score.py` — field-level accuracy scoring against `data/eval/labels.json`
- `notebooks/` — Colab/Kaggle fine-tuning notebook
- `deploy/` — FastAPI app (`app.py`) and SageMaker stretch-goal script
- `results/` — dated output snapshots (e.g. `day2_baseline/`, `day5_finetune_vs_baseline.md`)
- `notes/` — running notes and the Day 4-5 debugging log
- `walkthrough.md`, `interview_answers.md` — final write-up deliverables

## Notes

- This is a scoped learning sprint, not a production build — favor the simplest thing that demonstrably works over robustness or abstraction.
- Free-tier LLM APIs (OpenRouter/HF) can rate-limit or return malformed JSON; extraction code should handle retries/malformed output rather than assuming clean responses.
- Per the plan's risk notes, protect Day 4-5 fine-tuning if a day runs long — SageMaker deployment (Day 6) is a stretch goal, not required.
