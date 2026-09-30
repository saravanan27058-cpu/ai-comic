from pathlib import Path

from fastapi import APIRouter, Form, Request, HTTPException
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates

from .models import PromptRequest
from .gemini_flash import generate_outline
from .gemini_pro import generate_story
from .image_generator import generate_image
from .layout_builder import build_comic_layout
from .exporters import save_pdf

BASE_DIR = Path(__file__).resolve().parent.parent
templates = Jinja2Templates(directory=str(BASE_DIR / "templates"))

router = APIRouter()


@router.get("/", response_class=HTMLResponse)
async def home(request: Request):
    return templates.TemplateResponse(
        "index.html",
        {"request": request},
    )


def generate_comic(request_data: PromptRequest):
    outline = generate_outline(request_data)
    title, stories = generate_story(request_data, outline)

    image_paths = [
        generate_image(panel.image_prompt, panel.panel_number)
        for panel in stories
    ]

    layout = build_comic_layout(stories, image_paths)
    pdf_url = save_pdf(title, layout)

    return {
        "title": title,
        "panels": layout,
        "pdf_url": pdf_url,
    }


@router.post("/generate", response_class=HTMLResponse)
async def generate(
    request: Request,
    story_prompt: str = Form(...),
    character_name: str = Form(...),
    setting: str = Form(...),
    tone: str = Form(...),
    art_style: str = Form(...),
):
    try:
        data = PromptRequest(
            story_prompt=story_prompt,
            character_name=character_name,
            setting=setting,
            tone=tone,
            art_style=art_style,
        )
        result = generate_comic(data)

        return templates.TemplateResponse(
            "comic_preview.html",
            {"request": request, **result},
        )
    except Exception as exc:
        return templates.TemplateResponse(
            "index.html",
            {
                "request": request,
                "error": str(exc),
            },
            status_code=500,
        )


@router.post("/generate-comic/json")
async def generate_comic_json(data: PromptRequest):
    try:
        return generate_comic(data)
    except Exception as exc:
        raise HTTPException(status_code=500, detail=str(exc))


@router.get("/export-success", response_class=HTMLResponse)
async def export_success(request: Request, pdf_url: str = ""):
    return templates.TemplateResponse(
        "export_success.html",
        {"request": request, "pdf_url": pdf_url},
    )


@router.get("/test-image", response_class=HTMLResponse)
async def test_image(request: Request, prompt: str = "a brave fox in an enchanted forest, comic book art"):
    try:
        image_url = generate_image(prompt, 0)
        return templates.TemplateResponse(
            "test_image.html",
            {"request": request, "image_url": image_url, "prompt": prompt},
        )
    except Exception as exc:
        raise HTTPException(status_code=500, detail=str(exc))
