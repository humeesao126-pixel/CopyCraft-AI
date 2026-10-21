
# batch.py
# Asynchronous batch generation for CopyCraft AI

import asyncio
import pandas as pd

from google.genai import types
from pydantic import ValidationError

from config import client, MODEL_NAME
from prompts import (
    build_prompt,
    SUPPORTED_PLATFORMS,
    SUPPORTED_TONES
)
from models import (
    MarketingCopyRequest,
    MarketingCopyResponse
)


REQUIRED_COLUMNS = [
    "product_name",
    "description",
    "platform",
    "tone"
]

MAX_CONCURRENT_REQUESTS = 2
REQUEST_TIMEOUT = 90


def validate_batch_data(df):
    """Validate uploaded CSV structure."""

    missing = [
        col for col in REQUIRED_COLUMNS
        if col not in df.columns
    ]

    if missing:
        raise ValueError(
            "Missing required columns: " + ", ".join(missing)
        )

    if df.empty:
        raise ValueError("The CSV file is empty.")

    if len(df) > 20:
        raise ValueError("Maximum 20 products per batch.")

    return True


async def generate_single_async(
    row,
    semaphore,
    temperature,
    top_p
):
    """Generate validated content for one product."""

    product_name = str(row["product_name"]).strip()

    result = {
        "product_name": product_name,
        "platform": str(row["platform"]),
        "tone": str(row["tone"]),
        "generated_copy": "",
        "status": "Failed",
        "error": ""
    }

    try:
        # Validate missing CSV values
        for col in REQUIRED_COLUMNS:
            if pd.isna(row[col]) or not str(row[col]).strip():
                raise ValueError(f"Missing value: {col}")

        request = MarketingCopyRequest(
            product_name=product_name,
            description=str(row["description"]).strip(),
            platform=str(row["platform"]).strip(),
            tone=str(row["tone"]).strip(),
            temperature=temperature,
            top_p=top_p
        )

        if request.platform not in SUPPORTED_PLATFORMS:
            raise ValueError("Unsupported platform")

        if request.tone not in SUPPORTED_TONES:
            raise ValueError("Unsupported tone")

        prompt = build_prompt(
            request.product_name,
            request.description,
            request.platform,
            request.tone
        )

        prompt += """

Return a JSON object containing:
product_name, platform, tone, headline,
body, and call_to_action.

Write professional, platform-appropriate content.
Avoid unsupported product claims.
"""

        config = types.GenerateContentConfig(
            temperature=request.temperature,
            top_p=request.top_p,
            max_output_tokens=1024,
            response_mime_type="application/json",
            response_schema=MarketingCopyResponse
        )

        # Limit simultaneous API requests
        async with semaphore:

            # Limit waiting time per request
            async with asyncio.timeout(REQUEST_TIMEOUT):

                response = await client.aio.models.generate_content(
                    model=MODEL_NAME,
                    contents=prompt,
                    config=config
                )

        if not response.text:
            raise ValueError("Gemini returned an empty response.")

        validated = MarketingCopyResponse.model_validate_json(
            response.text
        )

        result["generated_copy"] = (
            f"{validated.headline}\n\n"
            f"{validated.body}\n\n"
            f"{validated.call_to_action}"
        )

        result["status"] = "Success"

    except TimeoutError:
        result["error"] = "Request timed out after 90 seconds."

    except ValidationError as error:
        result["error"] = f"Validation error: {error}"

    except Exception as error:
        result["error"] = str(error)

    return result


async def process_batch_async(
    df,
    temperature=0.7,
    top_p=0.9,
    progress_callback=None
):
    """Process products concurrently and preserve CSV order."""

    validate_batch_data(df)

    semaphore = asyncio.Semaphore(
        MAX_CONCURRENT_REQUESTS
    )

    rows = [
        row for _, row in df.iterrows()
    ]

    async def process_indexed(index, row):
        result = await generate_single_async(
            row,
            semaphore,
            temperature,
            top_p
        )
        return index, result

    tasks = [
        asyncio.create_task(process_indexed(i, row))
        for i, row in enumerate(rows)
    ]

    results = [None] * len(tasks)
    completed = 0

    for task in asyncio.as_completed(tasks):
        index, result = await task
        results[index] = result

        completed += 1

        if progress_callback is not None:
            progress_callback(completed, len(tasks))

    return pd.DataFrame(results)


def process_batch(
    df,
    temperature=0.7,
    top_p=0.9,
    progress_callback=None
):
    """Synchronous wrapper for the Streamlit application."""

    return asyncio.run(
        process_batch_async(
            df=df,
            temperature=temperature,
            top_p=top_p,
            progress_callback=progress_callback
        )
    )
