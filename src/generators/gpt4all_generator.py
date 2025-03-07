from gpt4all import GPT4All
from typing import Dict, List, Optional
import json

class ContentGenerator:
    def __init__(self):
        # Initialize with GPT4All-J model
        self.model = GPT4All("ggml-gpt4all-j-v1.3-groovy")
    
    def generate_content_structure(self, topic: str) -> Optional[Dict]:
        try:
            # Prompt for generating structure
            structure_prompt = f"""Create a detailed document structure for the topic "{topic}". 
            Format the response as JSON with the following structure:
            {{
                "title": "main title",
                "sections": [
                    {{
                        "heading": "section heading",
                        "subheadings": ["subheading1", "subheading2"]
                    }}
                ]
            }}
            Make it comprehensive but concise."""

            # Generate and parse response
            response = self.model.generate(structure_prompt, max_tokens=500)
            # Extract JSON from response
            json_str = response[response.find("{"):response.rfind("}")+1]
            return json.loads(json_str)

        except Exception as e:
            print(f"Error generating structure: {str(e)}")
            return None

    def generate_section_content(self, heading: str, subheadings: List[str]) -> Optional[Dict[str, str]]:
        try:
            content = {}
            # Generate content for main heading
            heading_prompt = f"""Write a detailed paragraph about "{heading}".
            Keep it informative and engaging. Be specific and factual."""
            
            content["main"] = self.model.generate(heading_prompt, max_tokens=200)

            # Generate content for each subheading
            for subheading in subheadings:
                subheading_prompt = f"""Write a concise paragraph about "{subheading}" 
                in the context of {heading}. Be specific and informative."""
                
                content[subheading] = self.model.generate(subheading_prompt, max_tokens=150)

            return content

        except Exception as e:
            print(f"Error generating content: {str(e)}")
            return None 