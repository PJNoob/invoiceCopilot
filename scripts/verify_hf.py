"""Day 1 sanity check: confirm HF_API_KEY/HF_MODEL from .env can reach the
HuggingFace Inference API with one real chat completion call.

HF's router requires an explicit inference *provider* per model (it doesn't
auto-select one) — this script looks up which providers currently serve the
configured model and tries each live one until a call succeeds.

Run: venv/bin/python3 scripts/verify_hf.py
"""

from __future__ import annotations

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from huggingface_hub import InferenceClient, model_info
from huggingface_hub.errors import HfHubHTTPError

from src import config

# Fallback models to try if HF_MODEL has no live provider.
FALLBACK_MODELS = [
    "Qwen/Qwen2.5-0.5B-Instruct",
    "meta-llama/Llama-3.2-1B-Instruct",
]


def live_providers(model_id: str) -> list[str]:
    info = model_info(
        model_id, expand=["inferenceProviderMapping"], token=config.HF_API_KEY
    )
    return [
        m.provider
        for m in (info.inference_provider_mapping or [])
        if m.status == "live" and m.task == "conversational"
    ]


def try_model(model: str) -> tuple[str, str] | None:
    providers = [config.HF_PROVIDER] if config.HF_PROVIDER else live_providers(model)
    for provider in providers:
        client = InferenceClient(api_key=config.HF_API_KEY, provider=provider)
        try:
            response = client.chat.completions.create(
                model=model,
                messages=[{"role": "user", "content": "Say OK and nothing else."}],
                max_tokens=10,
            )
            return provider, response.choices[0].message.content
        except HfHubHTTPError as e:
            print(f"  [{model} via {provider}] failed: {e}")
    return None


def main() -> None:
    if not config.HF_API_KEY or config.HF_API_KEY == "your_hf_api_key_here":
        raise SystemExit("HF_API_KEY not set in .env")

    models_to_try = [config.HF_MODEL] + [
        m for m in FALLBACK_MODELS if m != config.HF_MODEL
    ]

    for model in models_to_try:
        print(f"Trying model: {model}")
        result = try_model(model)
        if result is not None:
            provider, content = result
            print(f"\nSUCCESS with {model} via provider={provider}")
            print(f"Response: {content!r}")
            print(
                f"\nSet HF_MODEL={model} and HF_PROVIDER={provider} in .env "
                "to reuse this in extract.py/qa.py."
            )
            return

    raise SystemExit(
        "No configured or fallback model has a live conversational provider. "
        "Check your token or try a different model."
    )


if __name__ == "__main__":
    main()
