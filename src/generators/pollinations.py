import requests
from typing import Optional
import time

class PollinationsGenerator:
    def __init__(self):
        self.base_url = "https://image.pollinations.ai/prompt"

    def generate_image(self, prompt: str, model: str = "stable-diffusion-xl") -> Optional[str]:
        try:
            # Pollinations.ai now uses a simpler direct URL approach
            # Encode the prompt and model into the URL
            encoded_prompt = requests.utils.quote(f"{prompt}?model={model}")
            image_url = f"{self.base_url}/{encoded_prompt}"
            
            # Test if the URL is accessible
            response = requests.head(image_url)
            response.raise_for_status()
            
            return image_url

        except Exception as e:
            print(f"Error generating image with Pollinations: {str(e)}")
            return None 