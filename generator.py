
from google.genai import types
from pydantic import ValidationError

from config import client, MODEL_NAME
from prompts import build_prompt
from models import MarketingCopyRequest, MarketingCopyResponse


def generate_marketing_copy(
    product_name,
    description,
    platform,
    tone,
    temperature=0.7,
    top_p=0.9
):
    """Generate validated marketing content using Gemini."""

    # Validate user input
    request = MarketingCopyRequest(
        product_name=product_name,
        description=description,
        platform=platform,
        tone=tone,
        temperature=temperature,
        top_p=top_p
    )

    # Build the existing dynamic prompt
    prompt = build_prompt(
        product_name=request.product_name,
        description=request.description,
        platform=request.platform,
        tone=request.tone
    )

    # Request structured marketing content
    prompt += """

Return marketing content with these fields:
- product_name
- platform
- tone
- headline
- body
- call_to_action

Write engaging, platform-appropriate content.
Avoid unsupported product claims.
"""

    generation_config = types.GenerateContentConfig(
        temperature=request.temperature,
        top_p=request.top_p,
        max_output_tokens=1024,
        response_mime_type="application/json",
        response_schema=MarketingCopyResponse
    )

    # Generate content using Gemini
    response = client.models.generate_content(
        model=MODEL_NAME,
        contents=prompt,
        config=generation_config
    )

    if not response.text:
        raise ValueError("Gemini returned an empty response.")

    # Validate the generated JSON
    try:
        validated = MarketingCopyResponse.model_validate_json(
            response.text
        )
    except ValidationError as error:
        raise ValueError(
            f"Generated content failed validation: {error}"
        ) from error

    # Return formatted text for the existing Streamlit UI
    return (
        f"{validated.headline}\n\n"
        f"{validated.body}\n\n"
        f"{validated.call_to_action}"
    )
