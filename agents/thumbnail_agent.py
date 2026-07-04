import os
import logging
import urllib.parse
from google import genai
from google.genai import types

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class ThumbnailAgent:
    def __init__(self, api_key: str = None):
        """
        Initializes the ThumbnailAgent.
        If api_key is not provided, it looks for the GEMINI_API_KEY environment variable.
        """
        self.api_key = api_key or os.getenv("GEMINI_API_KEY")
        
        # Load system prompt
        current_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        prompt_path = os.path.join(current_dir, "prompts", "thumbnail_prompt.txt")
        try:
            with open(prompt_path, "r", encoding="utf-8") as f:
                self.system_prompt = f.read()
        except FileNotFoundError:
            logger.error(f"Prompt file not found at {prompt_path}")
            self.system_prompt = "You are the Thumbnail and Title Suggestion Agent for Creators AI. Generate title variations and thumbnail concepts."

    def run(self, topic: str, trend_report: str) -> str:
        """
        Generates Title and Thumbnail recommendations based on the topic and trend report.
        """
        if not self.api_key:
            raise ValueError("Gemini API key is required. Please set it in the Streamlit UI or environment.")
        
        # Initialize Gemini Client
        client = genai.Client(api_key=self.api_key)
        
        user_input_prompt = f"""
Chosen Video Topic/Angle: {topic}

=== TREND REPORT SUMMARY ===
{trend_report}

Please generate title ideas and detailed thumbnail concepts based on this input.
"""
        
        try:
            response = client.models.generate_content(
                model="gemini-2.5-flash",
                contents=user_input_prompt,
                config=types.GenerateContentConfig(
                    system_instruction=self.system_prompt
                )
            )
            return response.text
        except Exception as e:
            logger.error(f"Error during Gemini generation: {e}")
            raise e

    def get_thumbnail_mockup_url(self, prompt: str, seed: int = 42) -> str:
        """
        Generates a URL to create a mock thumbnail image using Pollinations.ai.
        """
        cleaned_prompt = urllib.parse.quote(prompt.strip())
        # Use Pollinations.ai for free instant image generation
        return f"https://image.pollinations.ai/prompt/{cleaned_prompt}?width=1280&height=720&seed={seed}&nologo=true"
