"""
Website Agent

This agent is responsible for analyzing websites to ensure they adhere to specific guidelines.
"""

from google.adk.tools.agent_tool import AgentTool
from google.adk.agents import LlmAgent
from .tools import get_website_data
from .prompt import WEBSITE_GUIDELINES

# --- Constants ---
GEMINI_MODEL = "gemini-2.0-flash"

# Instagram Agent
website_act_agent = LlmAgent(
    name="WebsiteAnalyserAgent",
    model=GEMINI_MODEL,
    instruction=f"""You are a website analysis agent. Your job is to analyze websites and check whether they follow the provided guidelines.

    You will receive a URL to the website. Based on the response by the tool, your task is to provide a summary of the website content, identify conflicts, provide suggestions for improvement and provide a score out of 100 based on if the website follows the guidelines.
    
    You must use the following guidelines for the Website: {WEBSITE_GUIDELINES}
    """,
    description="This agent analyzes Website content to provide conflicts, summary, suggestions, and score.",
    tools=[get_website_data],
    output_key="agent_output",
)
