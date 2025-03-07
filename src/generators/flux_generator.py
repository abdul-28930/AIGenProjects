from diffusers import DiffusionPipeline
from PIL import Image
from typing import Optional
import torch
import gc

class FluxGenerator:
    def __init__(self):
        self.model = "black-forest-labs/FLUX.1-dev"
        self.pipe = None

    def _load_model(self):
        """Lazy loading of the model to save memory when not in use"""
        if self.pipe is None:
            try:
                self.pipe = DiffusionPipeline.from_pretrained(self.model)
                if torch.cuda.is_available():
                    self.pipe = self.pipe.to("cuda")
            except Exception as e:
                raise Exception(f"Failed to load FLUX model: {str(e)}")

    def _cleanup(self):
        """Clean up GPU memory after generation"""
        if self.pipe is not None and torch.cuda.is_available():
            self.pipe.to("cpu")
            torch.cuda.empty_cache()
            gc.collect()

    def generate_image(
        self,
        prompt: str,
        negative_prompt: Optional[str] = None,
        num_inference_steps: int = 50,
        guidance_scale: float = 7.5,
    ) -> Optional[Image.Image]:
        """
        Generate an image using the FLUX.1 model.

        Args:
            prompt (str): The text prompt to generate the image from
            negative_prompt (str, optional): Things to avoid in the image
            num_inference_steps (int): Number of denoising steps (default: 50)
            guidance_scale (float): How closely to follow the prompt (default: 7.5)

        Returns:
            Optional[PIL.Image.Image]: Generated image or None if generation fails

        Raises:
            Exception: If there's an error during image generation
        """
        try:
            self._load_model()
            
            # Generate the image
            result = self.pipe(
                prompt=prompt,
                negative_prompt=negative_prompt,
                num_inference_steps=num_inference_steps,
                guidance_scale=guidance_scale,
            )
            
            image = result.images[0]
            self._cleanup()  # Clean up GPU memory
            return image
            
        except Exception as e:
            self._cleanup()  # Clean up GPU memory even on error
            raise Exception(f"Failed to generate image: {str(e)}")

# Example usage
if __name__ == "__main__":
    generator = FluxGenerator()
    prompt = "Astronaut in a jungle, cold color palette, muted colors, detailed, 8k"
    try:
        image = generator.generate_image(prompt)
        if image:
            image.save("flux_generated_image.png")
    except Exception as e:
        print(f"Error: {str(e)}")
