from functools import lru_cache
from config.settings import settings


@lru_cache(maxsize=1)
def _get_client():
    import anthropic
    return anthropic.Anthropic(api_key=settings.ANTHROPIC_API_KEY)


def call_llm(system_prompt: str, user_prompt: str) -> str:
    """Returns the model's plain-text response. Callers should catch exceptions
    (e.g. missing API key, network issues) and degrade gracefully."""
    client = _get_client()
    response = client.messages.create(
        model=settings.LLM_MODEL,
        max_tokens=settings.LLM_MAX_TOKENS,
        system=system_prompt,
        messages=[{"role": "user", "content": user_prompt}],
    )
    return "".join(block.text for block in response.content if block.type == "text").strip()
