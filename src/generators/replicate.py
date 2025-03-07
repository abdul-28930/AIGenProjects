import replicate
from typing import Optional
import time
import os

class ReplicateGenerator:
    def __init__(self, api_key: str):
        self.api_key = api_key
        os.environ["REPLICATE_API_TOKEN"] = api_key

    def generate_video(
        self, 
        prompt: str, 
        model: str = "zeroscope",
        num_frames: int = 24,
        fps: int = 8
    ) -> Optional[str]:
        try:
            model_versions = {
                "zeroscope": "zeroscope/zeroscope-v2-xl:9f747673945c62801b13b84701c783929c0ee784e4748ec062204894dda1a351",
                "animov": "animo/animov-512x:b44a4c3f8afd93f7fe35e35b901fe3e73886ad99e1233c9a693b83cec273d615",
                "stable-video": "stability-ai/stable-video-diffusion:3f0457e4619daac51203dedb472816fd4af51f3149fa7a9e0b5ffcf1b8172438"
            }

            # Set parameters based on model
            if model == "zeroscope":
                output = replicate.run(
                    model_versions[model],
                    input={
                        "prompt": prompt,
                        "num_frames": num_frames,
                        "fps": fps
                    }
                )
            elif model == "animov":
                output = replicate.run(
                    model_versions[model],
                    input={
                        "prompt": prompt,
                        "num_frames": num_frames
                    }
                )
            else:  # stable-video
                output = replicate.run(
                    model_versions[model],
                    input={
                        "prompt": prompt,
                        "video_length": "14_frames_with_svd"
                    }
                )

            # Replicate returns a list with the video URL as the first item
            if isinstance(output, list) and len(output) > 0:
                return output[0]
            return None

        except Exception as e:
            print(f"Error generating video with Replicate: {str(e)}")
            return None 