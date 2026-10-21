
# prompts.py
# Dynamic prompt template for CopyCraft AI

SUPPORTED_PLATFORMS = ["LinkedIn", "Instagram", "Email"]

SUPPORTED_TONES = [
    "Professional",
    "Friendly",
    "Exciting",
    "Persuasive",
    "Casual",
    "Luxury"
]


def build_prompt(product_name, description, platform, tone):
    """Create a customized marketing prompt."""

    platform_guidelines = {
        "LinkedIn": (
            "Write professional, informative content suitable "
            "for business professionals. Include a clear call to action."
        ),
        "Instagram": (
            "Write engaging, attention-grabbing content. "
            "Use suitable emojis and relevant hashtags."
        ),
        "Email": (
            "Write compelling marketing email copy with "
            "a subject line, body, and call to action."
        )
    }

    if platform not in SUPPORTED_PLATFORMS:
        raise ValueError(f"Unsupported platform: {platform}")

    if tone not in SUPPORTED_TONES:
        raise ValueError(f"Unsupported tone: {tone}")

    prompt = f"""
You are an expert marketing copywriter.

Create high-quality marketing content using the following details:

Product Name: {product_name}

Product Description:
{description}

Target Platform: {platform}

Desired Tone: {tone}

Platform Guidelines:
{platform_guidelines[platform]}

Additional Instructions:
1. Maintain the selected tone throughout the content.
2. Highlight the product's main benefits.
3. Make the content engaging and easy to understand.
4. Include a clear call to action.
5. Avoid making unsupported product claims.
6. Return only the final marketing copy.

Generate the marketing content now.
"""

    return prompt.strip()
