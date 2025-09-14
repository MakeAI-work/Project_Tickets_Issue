import json
import os
from typing import Dict

from dotenv import load_dotenv
from openai import OpenAI, BadRequestError

"""Ticket classifier

`classify_ticket(text) -> Dict[str, str]` returns a JSON-like dict with keys:
    topic, sentiment, priority

• uses GPT-3.5-turbo with a zero-temperature system prompt
• choices are constrained so downstream UI can rely on fixed categories
"""

load_dotenv()

_OPENAI_KEY = os.getenv("OPENAI_API_KEY")
if not _OPENAI_KEY:
    raise RuntimeError("OPENAI_API_KEY missing – set it in your environment or .env file")

client = OpenAI(api_key=_OPENAI_KEY)

_SYSTEM_PROMPT = (
    "You are an expert support-ticket classifier for a data-catalog product. "
    "Given a customer message, output strict JSON with the following keys: "
    "topic, sentiment, priority.\n\n"
    "Allowed topic values: How-to, Product, Connector, Lineage, API/SDK, SSO, "
    "Glossary, Best practices, Sensitive data.\n"
    "Allowed sentiment values: Frustrated, Curious, Angry, Neutral.\n"
    "Allowed priority values: P0 (High), P1 (Medium), P2 (Low).\n"
    "Rules:\n  – Only output JSON, no extra text.\n  – If urgency words like 'urgent', 'blocking', 'ASAP' appear, set priority to P0.\n  – If user complains loudly (e.g., 'infuriating', 'not working'), set sentiment Angry.\n  – How-to / Product questions usually P2 unless urgent.\n"
)


def _chat_completion(user_msg: str) -> str:
    """Wrapper that returns the assistant content string."""
    response = client.chat.completions.create(
        model="gpt-4o-mini",
        temperature=0.0,
        messages=[
            {"role": "system", "content": _SYSTEM_PROMPT},
            {"role": "user", "content": user_msg},
        ],
    )
    return response.choices[0].message.content.strip()


def classify_ticket(text: str) -> Dict[str, str]:
    """Return dict(topic, sentiment, priority) for the ticket text."""
    try:
        raw_json = _chat_completion(text)
        data = json.loads(raw_json)
        # basic validation
        for key in ("topic", "sentiment", "priority"):
            if key not in data:  # pragma: no cover
                raise ValueError(f"Missing key {key} in LLM response: {raw_json}")
        return {
            "topic": data["topic"],
            "sentiment": data["sentiment"],
            "priority": data["priority"],
        }
    except (json.JSONDecodeError, BadRequestError, ValueError):
        # fallback safe defaults
        return {"topic": "Product", "sentiment": "Neutral", "priority": "P2"}


if __name__ == "__main__":
    # quick manual test
    sample = "URGENT: Connector failed to crawl Snowflake."
    print(classify_ticket(sample))
