# Invoice/Receipt Copilot

A 7-day portfolio sprint: OCR + LLM-prompted structured extraction → eval harness with LangSmith tracing → LoRA fine-tune of the extraction step → deployed FastAPI endpoint → SQL-based anomaly detection.

Full scope, assumptions, success criteria, and the day-by-day build plan live in [`plan.md`](plan.md) — read that first. Repo conventions for Claude Code sessions live in [`CLAUDE.md`](CLAUDE.md).

## Setup

```bash
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
cp .env.example .env  # then fill in your API keys
```

## Structure

- `src/` — pipeline code: `ocr.py`, `extract.py`, `qa.py`, `anomaly.py`, plus shared `schema.py` (pydantic extraction schema) and `config.py` (env/config loader)
- `eval/score.py` — field-level accuracy scoring against `data/eval/labels.json`
- `deploy/` — FastAPI app (`app.py`) and the SageMaker stretch-goal script
- `notebooks/` — Colab/Kaggle LoRA fine-tuning notebook
- `data/raw/`, `data/eval/`, `data/train/` — sample docs, hand-labeled eval set, fine-tuning data (gitignored contents, directories tracked)
- `results/` — dated output snapshots per day (baseline accuracy, fine-tune comparison, deployment logs)
- `notes/` — running notes and the Day 4-5 debugging log
- `walkthrough.md`, `interview_answers.md` — final write-up deliverables

## How to run

Filled in as each day's script becomes runnable — see `plan.md` for the day-by-day sequence.

## Deliverables

- [`walkthrough.md`](walkthrough.md) — the 5-minute narrative
- [`interview_answers.md`](interview_answers.md) — "what I'd do differently at scale" answers
