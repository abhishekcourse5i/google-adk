"""
Instagram Agent

This agent is responsible for analyzing Instagram posts to ensure they adhere to specific guidelines.
"""

from google.adk.tools.agent_tool import AgentTool
from google.adk.agents import LlmAgent
from .tools import get_insta_summary
from .prompt import INSTA_GUIDELINES
from .insta_response_agent import insta_response_agent

# --- Constants ---
GEMINI_MODEL = "gemini-2.0-flash"

# Instagram Agent
insta_analyser_agent = LlmAgent(
    name="InstaPostAnalyserAgent",
    model=GEMINI_MODEL,
    instruction=f"""You are an Instagram post analysis agent. Your job is to analyze Instagram posts and check whether they follow the provided guidelines.

    You will receive a path to the Instagram post. Based on the response by the tool, your task is to provide a summary of the post and transcribe the audio if available.
    
    You must use the following guidelines for the Instagram post: {INSTA_GUIDELINES}
    
    Also, provide a score out of 100 based if the post follows the guidelines.

    You must ALWAYS use the insta_response_agent to provide a final response.
    
    """,
    description="This agent analyzes Instagram post content to provide a summary, suggestions and score.",
    sub_agents=[insta_response_agent],
    tools=[get_insta_summary],
    output_key="agent_output",
)
