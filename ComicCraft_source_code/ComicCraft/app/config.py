import os
from dotenv import load_dotenv

load_dotenv()

GEMINI_API_KEY = os.getenv("GEMINI_API_KEY", "").strip()
GEMINI_FLASH_MODEL = os.getenv("GEMINI_FLASH_MODEL", "gemini-2.5-flash").strip()
GEMINI_PRO_MODEL = os.getenv("GEMINI_PRO_MODEL", "gemini-2.5-pro").strip()

IMAGE_MODE = os.getenv("IMAGE_MODE", "local").strip().lower()
IMAGE_MODEL = os.getenv(
    "IMAGE_MODEL",
    "stable-diffusion-v1-5/stable-diffusion-v1-5",
).strip()

NUM_PANELS = int(os.getenv("NUM_PANELS", "5"))
IMAGE_STEPS = int(os.getenv("IMAGE_STEPS", "20"))
IMAGE_WIDTH = int(os.getenv("IMAGE_WIDTH", "512"))
IMAGE_HEIGHT = int(os.getenv("IMAGE_HEIGHT", "512"))

HF_TOKEN = os.getenv("HF_TOKEN", "").strip()
