import streamlit as st
from src import (
    ProdiaGenerator,
    PollinationsGenerator,
    StabilityGenerator,
    FluxGenerator,
    MochiGenerator,
    ContentGenerator,
    PDFGenerator,
    Config
)
import time
import random
import os

st.set_page_config(
    page_title="AI Media Generator",
    page_icon="🎨",
    layout="wide"
)

def initialize_generators():
    prodia = ProdiaGenerator(Config.PRODIA_API_KEY)
    pollinations = PollinationsGenerator()
    stability = StabilityGenerator(Config.STABILITY_API_KEY)
    content_gen = ContentGenerator()
    pdf_gen = PDFGenerator()
    flux = FluxGenerator()
    mochi = MochiGenerator()
    return prodia, pollinations, stability, content_gen, pdf_gen, flux, mochi

def cleanup_temp_files():
    """Clean up temporary generated files and directories"""
    temp_files = ["temp_flux_image.png", "temp_mochi_video.gif"]
    temp_dirs = [Config.PDF_SETTINGS["temp_directory"]]
    
    for file in temp_files:
        try:
            if os.path.exists(file):
                os.remove(file)
        except Exception as e:
            st.error(f"Failed to clean up {file}: {str(e)}")
            
    for dir_path in temp_dirs:
        try:
            if os.path.exists(dir_path):
                # Only remove files older than 24 hours
                current_time = time.time()
                for filename in os.listdir(dir_path):
                    filepath = os.path.join(dir_path, filename)
                    if current_time - os.path.getmtime(filepath) > 86400:  # 24 hours
                        os.remove(filepath)
        except Exception as e:
            st.error(f"Failed to clean up directory {dir_path}: {str(e)}")

