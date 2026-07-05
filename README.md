# 🚀 Creators AI — YouTube Creator Intelligence System

Creators AI is a powerful, production-ready **multi-agent orchestration system** designed to empower content creators. By automating the tedious parts of the content production pipeline—trend research, title & thumbnail brainstorming, structured script drafting, and SEO optimization—Creators AI helps you focus on what matters most: creating great content. 🎬✨

---

## 🌟 Key Features

The system consists of **four specialized AI Agents** working in harmony under a centralized workflow coordinator:

*   **📊 Trend Research Agent**: Gathers real-time intelligence by scraping YouTube view counts, analyzing Reddit discussions, and parsing Google News RSS feeds to identify target audience pain points and trending content angles.
*   **🎨 Title & Thumbnail Agent**: Brainstorms 5 high-CTR title variations paired with detailed visual layout descriptions. It integrates with **Pollinations.ai** to generate and display instant AI thumbnail background previews.
*   **📝 Script Planner Agent**: Outlines high-retention video structures including hooks, pacing, transitions, visual cues, B-roll recommendations, and speaker direction.
*   **🔍 SEO Optimization Agent**: Generates search-friendly YouTube descriptions, video chapters with timestamps, tags, hashtags, and calculates an overall SEO optimization score.

---

## 🏗️ System Architecture

To keep the pipeline organized and prevent context congestion, the system uses a **Workflow Coordinator** to manage the execution order and transition data between agents.

```mermaid
graph TD
    %% Define styles for distinct nodes
    classDef coordinator fill:#EBF3FF,stroke:#2B76D2,stroke-width:2px,color:#1A237E,font-weight:bold;
    classDef agent fill:#FFF3E0,stroke:#FF9800,stroke-width:2px,color:#E65100,font-weight:bold;
    classDef tool fill:#E8F5E9,stroke:#4CAF50,stroke-width:2px,color:#1B5E20;
    classDef io fill:#ECEFF1,stroke:#607D8B,stroke-width:2px,color:#263238;

    %% Workflow Flowchart
    Input([💡 Creator Topic Input])
    Coord[🔄 Workflow Coordinator]
    
    %% Trend Phase
    AgentTrend[📊 Trend Research Agent]
    ToolYT[(🎥 YouTube Search)]
    ToolReddit[(🤖 Reddit Search)]
    ToolNews[(📰 Google News RSS)]
    
    %% Title/Thumbnail Phase
    AgentThumb[🎨 Title & Thumbnail Agent]
    ToolPollinations[(🖼️ Pollinations.ai)]
    
    %% Script & SEO Phases
    AgentScript[📝 Script Planner Agent]
    AgentSEO[🔍 SEO Agent]
    
    Output([📦 Streamlit UI / Markdown Package])

    %% Connections
    Input --> Coord
    
    %% Step 1
    Coord ==> |"1. Request Analysis"| AgentTrend
    AgentTrend --> ToolYT
    AgentTrend --> ToolReddit
    AgentTrend --> ToolNews
    AgentTrend ==> |"Trend Report"| Coord
    
    %% Step 2
    Coord ==> |"2. Request Title & Concept"| AgentThumb
    AgentThumb --> ToolPollinations
    AgentThumb ==> |"Titles & Visual Prompts"| Coord
    
    %% Step 3
    Coord ==> |"3. Request Outline"| AgentScript
    AgentScript ==> |"Pacing, Hook & Script Outline"| Coord
    
    %% Step 4
    Coord ==> |"4. Request SEO Tuning"| AgentSEO
    AgentSEO ==> |"Chapters, Description & Tags"| Coord
    
    Coord --> Output

    %% Assign classes to nodes
    class Input,Output io;
    class Coord coordinator;
    class AgentTrend,AgentThumb,AgentScript,AgentSEO agent;
    class ToolYT,ToolReddit,ToolNews,ToolPollinations tool;
```

---

## 🛠️ Tech Stack & Integrations

*   **Core Logic**: Python 3.9+ 🐍
*   **Orchestration**: Custom state-based Coordinator Pattern 🔄
*   **AI Engine**: Gemini 2.5 Flash Lite via the official `google-genai` SDK 🧠
*   **Frontend**: Streamlit (custom styling, glassmorphism, responsive tabs) 💻
*   **APIs & Data Scraping**:
    *   `youtube-search-python` for fetching video metadata 🎥
    *   Reddit search parsing for community discussions 🤖
    *   Google News RSS parser for trending current events 📰
    *   `Pollinations.ai` free image generator for live thumbnail rendering 🖼️

---

## ⚙️ Setup & Installation

### 1️⃣ Prerequisites
Make sure you have Python 3.9 or higher installed on your system.

### 2️⃣ Clone & Install Dependencies
Navigate to your project directory and run:
```bash
pip install -r requirements.txt
```

### 3️⃣ Configure API Credentials (Optional)
The system is **pre-configured with a Gemini API Key**, so you can run the agents out of the box without providing your own.

If you wish to override the pre-configured key and use your own:
*   Set the `GEMINI_API_KEY` environment variable or create a `.env` file in the root directory:
    ```env
    GEMINI_API_KEY=your_custom_gemini_api_key
    ```
*   Or paste your custom key directly into the sidebar input field in the web dashboard.

---

## 🚀 Running the Application

### Option A: Launch Interactive Web Dashboard (Recommended) 🖥️
Run the main script without parameters to start the Streamlit-based web dashboard:
```bash
python main.py
```
This will start the server and open a browser tab (typically at `http://localhost:8501`). The UI features:
*   Interactive configurations (video duration, tone, and optional custom API key override).
*   Live progress bars and log outputs as agents process details.
*   Editable agent outputs, allowing you to fine-tune a title before generating the script.
*   One-click download of the complete video production package.

### Option B: Run Automated CLI Pipeline ⚙️
To quickly generate a complete video package straight to your filesystem using the pre-configured key:
```bash
python main.py --topic "learning rust programming"
```
*(Note: You can optionally pass your own key by appending `--api-key "YOUR_GEMINI_API_KEY"` to the command).*

This runs the full multi-agent pipeline sequentially and writes the output directly to a file named:
`creators_ai_learning_rust_programming.md`.

---

## 📂 Project Structure

```text
creatoros-ai/
├── agents/             # Agent definitions & prompts
│   ├── coordinator.py  # Orchestrates flow & maintains pipeline state
│   ├── script_agent.py # Hook, pacing, and visual-cues planning
│   ├── seo_agent.py    # Chapters, tags, description, and score
│   ├── thumbnail_agent.py # Title brainstorm & Pollinations.ai mockup
│   └── trend_agent.py  # YouTube/Reddit/News aggregator & analyzer
├── prompts/            # System instruction text files for agents
├── tools/              # Scrapers and API integration scripts
├── ui/                 # Streamlit web dashboard application
├── main.py             # Main entry point (CLI/Web router)
└── requirements.txt    # Required python packages
```
