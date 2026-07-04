import os
import sys
import argparse
import subprocess
from dotenv import load_dotenv
from agents.coordinator import CreatorsCoordinator

# Load environment variables (like GEMINI_API_KEY)
load_dotenv()

def run_streamlit():
    """Launches the Streamlit web application."""
    print("🚀 Launching Creators AI Web Interface...")
    current_dir = os.path.dirname(os.path.abspath(__file__))
    app_path = os.path.join(current_dir, "ui", "app.py")
    
    try:
        subprocess.run([sys.executable, "-m", "streamlit", "run", app_path, "--server.headless", "true"], check=True)
    except KeyboardInterrupt:
        print("\n👋 Web interface stopped.")
    except Exception as e:
        print(f"Error launching web interface: {e}")

def run_cli_pipeline(topic: str, api_key: str):
    """Runs the multi-agent pipeline in the console and saves the result."""
    print(f"\n📊 Starting Creators AI CLI Pipeline for: '{topic}'")
    
    if not api_key:
        print("❌ Error: Gemini API key is required. Pass it via --api-key or set GEMINI_API_KEY environment variable.")
        sys.exit(1)
        
    coordinator = CreatorsCoordinator(api_key=api_key)
    
    try:
        print("🧠 1. Running Trend Research Agent...")
        trend_report = coordinator.run_trend_research(topic)
        
        print("🎨 2. Running Title & Thumbnail Suggestion Agent...")
        titles_and_thumbnails = coordinator.run_thumbnail_title_suggestions(topic, trend_report)
        
        # Select default title & concept for demo script outline
        default_title = f"Creating the Ultimate Video about {topic}"
        default_concept = f"A high-contrast visual illustrating {topic} trends."
        
        print("📝 3. Running Script Planner Agent...")
        script_outline = coordinator.run_script_planner(default_title, default_concept, "10 minutes", "Educational")
        
        print("🔍 4. Running SEO Optimization Agent...")
        seo_metadata = coordinator.run_seo_optimization(default_title, script_outline, topic)
        
        # Save output to a markdown file
        output_filename = f"creators_ai_{topic.lower().replace(' ', '_')}.md"
        with open(output_filename, "w", encoding="utf-8") as f:
            f.write(f"""# Creators AI Video Package - {topic}

## 📊 PART 1: TREND RESEARCH REPORT
{trend_report}

---

## 🎨 PART 2: TITLE & THUMBNAIL CONCEPTS
{titles_and_thumbnails}

---

## 📝 PART 3: SCRIPT OUTLINE
{script_outline}

---

## 🔍 PART 4: SEO METADATA
{seo_metadata}
""")
        print(f"\n✅ Pipeline completed successfully! Full package saved to: {output_filename}")
        
    except Exception as e:
        print(f"\n❌ Error executing pipeline: {e}")

def main():
    parser = argparse.ArgumentParser(description="Creators AI - YouTube Creator Intelligence System")
    parser.add_argument("--topic", type=str, help="Topic keyword to run the pipeline on (CLI mode)")
    parser.add_argument("--api-key", type=str, help="Gemini API Key (CLI mode)")
    parser.add_argument("--ui", action="store_true", help="Force launching the Streamlit UI (default if no topic is provided)")
    
    args = parser.parse_args()
    
    # If a topic is provided, run in CLI mode
    if args.topic:
        api_key = args.api_key or os.getenv("GEMINI_API_KEY", "")
        run_cli_pipeline(args.topic, api_key)
    else:
        # Otherwise, run in UI mode
        run_streamlit()

if __name__ == "__main__":
    main()
