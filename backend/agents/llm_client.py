from functools import lru_cache
from config.settings import settings


@lru_cache(maxsize=1)
def _get_client():
    from groq import Groq
    return Groq(api_key=settings.GROQ_API_KEY)


def call_llm(system_prompt: str, user_prompt: str) -> str:
    """Returns the model's plain-text response. Callers should catch exceptions
    (e.g. missing API key, network issues) and degrade gracefully."""
    client = _get_client()
    response = client.chat.completions.create(
        model=settings.LLM_MODEL,
        max_tokens=settings.LLM_MAX_TOKENS,
        messages=[
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": user_prompt},
        ],
    )
    return response.choices[0].message.content.strip()