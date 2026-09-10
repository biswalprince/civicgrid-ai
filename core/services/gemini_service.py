import json
import os
import re
from pathlib import Path
from typing import Any

import httpx
from google import genai
from google.genai import errors, types
from dotenv import load_dotenv


PROJECT_ROOT = Path(__file__).resolve().parents[2]
GEMINI_MODEL = "gemini-3.5-flash-lite"
ALLOWED_CATEGORIES = {
    "water",
    "roads",
    "schools",
    "sanitation",
    "electricity",
    "healthcare",
    "other",
}
REQUIRED_FIELDS = {
    "category",
    "location",
    "language",
    "severity",
    "affected_population",
    "infrastructure_gap",
    "vulnerability",
    "summary",
}

# Use an explicit path so this also works when Django is started from elsewhere.
# ``override=False`` preserves environment variables supplied by deployment tools.
load_dotenv(PROJECT_ROOT / ".env", override=False)


class GeminiServiceError(Exception):
    """Base exception for request-extraction failures safe to show to callers."""


class GeminiConfigurationError(GeminiServiceError):
    """Raised when Gemini has not been configured."""


class GeminiRequestError(GeminiServiceError):
    """Raised when Gemini cannot be reached or rejects a request."""


class GeminiResponseError(GeminiServiceError):
    """Raised when Gemini returns unusable structured data."""


REQUEST_DETAILS_SCHEMA = {
    "type": "object",
    "properties": {
        "category": {"type": "string", "enum": sorted(ALLOWED_CATEGORIES)},
        "location": {"type": "string"},
        "language": {"type": "string"},
        "severity": {"type": "integer", "minimum": 0, "maximum": 10},
        "affected_population": {"type": "integer", "minimum": 0, "maximum": 10},
        "infrastructure_gap": {"type": "integer", "minimum": 0, "maximum": 10},
        "vulnerability": {"type": "integer", "minimum": 0, "maximum": 10},
        "summary": {"type": "string"},
    },
    "required": sorted(REQUIRED_FIELDS),
    "additionalProperties": False,
}


def _get_client() -> genai.Client:
    api_key = os.getenv("GEMINI_API_KEY")
    if not api_key:
        raise GeminiConfigurationError("Gemini is not configured. Set GEMINI_API_KEY.")
    return genai.Client(api_key=api_key)


def _parse_response(response_text: str) -> dict[str, Any]:
    """Parse JSON responses, accepting a single Markdown JSON code fence."""
    if not isinstance(response_text, str):
        raise GeminiResponseError("Gemini returned no usable response text.")

    text = response_text.strip()
    fenced_json = re.fullmatch(r"```(?:json)?\s*(.*?)\s*```", text, re.DOTALL | re.IGNORECASE)
    if fenced_json:
        text = fenced_json.group(1).strip()

    try:
        details = json.loads(text)
    except (TypeError, json.JSONDecodeError) as exc:
        raise GeminiResponseError("Gemini returned invalid structured data.") from exc

    _validate_details(details)
    return details


def _validate_details(details: Any) -> None:
    if not isinstance(details, dict) or set(details) != REQUIRED_FIELDS:
        raise GeminiResponseError("Gemini returned an incomplete structured response.")

    if details["category"] not in ALLOWED_CATEGORIES:
        raise GeminiResponseError("Gemini returned an invalid request category.")

    for field in ("location", "language", "summary"):
        if not isinstance(details[field], str):
            raise GeminiResponseError("Gemini returned an invalid structured response.")

    for field in (
        "severity",
        "affected_population",
        "infrastructure_gap",
        "vulnerability",
    ):
        value = details[field]
        if isinstance(value, bool) or not isinstance(value, int) or not 0 <= value <= 10:
            raise GeminiResponseError("Gemini returned scores outside the allowed range.")


def extract_request_details(description: str) -> dict[str, Any]:
    prompt = f"""
You are an AI assistant for CivicGrid AI, a public infrastructure
decision-support platform.

Analyze this citizen request:

"{description}"

Return only valid JSON with these exact fields:

{{
    "category": "water|roads|schools|sanitation|electricity|healthcare|other",
    "location": "location mentioned in the request, or unknown",
    "language": "language of the request",
    "severity": integer from 0 to 10,
    "affected_population": integer from 0 to 10,
    "infrastructure_gap": integer from 0 to 10,
    "vulnerability": integer from 0 to 10,
    "summary": "short summary of the request"
}}

Do not include Markdown or explanations.
"""

    if not isinstance(description, str) or not description.strip():
        raise ValueError("description must be a non-empty string.")

    client = _get_client()
    try:
        try:
            response = client.models.generate_content(
                model=GEMINI_MODEL,
                contents=prompt,
                config=types.GenerateContentConfig(
                    response_mime_type="application/json",
                    response_json_schema=REQUEST_DETAILS_SCHEMA,
                ),
            )
        except httpx.HTTPError as exc:
            raise GeminiRequestError(
                "Gemini could not be reached. Check DNS, network access, and proxy settings."
            ) from exc
        except errors.APIError as exc:
            raise GeminiRequestError("Gemini API request failed.") from exc
    finally:
        client.close()

    try:
        response_text = response.text
    except (AttributeError, ValueError) as exc:
        raise GeminiResponseError("Gemini returned no usable response text.") from exc

    return _parse_response(response_text)
