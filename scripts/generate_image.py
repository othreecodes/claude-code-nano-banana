#!/usr/bin/env -S uv run --script
# /// script
# requires-python = ">=3.10"
# dependencies = [
#     "google-genai>=1.0.0",
# ]
# ///
"""
Nano Banana Image Generation Script
Uses Google's Gemini API for image generation and editing.

Run with: uv run generate_image.py "your prompt" -o output.png
"""

import argparse
import base64
import os
import sys
from pathlib import Path

from google import genai
from google.genai import types


def get_client():
    """Initialize Gemini client with API key."""
    api_key = os.environ.get("GEMINI_API_KEY")
    if not api_key:
        print("Error: GEMINI_API_KEY environment variable not set.")
        print("Get your API key from: https://aistudio.google.com/apikey")
        sys.exit(1)
    return genai.Client(api_key=api_key)


def generate_image(
    prompt: str,
    model: str = "gemini-2.5-flash-image",
    output_path: str = "generated_image.png",
    input_image: str = None,
) -> str:
    """
    Generate or edit an image using Nano Banana.
    
    Args:
        prompt: Text description of desired image or edit
        model: Model to use (gemini-2.5-flash-image or gemini-3-pro-image-preview)
        output_path: Where to save the generated image
        input_image: Optional path to image for editing
    
    Returns:
        Path to saved image
    """
    client = get_client()
    
    contents = [prompt]
    
    # If input image provided, include it for editing
    if input_image:
        image_path = Path(input_image)
        if not image_path.exists():
            print(f"Error: Input image not found: {input_image}")
            sys.exit(1)
        
        with open(image_path, "rb") as f:
            image_data = base64.b64encode(f.read()).decode("utf-8")
        
        mime_type = "image/png" if image_path.suffix.lower() == ".png" else "image/jpeg"
        contents.append(types.Part.from_bytes(
            data=base64.b64decode(image_data),
            mime_type=mime_type
        ))
    
    # Generate image
    response = client.models.generate_content(
        model=model,
        contents=contents,
        config=types.GenerateContentConfig(
            response_modalities=["TEXT", "IMAGE"]
        )
    )
    
    # Process response
    text_response = None
    image_saved = False
    
    for part in response.candidates[0].content.parts:
        if hasattr(part, "text") and part.text:
            text_response = part.text
            print(f"Model response: {text_response}")
        elif hasattr(part, "inline_data") and part.inline_data:
            # Save the image
            image_bytes = part.inline_data.data
            output = Path(output_path)
            output.write_bytes(image_bytes)
            print(f"Image saved to: {output.absolute()}")
            image_saved = True
    
    if not image_saved:
        print("Warning: No image was generated in the response.")
        if text_response:
            print(f"Model said: {text_response}")
    
    return output_path


def main():
    parser = argparse.ArgumentParser(
        description="Generate or edit images using Google's Nano Banana (Gemini Image)"
    )
    parser.add_argument(
        "prompt",
        help="Text prompt describing the image to generate or edit"
    )
    parser.add_argument(
        "-o", "--output",
        default="generated_image.png",
        help="Output path for generated image (default: generated_image.png)"
    )
    parser.add_argument(
        "-i", "--input",
        help="Input image path for editing (optional)"
    )
    parser.add_argument(
        "-m", "--model",
        choices=["flash", "pro"],
        default="flash",
        help="Model to use: flash (Nano Banana) or pro (Nano Banana Pro)"
    )
    
    args = parser.parse_args()
    
    # Map model choice to actual model name
    model_map = {
        "flash": "gemini-2.5-flash-image",
        "pro": "gemini-3-pro-image-preview"
    }
    model = model_map[args.model]
    
    generate_image(
        prompt=args.prompt,
        model=model,
        output_path=args.output,
        input_image=args.input
    )


if __name__ == "__main__":
    main()
