import logging
from agents.trend_agent import TrendAgent
from agents.thumbnail_agent import ThumbnailAgent
from agents.script_agent import ScriptAgent
from agents.seo_agent import SeoAgent

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class CreatorsCoordinator:
    """
    Coordinator class to manage execution of the multi-agent Creators AI pipeline.
    Ensures state transitions between Trend, Thumbnail, Script, and SEO Agents.
    """
    def __init__(self, api_key: str = None):
        self.api_key = api_key
        self.trend_agent = TrendAgent(api_key=api_key)
        self.thumbnail_agent = ThumbnailAgent(api_key=api_key)
        self.script_agent = ScriptAgent(api_key=api_key)
        self.seo_agent = SeoAgent(api_key=api_key)
        self.state = {
            "topic": "",
            "trend_report": "",
            "chosen_title": "",
            "chosen_thumbnail": "",
            "titles_and_thumbnails": "",
            "script_outline": "",
            "seo_metadata": ""
        }

    def update_api_key(self, api_key: str):
        """Updates the API key for all agents if changed in UI."""
        self.api_key = api_key
        self.trend_agent.api_key = api_key
        self.thumbnail_agent.api_key = api_key
        self.script_agent.api_key = api_key
        self.seo_agent.api_key = api_key

    def run_trend_research(self, topic: str) -> str:
        """Step 1: Trend Research Agent"""
        logger.info("Coordinator: Running Trend Research...")
        self.state["topic"] = topic
        report = self.trend_agent.run(topic)
        self.state["trend_report"] = report
        return report

    def run_thumbnail_title_suggestions(self, topic: str, trend_report: str) -> str:
        """Step 2: Title and Thumbnail Agent"""
        logger.info("Coordinator: Running Title & Thumbnail Suggestion...")
        result = self.thumbnail_agent.run(topic, trend_report)
        self.state["titles_and_thumbnails"] = result
        return result

    def run_script_planner(self, title: str, thumbnail_concept: str, duration: str, tone: str) -> str:
        """Step 3: Script Planner Agent"""
        logger.info("Coordinator: Running Script Planner...")
        self.state["chosen_title"] = title
        self.state["chosen_thumbnail"] = thumbnail_concept
        script = self.script_agent.run(title, thumbnail_concept, duration=duration, tone=tone)
        self.state["script_outline"] = script
        return script

    def run_seo_optimization(self, title: str, script_outline: str, target_keywords: str) -> str:
        """Step 4: SEO Agent"""
        logger.info("Coordinator: Running SEO Optimization...")
        seo = self.seo_agent.run(title, script_outline, target_keywords)
        self.state["seo_metadata"] = seo
        return seo

    def run_full_pipeline(self, topic: str, duration: str = "10 minutes", tone: str = "Casual") -> dict:
        """Runs the entire pipeline end-to-end automatically with default selections."""
        logger.info("Coordinator: Running full Creators AI pipeline...")
        
        # 1. Trend Research
        trend_report = self.run_trend_research(topic)
        
        # 2. Thumbnail & Title Suggestion
        titles_and_thumbnails = self.run_thumbnail_title_suggestions(topic, trend_report)
        
        # Extract a default title and thumbnail concept (heuristics or simply using first lines)
        # In full automatic mode, we will pass the whole report to the script and seo agents.
        default_title = f"Creating the Ultimate Video about {topic}"
        default_thumbnail = f"A high-contrast visual illustrating {topic} trends."
        
        # 3. Script Planner
        script = self.run_script_planner(default_title, default_thumbnail, duration, tone)
        
        # 4. SEO
        seo = self.run_seo_optimization(default_title, script, topic)
        
        return {
            "trend_report": trend_report,
            "titles_and_thumbnails": titles_and_thumbnails,
            "script_outline": script,
            "seo_metadata": seo
        }
