"""Day 6 stretch goal: SageMaker real-time endpoint deploy.

Only pursued if AWS account/billing setup doesn't eat the day — the local
FastAPI endpoint (`deploy/app.py`) is the guaranteed deliverable. This
script is a stub outline of what `HuggingFaceModel.deploy()` would look
like; see `notes/day6_sagemaker_notes.md` for the accompanying write-up.
"""

from __future__ import annotations


def deploy() -> None:
    # TODO(day6, stretch): construct a HuggingFaceModel pointing at the
    # fine-tuned model artifacts and call .deploy() for a real-time
    # inference endpoint. Requires an AWS account with SageMaker access.
    raise NotImplementedError


if __name__ == "__main__":
    deploy()
