from diffusers import DiffusionPipeline
from PIL import Image
from typing import Optional, List
import torch
import imageio
import gc

class MochiGenerator:
    def __init__(self):
        self.model = "genmo/mochi-1-preview"
        self.pipe = None

    def _load_model(self):
        """Lazy loading of the model to save memory when not in use"""
        if self.pipe is None:
            try:
                self.pipe = DiffusionPipeline.from_pretrained(self.model)
                if torch.cuda.is_available():
                    self.pipe = self.pipe.to("cuda")
            except Exception as e:
                raise Exception(f"Failed to load Mochi model: {str(e)}")

    def _cleanup(self):
        """Clean up GPU memory after generation"""
        if self.pipe is not None and torch.cuda.is_available():
            self.pipe.to("cpu")
            torch.cuda.empty_cache()
            gc.collect()

    def generate_video(
        self,
        prompt: str,
        negative_prompt: Optional[str] = None,
        num_inference_steps: int = 50,
        guidance_scale: float = 7.5,
        num_frames: int = 16,
    ) -> List[Image.Image]:
        """
        Generate a video using the Mochi model.

        Args:
            prompt (str): The text prompt to generate the video from
            negative_prompt (str, optional): Things to avoid in the video
            num_inference_steps (int): Number of denoising steps (default: 50)
            guidance_scale (float): How closely to follow the prompt (default: 7.5)
            num_frames (int): Number of frames to generate (default: 16)

        Returns:
            List[Image.Image]: List of PIL Images representing video frames

        Raises:
            Exception: If there's an error during video generation
        """
        try:
            self._load_model()
            
            # Generate the video frames
            result = self.pipe(
                prompt=prompt,
                negative_prompt=negative_prompt,
                num_inference_steps=num_inference_steps,
                guidance_scale=guidance_scale,
                num_frames=num_frames,
            )
            
            frames = result.frames[0]
            self._cleanup()  # Clean up GPU memory
            return frames
            
        except Exception as e:
            self._cleanup()  # Clean up GPU memory even on error
            raise Exception(f"Failed to generate video: {str(e)}")

    def save_as_gif(self, frames: List[Image.Image], output_path: str, fps: int = 8) -> bool:
        """
        Save video frames as a GIF file.

        Args:
            frames (List[Image.Image]): List of PIL Image frames
            output_path (str): Path to save the GIF file
            fps (int): Frames per second for the GIF

        Returns:
            bool: True if successful, False otherwise
        """
        try:
            imageio.mimsave(output_path, frames, fps=fps)
            return True
        except Exception as e:
            raise Exception(f"Failed to save GIF: {str(e)}")

# Example usage
if __name__ == "__main__":
    generator = MochiGenerator()
    prompt = "Astronaut in a jungle, cold color palette, muted colors, detailed, 8k"
    frames = generator.generate_video(prompt)
    generator.save_as_gif(frames, "mochi_generated.gif")
    # Save first frame as preview
    frames[0].save("mochi_preview.png")
