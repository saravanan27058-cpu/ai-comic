import json
import re
from google import genai
from google.genai import types

from .config import GEMINI_API_KEY, GEMINI_PRO_MODEL
from .models import PromptRequest, PanelOutline, PanelStory

_client = None


def _get_client():
    global _client
    if _client is None:
        if not GEMINI_API_KEY:
            raise RuntimeError(
                "GEMINI_API_KEY is missing. Add it to your .env file."
            )
        _client = genai.Client(api_key=GEMINI_API_KEY)
    return _client


def _extract_json(text: str):
    text = text.strip()
    text = re.sub(r"^```json\s*", "", text, flags=re.I)
    text = re.sub(r"^```\s*", "", text)
    text = re.sub(r"\s*```$", "", text)
    start = text.find("{")
    end = text.rfind("}")
    if start == -1 or end == -1:
        raise ValueError("Gemini did not return a JSON object.")
    return json.loads(text[start:end + 1])


def generate_story(
    request: PromptRequest,
    outline: list[PanelOutline],
) -> tuple[str, list[PanelStory]]:
    outline_json = [item.model_dump() for item in outline]

    prompt = f"""
Turn this comic outline into a polished short comic story.

Original story idea: {request.story_prompt}
Main character: {request.character_name}
Setting: {request.setting}
Tone: {request.tone}
Art style: {request.art_style}

Outline:
{json.dumps(outline_json, ensure_ascii=False, indent=2)}

Return ONLY valid JSON in this exact shape:
{{
  "title": "Comic title",
  "panels": [
    {{
      "panel_number": 1,
      "title": "Panel title",
      "scene_description": "Short visual scene description",
      "image_prompt": "Detailed visual prompt",
      "caption": "Short caption",
      "narration": "Narration for this panel",
      "dialogue": "Optional character dialogue"
    }}
  ]
}}

Rules:
- Keep exactly the same number of panels as the outline.
- Preserve the outline's events and continuity.
- Make narration concise enough for a comic page.
- Keep dialogue natural and short.
- image_prompt should be suitable for Stable Diffusion.
- Do not add text, speech bubbles, captions, logos, watermarks, or typography to the generated image.
"""

    response = _get_client().models.generate_content(
        model=GEMINI_PRO_MODEL,
        contents=prompt,
        config=types.GenerateContentConfig(
            temperature=0.9,
            response_mime_type="application/json",
        ),
    )

    data = _extract_json(response.text)
    title = str(data.get("title", "ComicCraft Story"))
    panels = [PanelStory.model_validate(item) for item in data.get("panels", [])]

    if len(panels) != len(outline):
        raise ValueError("Gemini returned an incorrect number of story panels.")

    return title, panels
