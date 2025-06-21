"""
Video Act Agent

This agent is responsible for analyzing video ads to ensure they adhere to specific guidelines.
"""

from google.adk.tools.agent_tool import AgentTool
from google.adk.agents import LlmAgent
from .tools import get_video_summary

# --- Constants ---
GEMINI_MODEL = "gemini-2.0-flash"

# Video Act Agent
video_act_agent = LlmAgent(
    name="VideoActAgent",
    model=GEMINI_MODEL,
    instruction=f"""You are a video analysis agent. Your job is to analyse video ads and check whether they follow the provided guidelines.

    You will receive a path to the video. Based on the response by the tool, your task is to provide a summary of the Video Ad, identify conflicts, provide suggestions for improvement and provide a score out of 100 based on if the Video Ad follows the guidelines.

    You must ALWAYS use the get_video_summary tool to provide a final response.
    
    The prompt for the tool is as follows:
        You are a video analysis tool. Your job is to analyze the video content and provide a summary, conflicts, suggestions for improvement, and a score out of 100 based on the provided guidelines.
    """,
    description="This agent analyzes video content to provide conflicts, summary, suggestions, and score using Google Gemini.",
    tools=[get_video_summary],
    output_key="agent_output",
)
