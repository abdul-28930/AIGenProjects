import streamlit as st
from generators.flux_generator import FluxGenerator
from generators.mochi_generator import MochiGenerator
import os
from PIL import Image
import tempfile
import imageio

def save_frames_as_gif(frames, output_path):
    """Convert frames to GIF and save"""
    imageio.mimsave(output_path, frames, fps=8)

def main():
    st.title("AI Image & Video Generation")
    
    tab1, tab2 = st.tabs(["Image Generation", "Video Generation"])
    
    with tab1:
        st.header("FLUX Image Generator")
        img_prompt = st.text_area("Enter your image prompt:", 
                                "A serene landscape with mountains at sunset, detailed, 8k")
        
        img_col1, img_col2 = st.columns(2)
        with img_col1:
            neg_prompt = st.text_area("Negative prompt (optional):", 
                                    "blurry, low quality, distorted")
            steps = st.slider("Number of steps", 20, 100, 50, key="img_steps")
        
        with img_col2:
            guidance = st.slider("Guidance scale", 1.0, 20.0, 7.5, key="img_guidance")
        
        if st.button("Generate Image", key="gen_img"):
            with st.spinner("Generating your image..."):
                try:
                    generator = FluxGenerator()
                    image = generator.generate_image(
                        prompt=img_prompt,
                        negative_prompt=neg_prompt,
                        num_inference_steps=steps,
                        guidance_scale=guidance
                    )
                    
                    # Save and display image
                    output_path = "generated_image.png"
                    image.save(output_path)
                    st.image(output_path, caption="Generated Image")
                    
                    # Download button
                    with open(output_path, "rb") as file:
                        st.download_button(
                            label="Download Image",
                            data=file,
                            file_name="generated_image.png",
                            mime="image/png"
                        )
                except Exception as e:
                    st.error(f"Error generating image: {str(e)}")
    
    with tab2:
        st.header("Mochi Video Generator")
        vid_prompt = st.text_area("Enter your video prompt:",
                                "A butterfly flying through a magical forest, detailed")
        
        vid_col1, vid_col2 = st.columns(2)
        with vid_col1:
            vid_neg_prompt = st.text_area("Negative prompt (optional):", 
                                        "blurry, low quality, distorted",
                                        key="vid_neg")
            vid_steps = st.slider("Number of steps", 20, 100, 50, key="vid_steps")
        
        with vid_col2:
            vid_guidance = st.slider("Guidance scale", 1.0, 20.0, 7.5, key="vid_guidance")
            num_frames = st.slider("Number of frames", 8, 32, 16)
        
        if st.button("Generate Video", key="gen_vid"):
            with st.spinner("Generating your video... This may take a while"):
                try:
                    generator = MochiGenerator()
                    frames = generator.generate_video(
                        prompt=vid_prompt,
                        negative_prompt=vid_neg_prompt,
                        num_inference_steps=vid_steps,
                        guidance_scale=vid_guidance,
                        num_frames=num_frames
                    )
                    
                    # Save frames as GIF
                    output_path = "generated_video.gif"
                    save_frames_as_gif(frames, output_path)
                    
                    # Display video
                    st.video(output_path)
                    
                    # Download button
                    with open(output_path, "rb") as file:
                        st.download_button(
                            label="Download Video",
                            data=file,
                            file_name="generated_video.gif",
                            mime="image/gif"
                        )
                except Exception as e:
                    st.error(f"Error generating video: {str(e)}")

if __name__ == "__main__":
    main()
