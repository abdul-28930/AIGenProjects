from typing import Dict, Any
import os
from dotenv import load_dotenv

load_dotenv()

class Config:
    PRODIA_API_KEY: str = os.getenv("PRODIA_API_KEY", "")
    
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