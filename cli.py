
# cli.py
# Command-line interface for CopyCraft AI

import argparse
import time

from generator import generate_marketing_copy
from prompts import SUPPORTED_PLATFORMS, SUPPORTED_TONES


def main():
    parser = argparse.ArgumentParser(
        description="CopyCraft AI - Marketing Copy Generator"
    )

    parser.add_argument(
        "--product",
        required=True,
        help="Name of the product"
    )

    parser.add_argument(
        "--description",
        required=True,
        help="Product description"
    )

    parser.add_argument(
        "--platform",
        required=True,
        choices=SUPPORTED_PLATFORMS,
        help="Target marketing platform"
    )

    parser.add_argument(
        "--tone",
        required=True,
        choices=SUPPORTED_TONES,
        help="Writing tone"
    )

    parser.add_argument(
        "--temperature",
        type=float,
        default=0.7,
        help="Creativity level between 0 and 1"
    )

    parser.add_argument(
        "--top-p",
        type=float,
        default=0.9,
        help="Sampling diversity between 0 and 1"
    )

    args = parser.parse_args()

    if not 0 <= args.temperature <= 1:
        parser.error("--temperature must be between 0 and 1")

    if not 0 <= args.top_p <= 1:
        parser.error("--top-p must be between 0 and 1")

    print("\nCopyCraft AI")
    print("-" * 45)
    print(f"Product: {args.product}")
    print(f"Platform: {args.platform}")
    print(f"Tone: {args.tone}")
    print("Generating content...\n")

    try:
        start_time = time.perf_counter()

        result = generate_marketing_copy(
            product_name=args.product,
            description=args.description,
            platform=args.platform,
            tone=args.tone,
            temperature=args.temperature,
            top_p=args.top_p
        )

        elapsed = time.perf_counter() - start_time

        print("GENERATED MARKETING COPY")
        print("-" * 45)
        print(result)
        print("-" * 45)
        print(f"Generation time: {elapsed:.2f} seconds")

    except Exception as error:
        parser.exit(
            status=1,
            message=f"Generation failed: {error}\n"
        )


if __name__ == "__main__":
    main()
