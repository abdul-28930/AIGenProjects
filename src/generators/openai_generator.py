from openai import OpenAI
from typing import Dict, List, Optional
import json
from src.utils.config import Config

class ContentGenerator:
    def __init__(self):
        self.client = OpenAI(api_key=Config.OPENAI_API_KEY)
        self.model = "gpt-4o-mini"  # Using GPT-4 Turbo

    def generate_content_structure(self, topic: str) -> Optional[Dict]:
        try:
            # Prompt for generating structure
            prompt = f"""Create a detailed document structure for the topic "{topic}".
            The response must be a valid JSON with this exact structure:
            {{
                "title": "main title",
                "sections": [
                    {{
                        "heading": "section heading",
                        "subheadings": ["subheading1", "subheading2"]
                    }}
                ]
            }}
            Make it comprehensive but concise with 3-4 sections and 2-3 subheadings each.
            Only return the JSON, no additional text."""

            response = self.client.chat.completions.create(
                model=self.model,
                messages=[
                    {"role": "system", "content": "You are a document structure expert. You create well-organized, logical document outlines."},
                    {"role": "user", "content": prompt}
                ],
                temperature=0.7,
                response_format={"type": "json_object"}
            )

            return json.loads(response.choices[0].message.content)

        except Exception as e:
            print(f"Error generating structure: {str(e)}")
            return None

    def generate_section_content(self, heading: str, subheadings: List[str]) -> Optional[Dict[str, str]]:
        try:
            content = {}
            
            # Generate main heading content
            main_prompt = f"""Write a detailed, informative paragraph about "{heading}".
            The content should be engaging, factual, and around 150 words.
            Focus on providing valuable insights and clear explanations."""

            main_response = self.client.chat.completions.create(
                model=self.model,
                messages=[
                    {"role": "system", "content": "You are an expert content writer who creates clear, engaging, and informative content."},
                    {"role": "user", "content": main_prompt}
                ],
                temperature=0.7
            )
            
            content["main"] = main_response.choices[0].message.content.strip()

            # Generate content for each subheading
            for subheading in subheadings:
                sub_prompt = f"""Write a concise but detailed paragraph about "{subheading}" 
                in the context of {heading}. The content should be around 100 words,
                specific, and informative."""

                sub_response = self.client.chat.completions.create(
                    model=self.model,
                    messages=[
                        {"role": "system", "content": "You are an expert content writer who creates clear, engaging, and informative content."},
                        {"role": "user", "content": sub_prompt}
                    ],
                    temperature=0.7
                )
                
                content[subheading] = sub_response.choices[0].message.content.strip()

            return content

        except Exception as e:
            print(f"Error generating content: {str(e)}")
            return None 