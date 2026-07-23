# Plan: Invoice/Receipt Copilot — 7-Day Build

Build a working Invoice/Receipt Copilot end to end in one week: OCR + prompted extraction baseline → eval harness with LangSmith tracing → LoRA fine-tune of the extraction step → deployed endpoint → SQL-based anomaly detection. This is a scoped learning/portfolio sprint, not a production build — each day ends with something real and demoable, and the write-up at the end is as important as the code.

## Scope

**In:**
- OCR + LLM-prompted structured extraction (vendor, date, total, tax, line items) via a free-tier API (OpenRouter or HuggingFace Inference API)
- Simple grounded QA over an extracted document
- Hand-labeled eval set (20-30 docs) with a field-level scoring script
- LangSmith tracing of pipeline calls
- LoRA fine-tune of the extraction task on a small open model (Colab/Kaggle free GPU), tracked in Weights & Biases
- Baseline-vs-fine-tuned comparison on the eval set
- A deployed endpoint (local FastAPI primary; SageMaker real-time endpoint as a stretch goal)
- SQL-based anomaly detection (duplicate invoice numbers, tax-rate outliers) over a SQLite table
- A written walkthrough and "what I'd do differently at scale" answers

**Out (explicitly, per source doc's cut list):**
- DPO/RLHF implementation
- True VLM (LLaVA/Qwen-VL) — OCR+LLM only
- Quantization benchmarking (unless Day 6-7 have slack)
- LangGraph / multi-agent orchestration (one simple router step, if any, is enough)
- SageMaker Pipelines, autoscaling, batch transform

## Success Criteria

- One script/command runs the full loop: PDF in → extracted JSON → QA answer → anomaly flags out, on a fresh sample not in the eval set
- `results/` contains a documented baseline accuracy number (Day 2/3) and a fine-tuned accuracy number (Day 5) on the same eval set, with at least one concrete before/after example
- LangSmith shows at least one traced pipeline run
- Weights & Biases shows at least one fine-tuning run with a loss curve
- A deployed endpoint (FastAPI, and SageMaker if reached) returns a real response to a real request, captured as a log/screenshot
- The anomaly check fires correctly on at least one injected duplicate invoice number and one tax-rate outlier
- `walkthrough.md` and `interview_answers.md` exist and can carry a 5-minute crisp narrative without notes

## Assumptions

- Baseline pipeline (Days 1-3) calls a free-tier API model via OpenRouter (OpenAI-compatible SDK) or the HuggingFace Inference API — exact free model chosen at setup time based on availability/rate limits, and swappable without touching the rest of the pipeline
- Fine-tuning target model is Qwen2.5-1.5B-Instruct (small enough for a free Colab/Kaggle T4 GPU with LoRA); may swap to Llama-3.2-1B/3B-Instruct if tokenizer/template issues make Qwen impractical
- No AWS account exists yet, so Day 6's primary, guaranteed deliverable is a local FastAPI endpoint; a real SageMaker `HuggingFaceModel.deploy()` attempt is a stretch goal only pursued if account/billing setup doesn't eat the day
- Anomaly storage is SQLite (no server setup needed)
- Standard Python project layout in this repo: venv + `requirements.txt`, code under `src/`, sample/eval data under `data/`, outputs under `results/`, running notes under `notes/`
- Dataset is sourced fresh on Day 2 from a public Kaggle sample invoice/receipt dataset (15-20 docs for baseline, expanded to a 20-30 doc hand-labeled eval set on Day 3, and a 50-100 example synthetic/augmented set for fine-tuning on Day 4-5)

## Action Items

### Day 1 — LLM fundamentals + environment
- [ ] Read/watch one solid attention + transformer walkthrough (2-3 hrs); jot down anything unclear
- [x] Set up the Python project: venv, `requirements.txt` (transformers, an OpenAI-SDK-compatible client for OpenRouter, pdfplumber, pytesseract, python-dotenv, pydantic)
- [x] Get a free OpenRouter (or HF Inference API) key; verify access with one test call to a free model
- [x] Write `notes/day1_fundamentals.md`: your own-words explanation of tokenization, attention, context window, and greedy/sampling/beam decoding — read it aloud until it's fluent without notes

### Day 2 — Baseline pipeline (no fine-tuning yet)
- [ ] Source 15-20 sample invoices/receipts from a public dataset (e.g. Kaggle) into `data/raw/`
- [ ] Build `src/ocr.py`: extract text via pdfplumber, with pytesseract fallback for scanned/image PDFs
- [ ] Build `src/extract.py`: prompt the LLM to return structured JSON (vendor, date, total, tax, line items) against a pydantic schema; handle malformed/non-JSON output
- [ ] Build `src/qa.py`: answer ad-hoc questions ("what's the total payable?") grounded in the OCR'd text
- [ ] Run the pipeline over all sample docs and save outputs to `results/day2_baseline/` as the Stage-1 baseline snapshot

### Day 3 — Evaluation harness + LangSmith
- [ ] Sign up for LangSmith (free tier); get API key
- [ ] Wrap `extract.py` and `qa.py` calls with LangSmith tracing
- [ ] Hand-label a 20-30 doc eval set (ground-truth vendor/date/total/tax/items) into `data/eval/labels.json`
- [ ] Write `eval/score.py`: field-level exact-match accuracy per field + aggregate accuracy, and manually tag failure types (wrong field, hallucinated value, missed field)
- [ ] Run the scorer against the Day 2 baseline and save results to `results/day3_eval_baseline.json`
- [ ] If time allows, push the eval set as a LangSmith dataset and log an experiment; otherwise be ready to explain what LangSmith adds (versioned prompts, comparable runs, production trace inspection) without having built it

### Day 4-5 — Fine-tuning (highest-leverage, riskiest days — see risk note below)
- [ ] Set up a Colab/Kaggle notebook with GPU runtime: `notebooks/finetune_lora.ipynb`
- [ ] Build training data: convert the eval set plus a synthetic/augmented set (50-100 examples total) into input=OCR text / output=structured JSON pairs, saved as `data/train/finetune_data.jsonl`
- [ ] Load Qwen2.5-1.5B-Instruct via transformers; fine-tune with `peft` LoRA on the extraction task
- [ ] Wire up Weights & Biases (`wandb.init()`) and confirm a loss curve logs during training
- [ ] Save the LoRA adapter weights (download locally or persist to Drive)
- [ ] Run the fine-tuned model over the same Day 3 eval set using `eval/score.py`; save to `results/day5_finetune_vs_baseline.md` with the accuracy comparison and at least one concrete before/after example
- [ ] Log every real error hit (tokenization mismatches, prompt template formatting, LoRA rank/alpha issues, OOM) and the actual fix in `notes/day4_5_debugging_log.md` — this is deliberately part of the deliverable, not cleanup

### Day 6 — Deployment (minimum viable)
- [ ] Build `deploy/app.py`: FastAPI wrapper exposing `/extract` and `/qa` around the fine-tuned (or base) pipeline — this is the guaranteed deliverable for the day
- [ ] Send a real request to the local endpoint and capture the request/response (log or screenshot) into `results/day6_deployment/`
- [ ] Stretch, only if AWS account/billing gets set up without derailing the day: write `deploy/sagemaker_deploy.py` using `HuggingFaceModel.deploy()`, attempt a real-time SageMaker endpoint, and capture a successful invoke
- [ ] Write `notes/day6_sagemaker_notes.md` describing exactly what a full SageMaker Training Job + real-time Endpoint path would look like, accurate enough to defend under follow-up questions even if not executed

### Day 7 — Anomaly detection + polish + your story
- [ ] Create a SQLite table (`data/invoices.db`) storing extracted fields per processed invoice
- [ ] Write `src/anomaly.py`: SQL queries flagging (a) duplicate invoice numbers and (b) tax-rate outliers via statistics, not LLM judgment
- [ ] Wire the anomaly check into the pipeline after extraction; run over the full sample set, injecting one synthetic duplicate to prove the check actually fires
- [ ] Run a final end-to-end smoke test on 2-3 fresh invoices not in the eval set: PDF in → extraction → QA → anomaly flags out, no crashes
- [ ] Write `walkthrough.md`: the 5-minute narrative (baseline → eval harness → fine-tuning result → deployment → what you'd build next: VLM, DPO, quantization, LangGraph agent)
- [ ] Write `interview_answers.md`: 3 specific "what would you do differently at scale" answers (batch transform, quantization, RLHF/DPO), described correctly even though not built

## Risk Notes

- **Riskiest task: Day 4-5 fine-tuning.** Free Colab/Kaggle GPU + LoRA is where tokenization mismatches, prompt template bugs, and OOM are most likely. Per the source doc's own fallback rule: if a day goes sideways, protect fine-tuning first — cut Day 6 down to "I called the SageMaker deploy function and can walk through the config" before cutting fine-tuning.
- **Free-tier API flakiness (Day 2-3):** OpenRouter/HF free models can rate-limit or degrade on structured JSON output. Budget time for retry logic or a model swap; don't treat the first model choice as fixed.
- **AWS friction (Day 6):** No AWS account exists yet, so SageMaker access/billing setup is a real risk to the day. The FastAPI fallback is written as the primary path, not an afterthought, specifically to avoid this blocking the day's success criteria.