def main():
    try:
        # Register cleanup on session start
        if "cleanup_done" not in st.session_state:
            cleanup_temp_files()
            st.session_state.cleanup_done = True
            
        st.title("🎨 AI Media Generator")
        
        # Initialize generators
        prodia, pollinations, stability, content_gen, pdf_gen, flux, mochi = initialize_generators()
        
        # Sidebar for generation type selection
        generation_type = st.sidebar.radio(
            "Select Generation Type",
            ["Image", "Video", "PDF Document"]
        )
        
        if generation_type in ["Image", "Video"]:
            service = st.sidebar.radio(
                "Select Service",
                ["FLUX", "Mochi", "Prodia", "Pollinations.ai"] if generation_type == "Image" else ["Mochi", "Prodia", "Pollinations.ai"]
            )
            
            # Model selection based on service
            if service == "Prodia":
                model = st.sidebar.selectbox(
                    "Select Model",
                    list(Config.PRODIA_MODELS.keys())
                )
                model_id = Config.PRODIA_MODELS[model]
            elif service in ["FLUX", "Mochi"]:
                # Advanced settings for FLUX/Mochi
                num_steps = st.sidebar.slider("Number of steps", 20, 100, 50)
                guidance_scale = st.sidebar.slider("Guidance scale", 1.0, 20.0, 7.5)
                if service == "Mochi":
                    num_frames = st.sidebar.slider("Number of frames", 8, 32, 16)
            else:
                model = st.sidebar.selectbox(
                    "Select Model",
                    list(Config.POLLINATIONS_MODELS.keys())
                )
                model_id = Config.POLLINATIONS_MODELS[model]
            
            # Video generation settings for other services
            if service not in ["FLUX", "Mochi"] and generation_type == "Video":
                cfg_scale = st.sidebar.selectbox(
                    "CFG Scale",
                    Config.VIDEO_SETTINGS["cfg_scale_options"],
                    index=3  # Default to 7.0
                )
                
                motion_bucket_id = st.sidebar.selectbox(
                    "Motion Amount",
                    Config.VIDEO_SETTINGS["motion_bucket_options"],
                    index=0  # Default to 127
                )
                
                frames = st.sidebar.selectbox(
                    "Number of Frames",
                    Config.VIDEO_SETTINGS["frame_options"],
                    index=0  # Default to 14
                )
                
                use_random_seed = st.sidebar.checkbox("Use Random Seed", value=True)
        else:  # PDF Document
            st.subheader("Generate PDF Document")
            topic = st.text_input("Enter your document topic")
            
            if st.button("Generate Document"):
                if not topic:
                    st.error("Please enter a topic!")
                    return
                    
                with st.spinner("Generating document structure..."):
                    # Generate document structure
                    structure = content_gen.generate_content_structure(topic)
                    
                    if not structure:
                        st.error("Failed to generate document structure")
                        return
                    
                    # Show structure preview
                    st.write("Document Structure:")
                    st.json(structure)
                    
                    # Generate content for each section
                    contents = {}
                    with st.spinner("Generating content..."):
                        for section in structure["sections"]:
                            section_content = content_gen.generate_section_content(
                                section["heading"],
                                section["subheadings"]
                            )
                            if section_content:
                                contents[section["heading"]] = section_content
                    
                    # Generate PDF
                    with st.spinner("Creating PDF..."):
                        os.makedirs(Config.PDF_SETTINGS["temp_directory"], exist_ok=True)
                        output_path = os.path.join(
                            Config.PDF_SETTINGS["temp_directory"],
                            f"{int(time.time())}_{Config.PDF_SETTINGS['default_filename']}"
                        )
                        
                        pdf_path = pdf_gen.generate_pdf(
                            structure["title"],
                            structure["sections"],
                            contents,
                            output_path
                        )
                        
                        if pdf_path and os.path.exists(pdf_path):
                            with open(pdf_path, "rb") as f:
                                st.download_button(
                                    "Download PDF",
                                    f,
                                    file_name=os.path.basename(pdf_path),
                                    mime="application/pdf"
                                )
                        else:
                            st.error("Failed to generate PDF")

        # Main interface
        prompt = st.text_area("Enter your prompt", height=100)
        negative_prompt = st.text_area("Enter negative prompt (optional)", height=50)
        
        if st.button(f"Generate {generation_type}"):
            if not prompt:
                st.error("Please enter a prompt!")
                return
                
            with st.spinner(f"Generating your {generation_type.lower()}..."):
                try:
                    if generation_type == "Image":
                        if service == "FLUX":
                            image = flux.generate_image(
                                prompt=prompt,
                                negative_prompt=negative_prompt,
                                num_inference_steps=num_steps,
                                guidance_scale=guidance_scale
                            )
                            if image:
                                st.success("Image generated successfully!")
                                # Save temporary image
                                temp_path = "temp_flux_image.png"
                                try:
                                    image.save(temp_path)
                                    st.image(temp_path, caption=prompt)
                                    # Offer download
                                    with open(temp_path, "rb") as f:
                                        st.download_button(
                                            "Download Image",
                                            f,
                                            file_name="flux_generated_image.png",
                                            mime="image/png"
                                        )
                                finally:
                                    cleanup_temp_files()
                        elif service == "Prodia":
                            media_url = prodia.generate_image(prompt, model_id)
                            if media_url:
                                st.success("Image generated successfully!")
                                st.image(media_url, caption=prompt)
                        else:
                            media_url = pollinations.generate_image(prompt, model_id)
                            if media_url:
                                st.success("Image generated successfully!")
                                st.image(media_url, caption=prompt)
                    elif generation_type == "Video":
                        if service == "Mochi":
                            frames = mochi.generate_video(
                                prompt=prompt,
                                negative_prompt=negative_prompt,
                                num_inference_steps=num_steps,
                                guidance_scale=guidance_scale,
                                num_frames=num_frames
                            )
                            if frames:
                                st.success("Video generated successfully!")
                                # Save as GIF
                                temp_path = "temp_mochi_video.gif"
                                try:
                                    import imageio
                                    imageio.mimsave(temp_path, frames, fps=8)
                                    st.video(temp_path)
                                    # Offer download
                                    with open(temp_path, "rb") as f:
                                        st.download_button(
                                            "Download Video",
                                            f,
                                            file_name="mochi_generated_video.gif",
                                            mime="image/gif"
                                        )
                                finally:
                                    cleanup_temp_files()
                        else:
                            seed = random.randint(0, 2**32 - 1) if use_random_seed else None
                            video_path = stability.generate_video(
                                prompt=prompt,
                                cfg_scale=cfg_scale,
                                motion_bucket_id=motion_bucket_id,
                                frames=frames,
                                seed=seed
                            )
                            
                            if video_path:
                                st.success("Video generated successfully!")
                                st.video(video_path)
                                # Cleanup temporary file
                                stability.cleanup_temp_files(video_path)
                            else:
                                st.error("Failed to generate video. Please try again.")
                
                except Exception as e:
                    st.error(f"An error occurred: {str(e)}")
    except Exception as e:
        st.error(f"An unexpected error occurred: {str(e)}")
    finally:
        cleanup_temp_files()

if __name__ == "__main__":
    main()