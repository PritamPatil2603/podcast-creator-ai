@"
# 🎙️ Professional Podcast Creator AI

Transform YouTube videos and research topics into engaging podcast conversations using AI.

## Architecture

- **Backend**: LangGraph + Gemini 2.5 (Multi-agent system)
- **Frontend**: Next.js + React (Coming soon)

## Quick Start

### Backend Development
\`\`\`bash
cd backend
# Set environment variable
\$env:GEMINI_API_KEY="your_key"
# Run development server
uvx --refresh --from "langgraph-cli[inmem]" --with-editable . --python 3.11 langgraph dev --allow-blocking
\`\`\`

### Production URLs
- **Backend API**: https://your-deployment.langchain.app
- **Frontend**: Coming soon

## Features

🎥 **YouTube Analysis** - Extract insights from any video
🔍 **Research Topics** - Generate content from any topic  
🎙️ **Professional TTS** - Multi-speaker conversations (Alex & Sam)
📋 **Smart Metadata** - Auto-generated titles and descriptions
⏱️ **Flexible Duration** - 4-6 minute professional podcasts

Built with Gemini 2.5, LangGraph, and professional audio generation.
"@ | Out-File -FilePath README.md -Encoding utf8