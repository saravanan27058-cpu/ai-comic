import json
import re
from google import genai
from google.genai import types

from .config import GEMINI_API_KEY, GEMINI_FLASH_MODEL, NUM_PANELS
from .models import PromptRequest, PanelOutline

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

    start = text.find("[")
    end = text.rfind("]")
    if start == -1 or end == -1:
        raise ValueError("Gemini did not return a JSON array.")
    return json.loads(text[start:end + 1])


def generate_outline(request: PromptRequest) -> list[PanelOutline]:
    prompt = f"""
Create a structured {NUM_PANELS}-panel comic outline.

User story idea: {request.story_prompt}
Main character: {request.character_name}
Setting: {request.setting}
Tone: {request.tone}
Art style: {request.art_style}

Return ONLY valid JSON as an array. No markdown and no explanation.
Each item must have exactly:
panel_number, title, scene_description, image_prompt

Requirements:
- Exactly {NUM_PANELS} panels.
- Maintain continuity of the same main character.
- Each panel must move the story forward.
- image_prompt must describe a clear visual scene and include the requested art style.
- Do not put dialogue inside image_prompt.
"""

    response = _get_client().models.generate_content(
        model=GEMINI_FLASH_MODEL,
        contents=prompt,
        config=types.GenerateContentConfig(
            temperature=0.8,
            response_mime_type="application/json",
        ),
    )

    data = _extract_json(response.text)
    if not isinstance(data, list) or len(data) != NUM_PANELS:
        raise ValueError(f"Expected {NUM_PANELS} panels from Gemini.")

    return [PanelOutline.model_validate(item) for item in data]
