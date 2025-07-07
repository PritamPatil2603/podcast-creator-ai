from typing_extensions import TypedDict
from typing import Optional

class PodcastStateInput(TypedDict):
    """Input state for the podcast creator workflow"""
    # Both inputs are optional - at least one must be provided
    topic: Optional[str]
    video_url: Optional[str]
    # Optional customization
    duration_minutes: Optional[int]  # Target duration (default: 5)

class PodcastStateOutput(TypedDict):
    """Output state for the podcast creator workflow"""
    # Final outputs
    podcast_title: str
    podcast_description: str
    podcast_script: str
    podcast_audio_filename: str
    # Metadata
    duration_estimate: str
    topics_covered: list[str]

class PodcastState(TypedDict):
    """Complete state for the podcast creator workflow"""
    # Input fields
    topic: Optional[str]
    video_url: Optional[str]
    duration_minutes: Optional[int]
    
    # Intermediate results
    search_text: Optional[str]
    search_sources_text: Optional[str]
    video_text: Optional[str]
    
    # Content synthesis
    content_summary: Optional[str]
    key_insights: Optional[list[str]]
    
    # Final outputs
    podcast_title: str
    podcast_description: str
    podcast_script: str
    podcast_audio_filename: str
    duration_estimate: str
    topics_covered: list[str]

# Backwards compatibility aliases
ResearchStateInput = PodcastStateInput
ResearchStateOutput = PodcastStateOutput  
ResearchState = PodcastState