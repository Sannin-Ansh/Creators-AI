import streamlit as st
import os
import sys
import re
from PIL import Image
import requests
from io import BytesIO

# Add parent directory to path so we can import agents and tools
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from agents.coordinator import CreatorsCoordinator
from agents.thumbnail_agent import ThumbnailAgent

# Set page config for beautiful layout
st.set_page_config(
    page_title="Creators AI - YouTube Creator Intelligence System",
    page_icon="🚀",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom Styling for Premium Look
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Outfit:wght@300;400;600;800&display=swap');
    
    html, body, [class*="css"] {
        font-family: 'Outfit', sans-serif;
    }
    
    .main-title {
        background: linear-gradient(135deg, #FF007A 0%, #7928CA 50%, #FF0055 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        font-size: 3.5rem;
        font-weight: 800;
        margin-bottom: 0.2rem;
        text-shadow: 0px 4px 20px rgba(121, 40, 202, 0.15);
    }
    
    .sub-title {
        color: #8E8E93;
        font-size: 1.25rem;
        margin-bottom: 2rem;
        font-weight: 300;
    }
    
    .card {
        background: rgba(255, 255, 255, 0.03);
        border-radius: 16px;
        padding: 24px;
        border: 1px solid rgba(255, 255, 255, 0.08);
        box-shadow: 0 8px 32px 0 rgba(0, 0, 0, 0.2);
        backdrop-filter: blur(8px);
        margin-bottom: 1.5rem;
    }
    
    .agent-header {
        display: flex;
        align-items: center;
        gap: 12px;
        margin-bottom: 1rem;
        padding-bottom: 0.5rem;
        border-bottom: 1px solid rgba(255, 255, 255, 0.1);
    }
    
    .agent-icon {
        font-size: 2rem;
    }
    
    .agent-name {
        font-size: 1.5rem;
        font-weight: 600;
        background: linear-gradient(90deg, #FFFFFF, #B3B3B3);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
    }
    
    .stButton>button {
        background: linear-gradient(135deg, #FF0055 0%, #7928CA 100%);
        color: white;
        border: none;
        padding: 10px 24px;
        border-radius: 8px;
        font-weight: 600;
        transition: all 0.3s ease;
        box-shadow: 0 4px 15px rgba(255, 0, 85, 0.2);
    }
    
    .stButton>button:hover {
        transform: translateY(-2px);
        box-shadow: 0 6px 20px rgba(255, 0, 85, 0.4);
        background: linear-gradient(135deg, #FF007A 0%, #8A2BE2 100%);
        color: white;
    }
</style>
""", unsafe_allow_html=True)

# Initialize Session State
if "api_key" not in st.session_state:
    st.session_state.api_key = os.getenv("GEMINI_API_KEY", "")

if "topic" not in st.session_state:
    st.session_state.topic = ""

if "duration" not in st.session_state:
    st.session_state.duration = "10 minutes"

if "tone" not in st.session_state:
    st.session_state.tone = "Educational"

if "trend_report" not in st.session_state:
    st.session_state.trend_report = ""

if "titles_and_thumbnails" not in st.session_state:
    st.session_state.titles_and_thumbnails = ""

if "chosen_title" not in st.session_state:
    st.session_state.chosen_title = ""

if "chosen_thumbnail" not in st.session_state:
    st.session_state.chosen_thumbnail = ""

if "script_outline" not in st.session_state:
    st.session_state.script_outline = ""

if "seo_metadata" not in st.session_state:
    st.session_state.seo_metadata = ""

if "thumbnail_prompt" not in st.session_state:
    st.session_state.thumbnail_prompt = ""

if "generated_thumbnail_url" not in st.session_state:
    st.session_state.generated_thumbnail_url = ""

# Sidebar Configuration
st.sidebar.image("https://img.icons8.com/?size=100&id=19318&format=png", width=80)
st.sidebar.markdown("# Creators AI Config")
st.sidebar.markdown("---")

st.sidebar.info("🤖 AI Engine: Active (Pre-configured)")

st.sidebar.markdown("### Video Planning Options")
st.session_state.duration = st.sidebar.selectbox(
    "⏱️ Target Duration",
    ["3 minutes (Short)", "5 minutes", "10 minutes (Standard)", "15 minutes", "20+ minutes (Deep Dive)"],
    index=2
)

st.session_state.tone = st.sidebar.selectbox(
    "🎙️ Voice/Tone Style",
    ["Casual & Friendly", "Energetic & Enthusiastic", "Educational & Informative", "Dramatic & Storytelling", "Professional & Formal"],
    index=2
)

st.sidebar.markdown("---")
st.sidebar.markdown("""
**About Creators AI**
Creators AI is a multi-agent workflow designed to automate topic research, Title/Thumbnail ideation, Script outline planning, and SEO keyword mapping.
""")

# Setup Coordinator
coordinator = CreatorsCoordinator(api_key=st.session_state.api_key)

# App Title & Subtitle
st.markdown("<h1 class='main-title'>Creators AI</h1>", unsafe_allow_html=True)
st.markdown("<p class='sub-title'>YouTube Creator Intelligence System — Powered by Gemini 3.1</p>", unsafe_allow_html=True)

# Main Prompt warning if API key is missing
if not st.session_state.api_key:
    st.error("❌ Gemini API Key is missing! Please configure the GEMINI_API_KEY environment variable or verify the application settings.")
    st.stop()

# Layout Tabs
tabs = st.tabs([
    "📊 Trend Research",
    "🎨 Titles & Thumbnails",
    "📝 Script Planner",
    "🔍 SEO & Metadata",
    "📈 Export Dashboard"
])

# Utility to parse image prompts from generated content
def extract_image_prompt(content):
    if not content:
        return ""
    # Try finding patterns like "Image Generation Prompt:" or "Prompt:"
    match = re.search(r"(?:image generation prompt|prompt):\s*(.+)", content, re.IGNORECASE)
    if match:
        return match.group(1).strip()
    return ""

# Tab 1: Trend Research Agent
with tabs[0]:
    st.markdown("""
    <div class='card'>
        <div class='agent-header'>
            <span class='agent-icon'>📊</span>
            <span class='agent-name'>Trend Research Agent</span>
        </div>
        <p>Analyzes live YouTube search results, Reddit discussion threads, and Google News RSS feeds to identify high-interest sub-topics, audience pain points, and current viral angles.</p>
    </div>
    """, unsafe_allow_html=True)
    
    topic_input = st.text_input("Enter your seed topic or niche (e.g. 'building SaaS with AI', 'productivity hacks'):", value=st.session_state.topic)
    if topic_input:
        st.session_state.topic = topic_input

    col1, col2 = st.columns([1, 4])
    with col1:
        run_research = st.button("Run Trend Research")
        
    with col2:
        if run_research:
            if not st.session_state.topic:
                st.error("Please enter a topic first!")
            else:
                with st.spinner("Agent searching YouTube, Reddit, and RSS feeds..."):
                    try:
                        coordinator.update_api_key(st.session_state.api_key)
                        report = coordinator.run_trend_research(st.session_state.topic)
                        st.session_state.trend_report = report
                        st.success("Trend Research completed!")
                    except Exception as e:
                        st.error(f"Error executing agent: {e}")
                        
    if st.session_state.trend_report:
        st.markdown("### Agent Output: Trend Analysis Report")
        # Allow editing of the output
        edited_report = st.text_area("You can edit the report to customize before feeding it to the next agent:", 
                                     value=st.session_state.trend_report, 
                                     height=400)
        st.session_state.trend_report = edited_report
        st.markdown("---")
        st.markdown("#### Preview:")
        st.markdown(st.session_state.trend_report)

# Tab 2: Title & Thumbnail Agent
with tabs[1]:
    st.markdown("""
    <div class='card'>
        <div class='agent-header'>
            <span class='agent-icon'>🎨</span>
            <span class='agent-name'>Thumbnail & Title Suggestion Agent</span>
        </div>
        <p>Uses the Trend Report to brainstorm high-click-through-rate (CTR) video titles and matches them with creative thumbnail layouts, color suggestions, and text-to-image prompts.</p>
    </div>
    """, unsafe_allow_html=True)
    
    if not st.session_state.trend_report:
        st.info("⚠️ Please complete **Step 1: Trend Research** first, or paste a trend report below to proceed.")
        trend_report_fallback = st.text_area("Paste Trend Report manually:", height=200)
        if trend_report_fallback:
            st.session_state.trend_report = trend_report_fallback
            st.rerun()
    else:
        col1, col2 = st.columns([1, 4])
        with col1:
            run_thumbnail = st.button("Generate Title/Thumbnails")
        with col2:
            if run_thumbnail:
                with st.spinner("Brainstorming title formulas and visual layout concepts..."):
                    try:
                        coordinator.update_api_key(st.session_state.api_key)
                        result = coordinator.run_thumbnail_title_suggestions(
                            st.session_state.topic, 
                            st.session_state.trend_report
                        )
                        st.session_state.titles_and_thumbnails = result
                        # Seed thumbnail prompt suggestions
                        extracted = extract_image_prompt(result)
                        if extracted:
                            st.session_state.thumbnail_prompt = extracted
                        else:
                            st.session_state.thumbnail_prompt = f"Cinematic epic scene representing {st.session_state.topic}, high contrast, youtube thumbnail layout style, vibrant colors"
                        st.success("Title & Thumbnail suggestions generated!")
                    except Exception as e:
                        st.error(f"Error executing agent: {e}")
                        
        if st.session_state.titles_and_thumbnails:
            st.markdown("### Agent Output: Title & Thumbnail Concepts")
            edited_concepts = st.text_area("Review and modify the suggestions:", 
                                           value=st.session_state.titles_and_thumbnails, 
                                           height=300)
            st.session_state.titles_and_thumbnails = edited_concepts
            
            st.markdown("---")
            st.markdown("### 🖼️ Thumbnail Visual Mockup Generator")
            st.markdown("Generate a mockup using a free Stable Diffusion image generator (Pollinations.ai). Customize the image generation prompt below:")
            
            # Input for image prompt
            prompt_val = st.text_input("Stable Diffusion Prompt (keep it descriptive, no text overlays):", 
                                       value=st.session_state.thumbnail_prompt or f"Cinematic lighting, high-contrast digital art about {st.session_state.topic}")
            st.session_state.thumbnail_prompt = prompt_val
            
            seed_val = st.number_input("Random Seed (change to get different styles)", min_value=1, max_value=99999, value=42)
            
            if st.button("Generate Thumbnail Visual Mockup"):
                with st.spinner("Generating AI visual..."):
                    t_agent = ThumbnailAgent()
                    url = t_agent.get_thumbnail_mockup_url(prompt_val, seed=seed_val)
                    st.session_state.generated_thumbnail_url = url
            
            if st.session_state.generated_thumbnail_url:
                st.markdown("#### Generated Base Image Preview:")
                # Fetch image to display nicely
                try:
                    response = requests.get(st.session_state.generated_thumbnail_url)
                    img = Image.open(BytesIO(response.content))
                    st.image(img, caption="AI-Generated Thumbnail Background Mockup (16:9)", use_container_width=True)
                    st.info("💡 Tip: You can right-click the image to save it, or use the prompt directly in Midjourney/DALL-E for production!")
                except Exception as ex:
                    st.error(f"Could not load image from API: {ex}")
            
            st.markdown("---")
            st.markdown("#### Text suggestions:")
            st.markdown(st.session_state.titles_and_thumbnails)

# Tab 3: Script Planner Agent
with tabs[2]:
    st.markdown("""
    <div class='card'>
        <div class='agent-header'>
            <span class='agent-icon'>📝</span>
            <span class='agent-name'>Script Planner Agent</span>
        </div>
        <p>Takes the selected title, chosen thumbnail concept, duration, and tone settings to outline a comprehensive video script structure. Focuses heavily on high-retention hooks and detailed visual cues.</p>
    </div>
    """, unsafe_allow_html=True)
    
    if not st.session_state.titles_and_thumbnails:
        st.info("⚠️ Please complete **Step 2: Titles & Thumbnails** first to select your video details.")
    else:
        st.markdown("### Video Settings Setup")
        title_sel = st.text_input("Enter Chosen Video Title:", value=st.session_state.chosen_title or f"How I Mastered {st.session_state.topic}")
        st.session_state.chosen_title = title_sel
        
        thumb_sel = st.text_area("Enter Selected Thumbnail Visual Concept:", value=st.session_state.chosen_thumbnail or "A high-contrast visual showing progress.")
        st.session_state.chosen_thumbnail = thumb_sel
        
        col1, col2 = st.columns([1, 4])
        with col1:
            run_script = st.button("Generate Script Plan")
        with col2:
            if run_script:
                with st.spinner("Drafting full video structure, pacing, B-roll cues, and opening hooks..."):
                    try:
                        coordinator.update_api_key(st.session_state.api_key)
                        script = coordinator.run_script_planner(
                            title_sel,
                            thumb_sel,
                            duration=st.session_state.duration,
                            tone=st.session_state.tone
                        )
                        st.session_state.script_outline = script
                        st.success("Script Outline generated!")
                    except Exception as e:
                        st.error(f"Error executing agent: {e}")
                        
        if st.session_state.script_outline:
            st.markdown("### Agent Output: Script Outline")
            edited_script = st.text_area("Review and refine the script outline:", 
                                         value=st.session_state.script_outline, 
                                         height=400)
            st.session_state.script_outline = edited_script
            st.markdown("---")
            st.markdown("#### Preview:")
            st.markdown(st.session_state.script_outline)

# Tab 4: SEO Agent
with tabs[3]:
    st.markdown("""
    <div class='card'>
        <div class='agent-header'>
            <span class='agent-icon'>🔍</span>
            <span class='agent-name'>SEO Optimization Agent</span>
        </div>
        <p>Analyzes your script outline and target topic to draft search-engine-friendly metadata, tags, hashtags, and a detailed, chaptered video description designed to maximize YouTube search rankings.</p>
    </div>
    """, unsafe_allow_html=True)
    
    if not st.session_state.script_outline:
        st.info("⚠️ Please complete **Step 3: Script Planner** first to outline your video content.")
    else:
        st.markdown("### Metadata Parameters")
        target_kw = st.text_area("Keywords / Search Queries (separated by commas):", 
                                 value=f"{st.session_state.topic}, {st.session_state.topic} tutorial, how to do {st.session_state.topic}")
        
        col1, col2 = st.columns([1, 4])
        with col1:
            run_seo = st.button("Generate SEO Package")
        with col2:
            if run_seo:
                with st.spinner("Compiling description, tags, chapters, and SEO checks..."):
                    try:
                        coordinator.update_api_key(st.session_state.api_key)
                        seo = coordinator.run_seo_optimization(
                            st.session_state.chosen_title,
                            st.session_state.script_outline,
                            target_kw
                        )
                        st.session_state.seo_metadata = seo
                        st.success("SEO Package compiled!")
                    except Exception as e:
                        st.error(f"Error executing agent: {e}")
                        
        if st.session_state.seo_metadata:
            st.markdown("### Agent Output: SEO & Metadata Package")
            edited_seo = st.text_area("Edit description, tags, or hashtags:", 
                                       value=st.session_state.seo_metadata, 
                                       height=400)
            st.session_state.seo_metadata = edited_seo
            st.markdown("---")
            st.markdown("#### Preview:")
            st.markdown(st.session_state.seo_metadata)

# Tab 5: Export Dashboard
with tabs[4]:
    st.markdown("""
    <div class='card'>
        <div class='agent-header'>
            <span class='agent-icon'>📈</span>
            <span class='agent-name'>Creators AI Dashboard</span>
        </div>
        <p>Review the compiled output from all agents. You can download the complete content bundle to export to your script files or copy directly into YouTube Studio.</p>
    </div>
    """, unsafe_allow_html=True)
    
    # Check if any content is generated
    has_content = any([
        st.session_state.trend_report,
        st.session_state.titles_and_thumbnails,
        st.session_state.script_outline,
        st.session_state.seo_metadata
    ])
    
    if not has_content:
        st.info("No content has been generated yet. Go through the tabs to trigger the Creators AI agents!")
    else:
        # Build compilation markdown
        package_md = f"""# Creators AI - Video Production Package
Topic: {st.session_state.topic}
Tone: {st.session_state.tone}
Duration: {st.session_state.duration}

---

## 📊 PART 1: TREND RESEARCH
{st.session_state.trend_report}

---

## 🎨 PART 2: TITLES & THUMBNAIL CONCEPTS
{st.session_state.titles_and_thumbnails}
Image Generation Prompt: {st.session_state.thumbnail_prompt}

---

## 📝 PART 3: SCRIPT OUTLINE
{st.session_state.script_outline}

---

## 🔍 PART 4: SEO & METADATA
{st.session_state.seo_metadata}
"""
        st.markdown("### Complete Video Package Overview")
        
        # Download button
        st.download_button(
            label="📥 Download Complete Package (.md)",
            data=package_md,
            file_name=f"creators_ai_{st.session_state.topic.lower().replace(' ', '_')}.md",
            mime="text/markdown"
        )
        
        # Expanders to read
        with st.expander("📊 View Trend Report", expanded=False):
            st.markdown(st.session_state.trend_report)
            
        with st.expander("🎨 View Titles & Thumbnails", expanded=False):
            if st.session_state.generated_thumbnail_url:
                st.image(st.session_state.generated_thumbnail_url, caption="Generated Thumbnail Mockup Background", use_container_width=True)
            st.markdown(st.session_state.titles_and_thumbnails)
            
        with st.expander("📝 View Script Outline", expanded=False):
            st.markdown(st.session_state.script_outline)
            
        with st.expander("🔍 View SEO & Metadata", expanded=False):
            st.markdown(st.session_state.seo_metadata)
            
        st.success("🎉 Creators AI has successfully generated your full video concept workflow!")
