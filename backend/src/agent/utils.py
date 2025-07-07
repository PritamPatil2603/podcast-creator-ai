import os
import wave
import json
from typing import List, Tuple
from google.genai import Client, types
from rich.console import Console
from rich.markdown import Markdown
from dotenv import load_dotenv

load_dotenv()

# Initialize client
genai_client = Client(api_key=os.getenv("GEMINI_API_KEY"))


def display_gemini_response(response):
    """Extract text from Gemini response and display as markdown with references"""
    console = Console()
    
    # Extract main content
    text = response.candidates[0].content.parts[0].text
    md = Markdown(text)
    console.print(md)
    
    # Get candidate for grounding metadata
    candidate = response.candidates[0]
    
    # Build sources text block
    sources_text = ""
    
    # Display grounding metadata if available
    if hasattr(candidate, 'grounding_metadata') and candidate.grounding_metadata:
        console.print("\n" + "="*50)
        console.print("[bold blue]References & Sources[/bold blue]")
        console.print("="*50)
        
        # Display and collect source URLs
        if candidate.grounding_metadata.grounding_chunks:
            console.print(f"\n[bold]Sources ({len(candidate.grounding_metadata.grounding_chunks)}):[/bold]")
            sources_list = []
            for i, chunk in enumerate(candidate.grounding_metadata.grounding_chunks, 1):
                if hasattr(chunk, 'web') and chunk.web:
                    title = getattr(chunk.web, 'title', 'No title') or "No title"
                    uri = getattr(chunk.web, 'uri', 'No URI') or "No URI"
                    console.print(f"{i}. {title}")
                    console.print(f"   [dim]{uri}[/dim]")
                    sources_list.append(f"{i}. {title}\n   {uri}")
            
            sources_text = "\n".join(sources_list)
        
        # Display grounding supports (which text is backed by which sources)
        if candidate.grounding_metadata.grounding_supports:
            console.print(f"\n[bold]Text segments with source backing:[/bold]")
            for support in candidate.grounding_metadata.grounding_supports[:5]:  # Show first 5
                if hasattr(support, 'segment') and support.segment:
                    snippet = support.segment.text[:100] + "..." if len(support.segment.text) > 100 else support.segment.text
                    source_nums = [str(i+1) for i in support.grounding_chunk_indices]
                    console.print(f"• \"{snippet}\" [dim](sources: {', '.join(source_nums)})[/dim]")
    
    return text, sources_text


def wave_file(filename, pcm, channels=1, rate=24000, sample_width=2):
    """Save PCM data to a wave file"""
    with wave.open(filename, "wb") as wf:
        wf.setnchannels(channels)
        wf.setsampwidth(sample_width)
        wf.setframerate(rate)
        wf.writeframes(pcm)


def synthesize_content(topic: str, search_text: str, video_text: str, configuration) -> Tuple[str, List[str]]:
    """Synthesize all content sources into a comprehensive summary and key insights"""
    
    synthesis_prompt = f"""
    You are a content synthesizer for podcast creation. Analyze all the provided content about "{topic}" and create:
    
    1. A comprehensive content summary (2-3 paragraphs)
    2. A list of 5-7 key insights that would make for engaging podcast discussion
    
    RESEARCH CONTENT:
    {search_text}
    
    VIDEO CONTENT:
    {video_text}
    
    Focus on:
    - Most interesting and discussion-worthy points
    - Practical insights and takeaways
    - Surprising or counterintuitive information
    - Different perspectives or debates
    - Real-world applications
    
    Format your response as JSON:
    {{
        "content_summary": "comprehensive summary...",
        "key_insights": ["insight 1", "insight 2", "insight 3", ...]
    }}
    """
    
    response = genai_client.models.generate_content(
        model=configuration.synthesis_model,
        contents=synthesis_prompt,
        config={"temperature": configuration.synthesis_temperature}
    )
    
    try:
        result = json.loads(response.candidates[0].content.parts[0].text)
        return result["content_summary"], result["key_insights"]
    except:
        # Fallback if JSON parsing fails
        text = response.candidates[0].content.parts[0].text
        return text, ["Key insight from content analysis"]


def create_podcast_metadata(topic: str, content_summary: str, key_insights: List[str], configuration) -> Tuple[str, str, List[str]]:
    """Generate podcast title, description, and topic list"""
    
    metadata_prompt = f"""
    Create engaging podcast metadata for a {configuration.target_duration_minutes}-minute episode about "{topic}".
    
    CONTENT SUMMARY:
    {content_summary}
    
    KEY INSIGHTS:
    {', '.join(key_insights)}
    
    Generate:
    1. Catchy, professional podcast title (60 characters max)
    2. Engaging description (150-200 words) that would make people want to listen
    3. List of 3-5 main topics covered
    
    Format as JSON:
    {{
        "title": "Engaging Podcast Title",
        "description": "Professional description that hooks the listener...",
        "topics_covered": ["topic 1", "topic 2", "topic 3"]
    }}
    """
    
    response = genai_client.models.generate_content(
        model=configuration.synthesis_model,
        contents=metadata_prompt,
        config={"temperature": configuration.metadata_temperature}
    )
    
    try:
        result = json.loads(response.candidates[0].content.parts[0].text)
        return result["title"], result["description"], result["topics_covered"]
    except:
        # Fallback
        return f"Podcast: {topic}", f"An insightful discussion about {topic}", [topic]


