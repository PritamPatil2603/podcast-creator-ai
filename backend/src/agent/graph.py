"""LangGraph implementation of the podcast creator workflow"""

from langgraph.graph import StateGraph, START, END
from langchain_core.runnables import RunnableConfig
from google.genai import types

from agent.state import PodcastState, PodcastStateInput, PodcastStateOutput
from agent.utils import (
    display_gemini_response, 
    create_professional_podcast, 
    create_podcast_metadata,
    synthesize_content,
    genai_client
)
from agent.configuration import Configuration
from langsmith import traceable

@traceable(run_type="llm", name="Research Agent", project_name="podcast-creator")
def research_agent_node(state: PodcastState, config: RunnableConfig) -> dict:
    """Research Agent - Web search and topic analysis"""
    configuration = Configuration.from_runnable_config(config)
    topic = state.get("topic")
    
    if not topic:
        return {
            "search_text": "No research topic provided.",
            "search_sources_text": ""
        }
    
    # Enhanced research prompt for podcast content
    research_prompt = f"""
    Research this topic for creating an engaging podcast conversation: {topic}
    
    Focus on:
    1. Key concepts and definitions
    2. Current trends and developments  
    3. Interesting facts and insights
    4. Practical implications
    5. Different perspectives or debates
    6. Real-world examples or case studies
    
    Provide comprehensive information suitable for a 5-minute podcast discussion.
    """
    
    search_response = genai_client.models.generate_content(
        model=configuration.search_model,
        contents=research_prompt,
        config={
            "tools": [{"google_search": {}}],
            "temperature": configuration.search_temperature,
        },
    )
    
    search_text, search_sources_text = display_gemini_response(search_response)
    
    return {
        "search_text": search_text,
        "search_sources_text": search_sources_text
    }


@traceable(run_type="llm", name="Video Analysis Agent", project_name="podcast-creator")
def video_analysis_agent_node(state: PodcastState, config: RunnableConfig) -> dict:
    """Video Analysis Agent - YouTube content extraction"""
    configuration = Configuration.from_runnable_config(config)
    video_url = state.get("video_url")
    topic = state.get("topic", "this video content")
    
    if not video_url:
        return {"video_text": "No video provided for analysis."}
    
    # Enhanced video analysis prompt for podcast content
    video_prompt = f"""
    Analyze this video for creating a podcast conversation about: {topic}
    
    Extract and focus on:
    1. Main themes and key messages
    2. Important insights or revelations
    3. Interesting quotes or statements
    4. Visual elements worth describing
    5. Context and background information
    6. Actionable takeaways
    7. Discussion-worthy points
    
    Structure your analysis to be suitable for a 5-minute podcast conversation.
    """
    
    video_response = genai_client.models.generate_content(
        model=configuration.video_model,
        contents=types.Content(
            parts=[
                types.Part(
                    file_data=types.FileData(file_uri=video_url)
                ),
                types.Part(text=video_prompt)
            ]
        )
    )
    
    video_text, _ = display_gemini_response(video_response)
    
    return {"video_text": video_text}


@traceable(run_type="llm", name="Content Synthesizer", project_name="podcast-creator")
def content_synthesis_node(state: PodcastState, config: RunnableConfig) -> dict:
    """Synthesize all content sources into key insights"""
    configuration = Configuration.from_runnable_config(config)
    
    topic = state.get("topic", "the provided content")
    search_text = state.get("search_text", "")
    video_text = state.get("video_text", "")
    
    content_summary, key_insights = synthesize_content(
        topic, search_text, video_text, configuration
    )
    
    return {
        "content_summary": content_summary,
        "key_insights": key_insights
    }


@traceable(run_type="llm", name="Metadata Generator", project_name="podcast-creator") 
def metadata_generator_node(state: PodcastState, config: RunnableConfig) -> dict:
    """Generate podcast title, description, and topics"""
    configuration = Configuration.from_runnable_config(config)
    
    topic = state.get("topic", "")
    content_summary = state.get("content_summary", "")
    key_insights = state.get("key_insights", [])
    
    podcast_title, podcast_description, topics_covered = create_podcast_metadata(
        topic, content_summary, key_insights, configuration
    )
    
    return {
        "podcast_title": podcast_title,
        "podcast_description": podcast_description,
        "topics_covered": topics_covered
    }


@traceable(run_type="llm", name="Script Writer & Audio Producer", project_name="podcast-creator")
def script_and_audio_node(state: PodcastState, config: RunnableConfig) -> dict:
    """Script Writer + Audio Production - Generate conversation and TTS"""
    configuration = Configuration.from_runnable_config(config)
    
    topic = state.get("topic", "the content")
    content_summary = state.get("content_summary", "")
    key_insights = state.get("key_insights", [])
    podcast_title = state.get("podcast_title", "Podcast Episode")
    duration_minutes = state.get("duration_minutes", configuration.target_duration_minutes)
    
    # Create unique filename based on title
    safe_title = "".join(c for c in podcast_title if c.isalnum() or c in (' ', '-', '_')).rstrip()
    filename = f"podcast_{safe_title.replace(' ', '_')}.wav"
    
    podcast_script, podcast_filename, duration_estimate = create_professional_podcast(
        topic, content_summary, key_insights, duration_minutes, filename, configuration
    )
    
    return {
        "podcast_script": podcast_script,
        "podcast_audio_filename": podcast_filename,
        "duration_estimate": duration_estimate
    }


def should_do_research(state: PodcastState) -> str:
    """Conditional edge to determine if research should be performed"""
    if state.get("topic"):
        return "research_agent"
    else:
        return "video_analysis_agent"


def should_do_video_analysis(state: PodcastState) -> str:
    """Conditional edge after research to determine if video analysis needed"""
    if state.get("video_url"):
        return "video_analysis_agent"
    else:
        return "content_synthesis"


def validate_inputs(state: PodcastState) -> str:
    """Validate that at least one input is provided"""
    topic = state.get("topic")
    video_url = state.get("video_url")
    
    if not topic and not video_url:
        raise ValueError("At least one of 'topic' or 'video_url' must be provided")
    
    return should_do_research(state)


def create_podcast_graph() -> StateGraph:
    """Create and return the podcast creator workflow graph"""
    
    graph = StateGraph(
        PodcastState, 
        input=PodcastStateInput, 
        output=PodcastStateOutput,
        config_schema=Configuration
    )
    
    # Add nodes
    graph.add_node("research_agent", research_agent_node)
    graph.add_node("video_analysis_agent", video_analysis_agent_node)
    graph.add_node("content_synthesis", content_synthesis_node)
    graph.add_node("metadata_generator", metadata_generator_node)
    graph.add_node("script_and_audio", script_and_audio_node)
    
    # Add edges with validation
    graph.add_conditional_edges(
        START,
        validate_inputs,
        {
            "research_agent": "research_agent",
            "video_analysis_agent": "video_analysis_agent"
        }
    )
    
    graph.add_conditional_edges(
        "research_agent",
        should_do_video_analysis,
        {
            "video_analysis_agent": "video_analysis_agent",
            "content_synthesis": "content_synthesis"
        }
    )
    
    graph.add_edge("video_analysis_agent", "content_synthesis")
    graph.add_edge("content_synthesis", "metadata_generator")
    graph.add_edge("metadata_generator", "script_and_audio")
    graph.add_edge("script_and_audio", END)
    
    return graph


def create_compiled_graph():
    """Create and compile the podcast creator graph"""
    graph = create_podcast_graph()
    return graph.compile()