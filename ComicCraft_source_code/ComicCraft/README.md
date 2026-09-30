# ComicCraft — AI Comic Story Creator

A beginner-friendly FastAPI web application that:
1. Accepts a story prompt, character, setting, tone and art style.
2. Uses Gemini to create a structured 5-panel outline.
3. Uses Gemini again to create narration and dialogue.
4. Uses Hugging Face Diffusers + Stable Diffusion to generate panel images.
5. Shows the comic in a web page.
6. Exports the comic to a PDF.

## Quick start

### 1. Create and activate a virtual environment

Windows PowerShell:

```powershell
py -m venv .venv
.\.venv\Scripts\Activate.ps1
```

Windows CMD:

```cmd
py -m venv .venv
.venv\Scripts\activate
```

### 2. Install packages

```bash
python -m pip install --upgrade pip
pip install -r requirements.txt
```

### 3. Configure Gemini

Copy `.env.example` to `.env` and add your Gemini API key:

```text
GEMINI_API_KEY=your_key_here
```

### 4. First test without Stable Diffusion

Set:

```text
IMAGE_MODE=placeholder
```

Then run:

```bash
uvicorn app.main:app --reload
```

Open:

http://127.0.0.1:8000

This tests the FastAPI + Gemini + PDF workflow without downloading the image model.

### 5. Enable real AI images

Change `.env`:

```text
IMAGE_MODE=local
```

The first image generation downloads the Stable Diffusion model. A suitable GPU is strongly recommended. CPU execution is supported but can be very slow.

## API

Interactive documentation:

http://127.0.0.1:8000/docs

JSON endpoint:

POST `/generate-comic/json`

Example:

```json
{
  "story_prompt": "A brave fox explores an enchanted forest.",
  "character_name": "Finn",
  "setting": "Enchanted forest",
  "tone": "Adventure",
  "art_style": "Comic book"
}
```

Image test:

http://127.0.0.1:8000/test-image?prompt=a%20brave%20fox%20in%20an%20enchanted%20forest
