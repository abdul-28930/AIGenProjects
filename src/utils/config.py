from typing import Dict, Any
import os
from dotenv import load_dotenv

load_dotenv()

class Config:
    PRODIA_API_KEY: str = os.getenv("PRODIA_API_KEY", "")
    STABILITY_API_KEY: str = os.getenv("STABILITY_API_KEY", "")
    OPENAI_API_KEY: str = os.getenv("OPENAI_API_KEY", "")
    
    PRODIA_MODELS: Dict[str, str] = {
        "SDXL": "sdxl",
        "Stable Diffusion XL": "stable-diffusion-xl",
        "Deliberate V2": "deliberate-v2",
        "DreamShaper 8": "dreamshaper-8",
        "Realistic Vision V5.1": "realistic-vision-v5.1"
    }
    
    POLLINATIONS_MODELS: Dict[str, str] = {
        "Stable Diffusion XL": "stable-diffusion-xl",
        "Kandinsky": "kandinsky",
        "OpenJourney": "openjourney",
        "Stable Diffusion 2.1": "stable-diffusion-2.1"
    }

    VIDEO_MODELS: Dict[str, str] = {
        "ZeroScope": "zeroscope",
        "AnimoV": "animov",
        "Stable Video Diffusion": "stable-video"
    }

    VIDEO_SETTINGS = {
        "cfg_scale_options": [1.0, 3.0, 5.0, 7.0, 9.0],
        "motion_bucket_options": [127, 150, 175, 200],
        "frame_options": [14, 25, 50]
    }

    PDF_SETTINGS = {
        "temp_directory": "temp_pdfs",
        "default_filename": "generated_document.pdf"
    } 