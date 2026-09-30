from pathlib import Path
import re
import uuid

from .config import (
    IMAGE_MODE,
    IMAGE_MODEL,
    IMAGE_STEPS,
    IMAGE_WIDTH,
    IMAGE_HEIGHT,
    HF_TOKEN,
)

BASE_DIR = Path(__file__).resolve().parent.parent
PANEL_DIR = BASE_DIR / "static" / "panels"
PANEL_DIR.mkdir(parents=True, exist_ok=True)

_pipe = None


def _safe_name(value: str) -> str:
    value = re.sub(r"[^a-zA-Z0-9_-]+", "_", value).strip("_")
    return value[:60] or "panel"


def _load_pipeline():
    global _pipe
    if _pipe is not None:
        return _pipe

    import torch
    from diffusers import StableDiffusionPipeline

    kwargs = {"use_safetensors": True}
    if HF_TOKEN:
        kwargs["token"] = HF_TOKEN

    _pipe = StableDiffusionPipeline.from_pretrained(IMAGE_MODEL, **kwargs)

    if torch.cuda.is_available():
        _pipe = _pipe.to("cuda")
    else:
        _pipe = _pipe.to("cpu")

    return _pipe


def _placeholder_image(prompt: str, output_path: Path):
    from PIL import Image, ImageDraw, ImageFont

    image = Image.new("RGB", (IMAGE_WIDTH, IMAGE_HEIGHT), "white")
    draw = ImageDraw.Draw(image)

    title = "ComicCraft"
    draw.text((24, 24), title, fill="black")
    text = prompt[:500]
    lines = [text[i:i + 45] for i in range(0, len(text), 45)]
    y = 80
    for line in lines[:10]:
        draw.text((24, y), line, fill="black")
        y += 28

    image.save(output_path)


def generate_image(prompt: str, panel_number: int) -> str:
    filename = f"panel_{panel_number}_{uuid.uuid4().hex[:8]}_{_safe_name(prompt)}.png"
    output_path = PANEL_DIR / filename

    if IMAGE_MODE == "placeholder":
        _placeholder_image(prompt, output_path)
        return f"/static/panels/{filename}"

    pipe = _load_pipeline()

    image = pipe(
        prompt=prompt,
        negative_prompt=(
            "blurry, low quality, distorted face, extra fingers, "
            "extra limbs, text, letters, words, watermark, logo"
        ),
        num_inference_steps=IMAGE_STEPS,
        width=IMAGE_WIDTH,
        height=IMAGE_HEIGHT,
    ).images[0]

    image.save(output_path)
    return f"/static/panels/{filename}"
