from __future__ import annotations

import os
from dataclasses import dataclass


@dataclass(frozen=True)
class Settings:
    api_key: str = os.getenv("GENAI_EVAL_API_KEY", "")
    requests_per_minute: int = int(os.getenv("GENAI_EVAL_REQUESTS_PER_MINUTE", "30"))
    pass_threshold: float = float(os.getenv("GENAI_EVAL_PASS_THRESHOLD", "0.80"))


settings = Settings()
