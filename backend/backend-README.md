# Professional Podcast Creator AI

Convert YouTube videos and/or research topics into high-quality podcast conversations using Gemini 2.5 and LangGraph.

## 🚀 Features

🎙️ **Multi-Modal Input**: YouTube videos, research topics, or both  
🤖 **Multi-Agent System**: Research, Video Analysis, Script Writing, Audio Production  
🎵 **Professional TTS**: Multi-speaker conversations with Alex & Sam  
📋 **Smart Metadata**: Auto-generated titles and descriptions  
⏱️ **Flexible Duration**: 4-6 minute professional podcasts

## Quick Start

### Prerequisites

- Python 3.11+
- [uv](https://docs.astral.sh/uv/) package manager
- Google Gemini API key

### Setup

1. **Clone and navigate to the project**:
```bash
git clone https://github.com/langchain-ai/multi-modal-researcher
cd multi-modal-researcher
```

2. **Set up environment variables**:
```bash
cp .env.example .env
```
Edit `.env` and [add your Google Gemini API key](https://ai.google.dev/gemini-api/docs/api-key):
```bash
GEMINI_API_KEY=your_api_key_here
PODCAST_HOST_NAME=Alex
PODCAST_EXPERT_NAME=Sam
PODCAST_DURATION_TARGET=5
```

3. **Run the development server**:

```bash
# Install uv package manager
curl -LsSf https://astral.sh/uv/install.sh | sh
# Install dependencies and start the LangGraph server
uvx --refresh --from "langgraph-cli[inmem]" --with-editable . --python 3.11 langgraph dev --allow-blocking
```

4. **Access the application**:

LangGraph will open in your browser.

```bash
╦  ┌─┐┌┐┌┌─┐╔═╗┬─┐┌─┐┌─┐┬ ┬
║  ├─┤││││ ┬║ ╦├┬┘├─┤├─┘├─┤
╩═╝┴ ┴┘└┘└─┘╚═╝┴└─┴ ┴┴  ┴ ┴

- 🚀 API: http://127.0.0.1:2024
- 🎨 Studio UI: https://smith.langchain.com/studio/?baseUrl=http://127.0.0.1:2024
- 📚 API Docs: http://127.0.0.1:2024/docs
```

## Input Options

### Option 1: Topic Only
```json
{
  "topic": "The future of renewable energy",
  "duration_minutes": 5
}
```

### Option 2: Video Only  
```json
{
  "video_url": "https://youtu.be/your_video_id",
  "duration_minutes": 4
}
```

### Option 3: Both Topic + Video
```json
{
  "topic": "AI and Climate Change",
  "video_url": "https://youtu.be/your_video_id", 
  "duration_minutes": 6
}
```

## Architecture

The system implements a **multi-agent LangGraph workflow**:

### Agent Roles

1. **Research Agent**: Web search and topic analysis using Gemini's Google Search
2. **Video Analysis Agent**: YouTube content extraction and analysis  
3. **Content Synthesizer**: Combines research and video insights
4. **Metadata Generator**: Creates titles, descriptions, and topic lists
5. **Script Writer & Audio Producer**: Generates conversation and TTS audio

### Workflow

```
Input Validation → Research Agent → Video Analysis Agent → Content Synthesis → Metadata Generator → Script Writer & Audio Producer → Output
```

The workflow intelligently routes based on available inputs:
- **Topic only**: Research Agent → Content Synthesis → ...
- **Video only**: Video Analysis Agent → Content Synthesis → ...  
- **Both**: Research Agent → Video Analysis Agent → Content Synthesis → ...

### Output

The system generates:

- **Podcast Title**: Engaging, professional title (60 chars max)
- **Podcast Description**: Hook-worthy description (150-200 words)
- **Podcast Script**: Natural conversation between Alex (host) & Sam (expert)
- **Audio File**: Multi-speaker TTS audio (`podcast_*.wav`)
- **Metadata**: Duration estimate and topics covered

## Configuration

### Model Settings
- `search_model`: Web search (default: "gemini-2.5-flash")
- `synthesis_model`: Content synthesis (default: "gemini-2.5-flash")  
- `video_model`: Video analysis (default: "gemini-2.5-flash")
- `tts_model`: Text-to-speech (default: "gemini-2.5-flash-preview-tts")

### Podcast Settings
- `host_name`: Podcast host (default: "Alex")
- `expert_name`: Podcast expert (default: "Sam")
- `target_duration_minutes`: Target duration (default: 5)
- `conversation_style`: professional, casual, educational

### TTS Settings
- `host_voice`: Voice for host (default: "Kore")
- `expert_voice`: Voice for expert (default: "Puck")

## Project Structure

```
├── src/agent/
│   ├── state.py           # State definitions (podcast-focused schemas)
│   ├── configuration.py   # Podcast creator configuration  
│   ├── utils.py          # Podcast generation utilities
│   └── graph.py          # Multi-agent workflow definition
├── langgraph.json        # LangGraph deployment configuration
├── pyproject.toml        # Python package configuration
├── test_podcast.py       # Test script
└── .env                  # Environment variables
```

## Testing

Run the test script to verify functionality:

```bash
python test_podcast.py
```

## Key Features

### Professional Quality
- Natural conversation flow between distinct speakers
- Smooth topic transitions and engaging dialogue
- Professional TTS with configurable voices

### Intelligent Content Synthesis  
- Combines web research with video analysis
- Extracts key insights for discussion
- Maintains focus on most engaging content

### Flexible Input Handling
- Works with topic only, video only, or both
- Validates inputs and provides clear error messages
- Adapts workflow based on available content

### Rich Metadata Generation
- Auto-generated engaging titles and descriptions
- Topic extraction for discoverability  
- Duration estimation and content categorization

## Deployment

- **Local Development**: LangGraph CLI with in-memory storage
- **Production**: LangGraph Platform or self-hosted containers
- **API Integration**: REST endpoints for external systems

## Dependencies

Core dependencies:
- `langgraph>=0.2.6` - Multi-agent workflow orchestration
- `google-genai` - Gemini API client with TTS support
- `langchain>=0.3.19` - LangChain integrations
- `langsmith` - Tracing and monitoring

Built with ❤️ using Gemini 2.5 Flash, LangGraph, and professional TTS generation.

## Quick Start

### Prerequisites

- Python 3.11+
- [uv](https://docs.astral.sh/uv/) package manager
- Google Gemini API key

### Setup

1. **Clone and navigate to the project**:
```bash
git clone https://github.com/langchain-ai/multi-modal-researcher
cd mutli-modal-researcher
```

2. **Set up environment variables**:
```bash
cp .env.example .env
```
Edit `.env` and [add your Google Gemini API key](https://ai.google.dev/gemini-api/docs/api-key):
```bash
GEMINI_API_KEY=your_api_key_here
```

3. **Run the development server**:

```bash
# Install uv package manager
curl -LsSf https://astral.sh/uv/install.sh | sh
# Install dependencies and start the LangGraph server
uvx --refresh --from "langgraph-cli[inmem]" --with-editable . --python 3.11 langgraph dev --allow-blocking
```

4. **Access the application**:

LangGraph will open in your browser.

```bash
╦  ┌─┐┌┐┌┌─┐╔═╗┬─┐┌─┐┌─┐┬ ┬
║  ├─┤││││ ┬║ ╦├┬┘├─┤├─┘├─┤
╩═╝┴ ┴┘└┘└─┘╚═╝┴└─┴ ┴┴  ┴ ┴

- 🚀 API: http://127.0.0.1:2024
- 🎨 Studio UI: https://smith.langchain.com/studio/?baseUrl=http://127.0.0.1:2024
- 📚 API Docs: http://127.0.0.1:2024/docs
```

5. Pass a `topic` and optionally a `video_url`.

Example:
* `topic`: Give me an overview of the idea that LLMs are like a new kind of operating system.
* `video_url`: https://youtu.be/LCEmiRjPEtQ?si=raeMN2Roy5pESNG2

<img width="1604" alt="Screenshot 2025-06-24 at 5 13 31 PM" src="https://github.com/user-attachments/assets/6407e802-8932-4cfb-bdf9-5af96050ee1f" />

Result:

[🔍 See the example report](./example/report/karpathy_os.md)

[▶️ Download the example podcast](./example/audio/karpathy_os.wav)

## Architecture

The system implements a LangGraph workflow with the following nodes:

1. **Search Research Node**: Performs web search using Gemini's Google Search integration
2. **Analyze Video Node**: Analyzes YouTube videos when provided (conditional)
3. **Create Report Node**: Synthesizes findings into a comprehensive markdown report
4. **Create Podcast Node**: Generates a 2-speaker podcast discussion with TTS audio

### Workflow

```
START → search_research → [analyze_video?] → create_report → create_podcast → END
```

The workflow conditionally includes video analysis if a YouTube URL is provided, otherwise proceeds directly to report generation.

### Output

The system generates:

- **Research Report**: Comprehensive markdown report with executive summary and sources
- **Podcast Script**: Natural dialogue between Dr. Sarah (expert) and Mike (interviewer)  
- **Audio File**: Multi-speaker TTS audio file (`research_podcast_*.wav`)

## Configuration

The system supports runtime configuration through the `Configuration` class:

### Model Settings
- `search_model`: Model for web search (default: "gemini-2.5-flash")
- `synthesis_model`: Model for report synthesis (default: "gemini-2.5-flash")
- `video_model`: Model for video analysis (default: "gemini-2.5-flash")
- `tts_model`: Model for text-to-speech (default: "gemini-2.5-flash-preview-tts")

### Temperature Settings
- `search_temperature`: Factual search queries (default: 0.0)
- `synthesis_temperature`: Balanced synthesis (default: 0.3)
- `podcast_script_temperature`: Creative dialogue (default: 0.4)

### TTS Settings
- `mike_voice`: Voice for interviewer (default: "Kore")
- `sarah_voice`: Voice for expert (default: "Puck")
- Audio format settings for output quality

## Project Structure

```
├── src/agent/
│   ├── state.py           # State definitions (input/output schemas)
│   ├── configuration.py   # Runtime configuration class
│   ├── utils.py          # Utility functions (TTS, report generation)
│   └── graph.py          # LangGraph workflow definition
├── langgraph.json        # LangGraph deployment configuration
├── pyproject.toml        # Python package configuration
└── .env                  # Environment variables
```

## Key Components

### State Management

- **ResearchStateInput**: Input schema (topic, optional video_url)
- **ResearchStateOutput**: Output schema (report, podcast_script, podcast_filename)
- **ResearchState**: Complete state including intermediate results

### Utility Functions

- **display_gemini_response()**: Processes Gemini responses with grounding metadata
- **create_podcast_discussion()**: Generates scripted dialogue and TTS audio
- **create_research_report()**: Synthesizes multi-modal research into reports
- **wave_file()**: Saves audio data to WAV format

## Deployment

The application is configured for deployment on:

- **Local Development**: Using LangGraph CLI with in-memory storage
- **LangGraph Platform**: Production deployment with persistent storage
- **Self-Hosted**: Using Docker containers

## Dependencies

Core dependencies managed via `pyproject.toml`:

- `langgraph>=0.2.6` - Workflow orchestration
- `google-genai` - Gemini API client
- `langchain>=0.3.19` - LangChain integrations
- `rich` - Enhanced terminal output
- `python-dotenv` - Environment management

## License

MIT License - see LICENSE file for details.
