import requests
from typing import Optional
import time

class ProdiaGenerator:
    def __init__(self, api_key: str):
        self.api_key = api_key
        self.base_url = "https://api.prodia.com/v1"
        self.headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json"
        }

    def generate_image(self, prompt: str, model: str = "sdxl", steps: int = 30) -> Optional[str]:
        try:
            # Create generation request
            generate_url = f"{self.base_url}/generate"
            payload = {
                "prompt": prompt,
                "model": model,
                "steps": steps,
                "cfg_scale": 7,
                "negative_prompt": "blurry, bad quality, distorted",
                "aspect_ratio": "square"
            }
            
            response = requests.post(generate_url, headers=self.headers, json=payload)
            response.raise_for_status()
            job = response.json()
            
            # Poll for completion
            while True:
                status_url = f"{self.base_url}/generation/{job['id']}"
                status_response = requests.get(status_url, headers=self.headers)
                status_response.raise_for_status()
                
                status_data = status_response.json()
                if status_data["status"] == "succeeded":
                    return status_data["image"]["url"]
                elif status_data["status"] == "failed":
                    raise Exception("Image generation failed")
                    
                time.sleep(1)

        except Exception as e:
            print(f"Error generating image with Prodia: {str(e)}")
            return None 