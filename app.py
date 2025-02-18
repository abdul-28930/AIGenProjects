import streamlit as st
from src.generators.prodia import ProdiaGenerator
from src.generators.pollinations import PollinationsGenerator
from src.utils.config import Config
import time

st.set_page_config(
    page_title="AI Image Generator",
    page_icon="🎨",
    layout="wide"
)

def initialize_generators():
    prodia = ProdiaGenerator(Config.PRODIA_API_KEY)
    pollinations = PollinationsGenerator()
    return prodia, pollinations

def main():
    st.title("🎨 AI Image Generator")
    
    # Initialize generators
    prodia, pollinations = initialize_generators()
    
    # Sidebar for service selection
    service = st.sidebar.radio(
        "Select Service",
        ["Prodia", "Pollinations.ai"]
    )
    
    # Model selection based on service
    if service == "Prodia":
        model = st.sidebar.selectbox(
            "Select Model",
            list(Config.PRODIA_MODELS.keys())
        )
        model_id = Config.PRODIA_MODELS[model]
    else:
        model = st.sidebar.selectbox(
            "Select Model",
            list(Config.POLLINATIONS_MODELS.keys())
        )
        model_id = Config.POLLINATIONS_MODELS[model]
    
    # Main interface
    prompt = st.text_area("Enter your prompt", height=100)
    
    if st.button("Generate Image"):
        if not prompt:
            st.error("Please enter a prompt!")
            return
            
        with st.spinner("Generating your image..."):
            try:
                if service == "Prodia":
                    image_url = prodia.generate_image(prompt, model_id)
                else:
                    image_url = pollinations.generate_image(prompt, model_id)
                
                if image_url:
                    st.success("Image generated successfully!")
                    st.image(image_url, caption=prompt)
                else:
                    st.error("Failed to generate image. Please try again.")
            
            except Exception as e:
                st.error(f"An error occurred: {str(e)}")

if __name__ == "__main__":
    main() 