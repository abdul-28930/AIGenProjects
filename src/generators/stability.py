import requests
from typing import Optional
import time
import base64
import os

class StabilityGenerator:
    def __init__(self, api_key: str):
        self.api_key = api_key
        self.base_url = "https://api.stability.ai/v1"
        self.headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json",
            "Accept": "application/json"
        }

    def generate_video(
        self, 
        prompt: str,
        cfg_scale: float = 7.0,
        seed: int = None,
        motion_bucket_id: int = 127,
        frames: int = 14
    ) -> Optional[str]:
        try:
            # First check available engines
            engines_url = f"{self.base_url}/engines/list"
            engines_response = requests.get(engines_url, headers=self.headers)
            engines_response.raise_for_status()
            
            # Find the video generation engine
            video_engine = None
            for engine in engines_response.json():
                if "video" in engine["id"].lower():
                    video_engine = engine["id"]
                    break

            if not video_engine:
                raise Exception("No video generation engine found")

            # Generate video
            url = f"{self.base_url}/generation/{video_engine}/text-to-video"
            
            payload = {
                "text_prompts": [
                    {
                        "text": prompt,
                        "weight": 1
                    }
                ],
                "seed": seed if seed is not None else 0,
                "cfg_scale": cfg_scale,
                "motion_bucket_id": motion_bucket_id,
                "number_of_frames": frames
            }

            response = requests.post(url, headers=self.headers, json=payload)
            response.raise_for_status()

            # Save the video temporarily and return the path
            video_data = base64.b64decode(response.json()["artifacts"][0]["base64"])
            temp_path = f"temp_video_{int(time.time())}.mp4"
            
            with open(temp_path, "wb") as f:
                f.write(video_data)
            
            return temp_path

        except Exception as e:
            print(f"Error generating video with Stability AI: {str(e)}")
            return None

    def cleanup_temp_files(self, file_path: str):
        try:
            if os.path.exists(file_path):
                os.remove(file_path)
        except Exception as e:
            print(f"Error cleaning up temporary file: {str(e)}") 