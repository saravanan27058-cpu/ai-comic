from pathlib import Path
from datetime import datetime
from fpdf import FPDF
from PIL import Image

BASE_DIR = Path(__file__).resolve().parent.parent
EXPORT_DIR = BASE_DIR / "static" / "exports"
EXPORT_DIR.mkdir(parents=True, exist_ok=True)


def _local_image(image_url: str) -> Path:
    relative = image_url.replace("/static/", "")
    return BASE_DIR / "static" / relative


def save_pdf(title: str, layout: list[dict]) -> str:
    filename = f"comic_{datetime.now().strftime('%Y%m%d_%H%M%S')}.pdf"
    output = EXPORT_DIR / filename

    pdf = FPDF()
    pdf.set_auto_page_break(auto=True, margin=15)

    for panel in layout:
        pdf.add_page()

        pdf.set_font("Helvetica", "B", 18)
        pdf.multi_cell(0, 10, f"Panel {panel['panel_number']}: {panel['title']}")
        pdf.ln(3)

        image_path = _local_image(panel["image_path"])
        if image_path.exists():
            with Image.open(image_path) as img:
                width, height = img.size
            max_width = 175
            max_height = 105
            scale = min(max_width / width, max_height / height)
            pdf.image(
                str(image_path),
                x=17,
                y=pdf.get_y(),
                w=width * scale,
                h=height * scale,
            )
            pdf.ln(height * scale + 5)

        pdf.set_font("Helvetica", "I", 11)
        pdf.multi_cell(0, 7, panel["scene_description"])
        pdf.ln(2)

        pdf.set_font("Helvetica", "B", 11)
        pdf.multi_cell(0, 7, panel["caption"])
        pdf.ln(2)

        pdf.set_font("Helvetica", "", 11)
        pdf.multi_cell(0, 7, panel["narration"])

        if panel.get("dialogue"):
            pdf.ln(2)
            pdf.set_font("Helvetica", "B", 11)
            pdf.multi_cell(0, 7, f"Dialogue: {panel['dialogue']}")

    pdf.output(str(output))
    return f"/static/exports/{filename}"
