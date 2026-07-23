# Day 1: LLM Fundamentals

Own-words notes on the four things I need to be able to explain fluently without
looking at this file: tokenization, attention, context window, and decoding.
Written with the Day 2 extraction task in mind (prompting an LLM to return
structured JSON from OCR'd invoice text).

## Tokenization

A model doesn't see words or characters — it sees tokens, which are chunks of
text produced by a subword algorithm (BPE / byte-pair encoding, or a variant
like SentencePiece/WordPiece). The vocabulary is built by starting from
individual bytes/characters and iteratively merging the most frequent adjacent
pairs until it hits a target vocab size (commonly 30k-150k tokens). Common
words end up as a single token ("the", "invoice"); rare or made-up words get
split into pieces ("Qwen2.5" might become "Qw" + "en" + "2" + "." + "5").

Why it matters practically:
- **Cost and context budget** are measured in tokens, not characters or words.
  A rough rule of thumb for English is ~4 characters/token, but numbers,
  punctuation-heavy text (like invoice line items: "$1,234.56") and non-English
  text tokenize less efficiently, so OCR'd receipts can burn more tokens than
  the raw character count suggests.
- **The model can't "see" inside a token** the way it sees a token boundary.
  This is why LLMs are historically bad at character-level tasks (counting
  letters, reversing strings) — those operations cross token boundaries the
  model was never trained to reason about directly.
- For structured extraction, this means field values like dates, totals, and
  invoice numbers can get tokenized in inconsistent ways run-to-run depending
  on surrounding punctuation, which is part of why exact-match scoring
  (Day 3) needs some normalization, not raw string equality.

## Attention

Attention is the mechanism that lets each token in a sequence "look at" every
other token and decide how much to weight each one when building its own
representation. Concretely, each token produces three vectors: a **Query**
(what am I looking for), a **Key** (what do I contain, for others to match
against), and a **Value** (what do I actually contribute if selected). The
attention score between token A and token B is the dot product of A's query
and B's key (scaled and softmaxed into a probability distribution); the
output for A is the weighted sum of all tokens' values using those scores.

This is **self-attention** when queries/keys/values all come from the same
sequence (e.g. a token in the invoice text attending to other tokens in the
same invoice text) — this is what GPT-style decoder-only models use
throughout. **Cross-attention** is when queries come from one sequence and
keys/values come from another (e.g. classic encoder-decoder translation
models, where the decoder attends over the encoder's output) — less relevant
for the decoder-only chat models this project uses, but useful to know exists.

Why attention replaced recurrence (RNN/LSTM): RNNs process tokens sequentially
and compress everything seen so far into a fixed-size hidden state, so
information from early in a long sequence has to survive many sequential
updates to influence a later token — it degrades over distance. Attention
gives every token a **direct, one-step path** to every other token regardless
of distance, and because there's no sequential dependency between tokens
during training, it's fully parallelizable on GPUs. That parallelism is the
practical reason transformers scaled so much faster than RNNs.

Multi-head attention just runs several attention operations in parallel with
different learned Q/K/V projections, so different heads can specialize (one
head might track syntactic structure, another might track "which number is
the total" in an invoice-like layout) — the outputs get concatenated and
projected back down.

## Context Window

The context window is the maximum number of tokens (input + output combined,
for most APIs) the model can attend over in one call. It's not just a
convenience limit — attention is (naively) quadratic in sequence length
(O(n²) in compute and memory, since every token attends to every other
token), so context window size is a real architectural/cost constraint, not
an arbitrary product decision, though newer models use various tricks
(sliding window, sparse/linear attention approximations) to push this out
cheaper than naive quadratic scaling would suggest.

Practical tradeoffs for this project:
- A long, multi-page invoice's OCR'd text plus the extraction prompt plus the
  JSON schema instructions all have to fit in the input budget, with room left
  for the output JSON.
- Stuffing too much irrelevant OCR noise (headers, boilerplate legal text) into
  the prompt wastes context budget and can genuinely degrade extraction
  accuracy — models don't attend uniformly well across very long, noisy
  contexts ("lost in the middle" effects are well documented).
- This is the practical argument for keeping OCR preprocessing reasonably
  clean (Day 2's `ocr.py`) rather than just dumping raw OCR output at the
  model and hoping attention sorts it out.

## Decoding Strategies

Once the model produces a probability distribution over the next token, a
decoding strategy decides which token to actually emit. This choice is
directly relevant to Day 2's structured JSON extraction, since decoding
determines how deterministic and well-formed the output is.

- **Greedy decoding**: always pick the single highest-probability token at
  each step. Fully deterministic, fastest, but can get stuck in repetitive or
  locally-optimal-but-globally-bad outputs, and can't recover from an early
  suboptimal choice. For structured extraction where I want the same input to
  reliably produce the same JSON, greedy (or low-temperature sampling close
  to greedy) is usually the right default.
- **Sampling (temperature / top-p / top-k)**: instead of always taking the
  argmax, sample from the (reshaped) probability distribution.
  - *Temperature* scales the logits before softmax — lower temperature
    (<1.0) sharpens the distribution toward the top choices (closer to
    greedy), higher temperature (>1.0) flattens it (more random/creative).
  - *Top-k* restricts sampling to only the k highest-probability tokens.
  - *Top-p (nucleus sampling)* restricts sampling to the smallest set of
    tokens whose cumulative probability exceeds p, which adapts the
    candidate pool size to how "confident" the distribution is at each step.
  - Good for open-ended generation (QA answers, Day 2's `qa.py`) where some
    variation in phrasing is fine or even desirable, but risky for strict
    JSON output — temperature > 0 is part of why malformed JSON happens, and
    part of why `extract.py` needs to handle retries/malformed output per
    CLAUDE.md.
- **Beam search**: instead of committing to one token at each step, keep the
  top-k most probable *sequences* (beams) at every step and expand each,
  pruning back down to k after each step, finally returning the
  highest-scoring complete sequence. Produces more globally coherent output
  than greedy for tasks like translation/summarization, but is expensive
  (k× the forward passes), less commonly exposed on hosted inference APIs
  for chat models, and doesn't obviously help structured extraction over
  just using greedy/low-temperature decoding with a schema-constrained
  prompt.

**Takeaway for this project**: Day 2's extraction step should default to
greedy or near-zero temperature for reproducibility and JSON-validity, while
`qa.py`'s free-form answers can tolerate (or even benefit from) a bit more
temperature.
