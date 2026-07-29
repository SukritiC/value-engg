import os
from pathlib import Path
from typing import Optional

try:
    from dotenv import load_dotenv
except ImportError:  # pragma: no cover - optional dependency
    load_dotenv = None

if load_dotenv is not None:
    load_dotenv(Path(__file__).resolve().parents[1] / ".env")

try:
    from openai import OpenAI
except ImportError:  # pragma: no cover - optional dependency
    OpenAI = None


def call_openai(prompt: str, api_key: Optional[str] = None, model: str = "gpt-4o-mini") -> Optional[str]:
    """Call the OpenAI API when a key is available; otherwise return None."""
    if not api_key and not os.getenv("OPENAI_API_KEY"):
        return None
    if OpenAI is None:
        return None
    try:
        client = OpenAI(api_key=api_key or os.getenv("OPENAI_API_KEY"))
        response = client.responses.create(model=model, input=prompt)
        return getattr(response, "output_text", None) or str(response)
    except Exception:
        return None
