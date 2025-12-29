# Nano Banana Image Generation Skill

A [Claude Code](https://docs.anthropic.com/en/docs/claude-code) skill for generating and editing images using Google's **Nano Banana** (Gemini Image API).

## Features

- **Text-to-image generation** — Create images from text prompts
- **Image editing** — Modify existing images with natural language
- **Two models** — Fast (Nano Banana) or Pro quality (Nano Banana Pro)
- **Zero dependencies to manage** — Uses `uv` inline script dependencies

## Installation

### Prerequisites

1. **uv** — Install from [astral.sh/uv](https://astral.sh/uv)
   ```bash
   curl -LsSf https://astral.sh/uv/install.sh | sh
   ```

2. **Gemini API Key** — Get one free from [aistudio.google.com/apikey](https://aistudio.google.com/apikey)
   ```bash
   export GEMINI_API_KEY="your-api-key"
   ```

### Add to Claude Code

**Option A: Clone directly into skills folder**
```bash
git clone https://github.com/othreecodes/nano-banana-imagegen.git ~/.claude/skills/nano-banana-imagegen
```

**Option B: Project-level installation**
```bash
cd your-project
git clone https://github.com/othreecodes/nano-banana-imagegen.git .claude/skills/nano-banana-imagegen
```

## Usage

### In Claude Code

Just ask Claude to generate images:

```
> create an image of a flying cat with angel wings
> edit this photo to make it look like sunset
> generate an infographic about climate change using pro model
```

### CLI Usage

```bash
# Generate an image
uv run scripts/generate_image.py "A futuristic city at sunset" -o city.png

# Edit an existing image
uv run scripts/generate_image.py "Remove the background" -i photo.jpg -o edited.png

# Use Nano Banana Pro for higher quality
uv run scripts/generate_image.py "Create a detailed infographic" -m pro -o infographic.png
```

## Models

| Model | Flag | Best For |
|-------|------|----------|
| Nano Banana | `-m flash` (default) | Fast generation, iterations, high volume |
| Nano Banana Pro | `-m pro` | Professional quality, text rendering, complex prompts |

## Pricing

- **Nano Banana**: ~$0.039 per image
- **Nano Banana Pro**: Check [Google's pricing](https://ai.google.dev/pricing)

## File Structure

```
nano-banana-imagegen/
├── SKILL.md                 # Main skill instructions
├── scripts/
│   └── generate_image.py    # CLI tool with uv inline dependencies
└── references/
    ├── api_reference.md     # Detailed API documentation
    └── prompting_guide.md   # Tips for effective prompts
```

## License

MIT

## Credits

- Built for [Claude Code](https://docs.anthropic.com/en/docs/claude-code)
- Uses [Google Gemini Image API](https://ai.google.dev/gemini-api/docs/image-generation)
