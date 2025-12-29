# Nano Banana API Reference

## Models

| Model | API Name | Best For |
|-------|----------|----------|
| Nano Banana | `gemini-2.5-flash-image` | Speed, high-volume tasks, quick iterations |
| Nano Banana Pro | `gemini-3-pro-image-preview` | Professional quality, complex prompts, text rendering |

## Pricing

- **Nano Banana**: $30.00 per 1M output tokens (~$0.039 per image at 1290 tokens/image)
- **Nano Banana Pro**: Check Google's pricing page for current rates

## Python SDK Usage

### Running with uv (recommended)
```bash
# One-off command with dependency
uv run --with google-genai python your_script.py

# Or use inline script dependencies (see generate_image.py)
uv run scripts/generate_image.py "your prompt"
```

### Basic Generation
```python
from google import genai
import os

client = genai.Client(api_key=os.environ["GEMINI_API_KEY"])
response = client.models.generate_content(
    model="gemini-2.5-flash-image",
    contents=["Create an image of a sunset over mountains"]
)

for part in response.candidates[0].content.parts:
    if part.inline_data:
        with open("output.png", "wb") as f:
            f.write(part.inline_data.data)
```

### Image Editing
```python
from google import genai
from google.genai import types
import base64
import os

client = genai.Client(api_key=os.environ["GEMINI_API_KEY"])

with open("input.jpg", "rb") as f:
    image_data = base64.b64encode(f.read()).decode()

response = client.models.generate_content(
    model="gemini-2.5-flash-image",
    contents=[
        "Remove the background and replace with a beach scene",
        types.Part.from_bytes(
            data=base64.b64decode(image_data),
            mime_type="image/jpeg"
        )
    ]
)
```

### Multi-turn Editing (Chat)
```python
from google import genai
from google.genai import types
import os

client = genai.Client(api_key=os.environ["GEMINI_API_KEY"])

chat = client.chats.create(
    model="gemini-3-pro-image-preview",
    config=types.GenerateContentConfig(
        response_modalities=['TEXT', 'IMAGE']
    )
)

response = chat.send_message("Create a logo for a coffee shop")
response = chat.send_message("Make the text more elegant")
```

## Capabilities

### Generation
- Text-to-image generation
- Photorealistic and artistic styles
- Infographics and diagrams
- Text rendering in images

### Editing
- Background replacement
- Object removal
- Style transfer
- Color/lighting adjustments
- Pose changes
- Day/night transformation

### Advanced (Nano Banana Pro)
- Character consistency across images
- Complex infographics with real-world data
- Studio-quality control over lighting, focus, angles

## Response Handling

```python
for part in response.candidates[0].content.parts:
    if part.text:
        print(part.text)
    elif part.inline_data:
        # part.inline_data.data = image bytes
        # part.inline_data.mime_type = "image/png"
        pass
```

## SynthID Watermarking

All generated images include invisible SynthID digital watermark for AI content detection.