def create_professional_podcast(topic: str, content_summary: str, key_insights: List[str], 
                               duration_minutes: int, filename: str, configuration) -> Tuple[str, str, str]:
    """Create a professional podcast conversation and generate TTS audio"""
    
    # Step 1: Generate professional script
    script_prompt = f"""
    Create a natural, engaging {duration_minutes}-minute podcast conversation between {configuration.host_name} (curious host) and {configuration.expert_name} (knowledgeable expert) about "{topic}".
    
    CONTENT TO COVER:
    {content_summary}
    
    KEY INSIGHTS TO DISCUSS:
    {', '.join(key_insights)}
    
    CONVERSATION STYLE: {configuration.conversation_style}
    
    Structure (aim for ~{duration_minutes * 200} words total):
    1. {configuration.host_name} introduces the topic and {configuration.expert_name} (30 seconds)
    2. Main discussion covering key insights (3-4 minutes)
    3. Practical takeaways and wrap-up (30-60 seconds)
    
    Guidelines:
    - Make it conversational and natural
    - {configuration.host_name} asks thoughtful questions
    - {configuration.expert_name} provides clear, insightful answers
    - Include smooth transitions between topics
    - End with a memorable takeaway
    
    Format exactly like this:
    {configuration.host_name}: [opening introduction]
    {configuration.expert_name}: [expert response]
    {configuration.host_name}: [follow-up question]
    {configuration.expert_name}: [detailed explanation]
    [continue natural conversation...]
    """
    
    script_response = genai_client.models.generate_content(
        model=configuration.synthesis_model,
        contents=script_prompt,
        config={"temperature": configuration.script_temperature}
    )
    
    podcast_script = script_response.candidates[0].content.parts[0].text
    
    # Step 2: Generate TTS audio
    tts_prompt = f"""Create a professional podcast conversation between {configuration.host_name} and {configuration.expert_name}:

{podcast_script}"""
    
    response = genai_client.models.generate_content(
        model=configuration.tts_model,
        contents=tts_prompt,
        config=types.GenerateContentConfig(
            response_modalities=["AUDIO"],
            speech_config=types.SpeechConfig(
                multi_speaker_voice_config=types.MultiSpeakerVoiceConfig(
                    speaker_voice_configs=[
                        types.SpeakerVoiceConfig(
                            speaker=configuration.host_name,
                            voice_config=types.VoiceConfig(
                                prebuilt_voice_config=types.PrebuiltVoiceConfig(
                                    voice_name=configuration.host_voice,
                                )
                            )
                        ),
                        types.SpeakerVoiceConfig(
                            speaker=configuration.expert_name,
                            voice_config=types.VoiceConfig(
                                prebuilt_voice_config=types.PrebuiltVoiceConfig(
                                    voice_name=configuration.expert_voice,
                                )
                            )
                        ),
                    ]
                )
            )
        )
    )
    
    # Step 3: Save audio file
    audio_data = response.candidates[0].content.parts[0].inline_data.data
    audio_dir = "generated_podcasts"
    os.makedirs(audio_dir, exist_ok=True)
    full_path = os.path.join(audio_dir, filename)
    wave_file(full_path, audio_data, configuration.tts_channels, configuration.tts_rate, configuration.tts_sample_width)
    
    # Estimate duration (rough calculation)
    word_count = len(podcast_script.split())
    estimated_duration = f"{word_count // 200} min {(word_count % 200) // 3} sec"
    
    print(f"Professional podcast saved as: {full_path}")
    return podcast_script, full_path, estimated_duration


# Keep the existing create_podcast_discussion function for backwards compatibility
def create_podcast_discussion(topic, search_text, video_text, search_sources_text, video_url, filename="research_podcast.wav", configuration=None):
    """Backwards compatibility wrapper"""
    if configuration is None:
        from agent.configuration import Configuration
        configuration = Configuration()
    
    # Use new professional podcast function
    return create_professional_podcast(
        topic, search_text, [video_text], 5, filename, configuration
    )


def create_research_report(topic, search_text, video_text, search_sources_text, video_url, configuration=None):
    """Create a comprehensive research report by synthesizing search and video content"""
    
    # Use default values if no configuration provided
    if configuration is None:
        from agent.configuration import Configuration
        configuration = Configuration()
    
    # Step 1: Create synthesis using Gemini
    synthesis_prompt = f"""
    You are a research analyst. I have gathered information about "{topic}" from two sources:
    
    SEARCH RESULTS:
    {search_text}
    
    VIDEO CONTENT:
    {video_text}
    
    Please create a comprehensive synthesis that:
    1. Identifies key themes and insights from both sources
    2. Highlights any complementary or contrasting perspectives
    3. Provides an overall analysis of the topic based on this multi-modal research
    4. Keep it concise but thorough (3-4 paragraphs)
    
    Focus on creating a coherent narrative that brings together the best insights from both sources.
    """
    
    synthesis_response = genai_client.models.generate_content(
        model=configuration.synthesis_model,
        contents=synthesis_prompt,
        config={
            "temperature": configuration.synthesis_temperature,
        }
    )
    
    synthesis_text = synthesis_response.candidates[0].content.parts[0].text
    
    # Step 2: Create markdown report
    report = f"""# Research Report: {topic}

## Executive Summary

{synthesis_text}

## Video Source
- **URL**: {video_url}

## Additional Sources
{search_sources_text}

---
*Report generated using multi-modal AI research combining web search and video analysis*
"""
    
    return report, synthesis_text