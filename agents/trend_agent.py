import os
import logging
from google import genai
from google.genai import types
from tools.youtube_search import search_youtube
from tools.reddit_search import search_reddit
from tools.trends_tool import fetch_trending_topics

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class TrendAgent:
    def __init__(self, api_key: str = None):
        """
        Initializes the TrendAgent.
        If api_key is not provided, it looks for the GEMINI_API_KEY environment variable.
        """
        self.api_key = api_key or os.getenv("GEMINI_API_KEY")
        
        # Load system prompt
        current_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        prompt_path = os.path.join(current_dir, "prompts", "trend_prompt.txt")
        try:
            with open(prompt_path, "r", encoding="utf-8") as f:
                self.system_prompt = f.read()
        except FileNotFoundError:
            logger.error(f"Prompt file not found at {prompt_path}")
            self.system_prompt = "You are the Trend Research Agent for Creators AI. Analyze search data and produce a structured Trend Analysis Report."

    def run(self, topic: str) -> str:
        """
        Gathers YouTube, Reddit, and RSS Trends data for the topic,
        and generates a Trend Analysis Report using Gemini.
        """
        if not self.api_key:
            raise ValueError("Gemini API key is required. Please set it in the Streamlit UI or environment.")
        
        # Initialize Gemini Client
        client = genai.Client(api_key=self.api_key)
        
        # Gather data from tools
        youtube_data = search_youtube(topic, limit=5)
        reddit_data = search_reddit(topic, limit=5)
        trends_data = fetch_trending_topics(topic)
        
        # Format the gathered data for the prompt
        yt_summary = "\n".join([
            f"- Title: {item['title']}\n  Views: {item['views']} | Published: {item['published_time']} | Channel: {item['channel']}\n  Link: {item['link']}"
            for item in youtube_data
        ])
        
        reddit_summary = "\n".join([
            f"- Title: {item['title']}\n  Subreddit: {item['subreddit']} | Upvotes: {item['upvotes']} | Comments: {item['comments']}\n  Summary: {item['summary']}\n  Link: {item['link']}"
            for item in reddit_data
        ])
        
        trends_summary = "\n".join([
            f"- Title: {item['title']} | Source: {item['source']} | Date: {item['pub_date']}"
            for item in trends_data
        ])
        
        user_input_prompt = f"""
Seed Keyword / Topic: {topic}

=== YOUTUBE SEARCH RESULTS ===
{yt_summary}

=== REDDIT DISCUSSIONS ===
{reddit_summary}

=== GOOGLE TRENDS NEWS ===
{trends_summary}

Please analyze this data and generate a comprehensive Trend Analysis Report according to your system instructions.
"""
        
        try:
            # Use gemini-2.5-flash-lite as the default model
            response = client.models.generate_content(
                model="gemini-2.5-flash-lite",
                contents=user_input_prompt,
                config=types.GenerateContentConfig(
                    system_instruction=self.system_prompt
                )
            )
            return response.text
        except Exception as e:
            logger.error(f"Error during Gemini generation: {e}")
            raise e
