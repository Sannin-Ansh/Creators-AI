import os
import logging
from google import genai
from google.genai import types

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class SeoAgent:
    def __init__(self, api_key: str = None):
        """
        Initializes the SeoAgent.
        If api_key is not provided, it looks for the GEMINI_API_KEY environment variable.
        """
        self.api_key = api_key or os.getenv("GEMINI_API_KEY")
        
        # Load system prompt
        current_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        prompt_path = os.path.join(current_dir, "prompts", "seo_prompt.txt")
        try:
            with open(prompt_path, "r", encoding="utf-8") as f:
                self.system_prompt = f.read()
        except FileNotFoundError:
            logger.error(f"Prompt file not found at {prompt_path}")
            self.system_prompt = "You are the SEO Optimization Agent for Creators AI. Generate optimized descriptions, tags, and titles."

    def run(self, title: str, script_outline: str, target_keywords: str) -> str:
        """
        Generates SEO recommendations, descriptions, tags, hashtags, and score checklist.
        """
        if not self.api_key:
            raise ValueError("Gemini API key is required. Please set it in the Streamlit UI or environment.")
        
        # Initialize Gemini Client
        client = genai.Client(api_key=self.api_key)
        
        user_input_prompt = f"""
Video Title: {title}

=== SCRIPT OUTLINE ===
{script_outline}

=== TARGET KEYWORDS / SEARCH DATA ===
{target_keywords}

Please generate the SEO optimization package according to your system instructions.
"""
        
        try:
            response = client.models.generate_content(
                model="gemini-3.1-flash-lite",
                contents=user_input_prompt,
                config=types.GenerateContentConfig(
                    system_instruction=self.system_prompt
                )
            )
            return response.text
        except Exception as e:
            logger.error(f"Error during Gemini generation: {e}")
            raise e
