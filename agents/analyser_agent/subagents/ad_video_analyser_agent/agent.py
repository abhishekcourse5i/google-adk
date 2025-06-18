"""
Video Agent

This agent is responsible for analysing videos.
"""

from google.adk.agents import LlmAgent
from .tools import get_video_summary
from .prompt import VIDEO_GUIDELINES
from .video_response_agent import video_response_agent

# --- Constants ---
GEMINI_MODEL = "gemini-2.0-flash"

# Video Agent
ad_video_analyser_agent = LlmAgent(
    name="VideoAnalyserAgent",
    model=GEMINI_MODEL,
    instruction=f"""You are a video analysis agent. Your job is to analyse video ads and check whether they follow the provided guidelines.

    You will receive a path to the video. Based on the response by the tool, your task is to provide suggestions to improve the video ad.
    
    You must use the following guidelines for the video ad: {VIDEO_GUIDELINES}

    Also, provide a score out of 100 based if the post follows the guidelines.

    You must ALWAYS use the insta_response_agent to provide a final response.
    
    """,
    description="This agent analyzes video content to provide suggestions and score using Google Gemini.",
    sub_agents=[video_response_agent],
    tools=[get_video_summary],
    output_key="agent_output",
)
