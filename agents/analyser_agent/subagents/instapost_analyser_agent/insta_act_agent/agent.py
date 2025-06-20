"""
Instagram Act Agent

This agent is responsible for analyzing Instagram posts to ensure they adhere to specific guidelines.
"""

from google.adk.tools.agent_tool import AgentTool
from google.adk.agents import LlmAgent
from .tools import get_insta_summary

# --- Constants ---
GEMINI_MODEL = "gemini-2.0-flash"

# Instagram Act Agent
insta_act_agent = LlmAgent(
    name="InstaActAgent",
    model=GEMINI_MODEL,
    instruction=f"""You are an Instagram post analysis agent. Your job is to analyze Instagram posts and check whether they follow the provided guidelines.

    You will receive a path to the Instagram post. Based on the response by the tool, your task is to provide a summary of the post and transcribe the audio if available.
        
    Also, provide a score out of 100 based on how well the post follows the guidelines.
    """,
    description="This agent analyzes Instagram post content to provide a summary, suggestions and score.",
    tools=[get_insta_summary],
    output_key="agent_output",
)
