"""
Response Agent
"""

from google.adk.agents import LlmAgent
from pydantic import BaseModel, Field

class AgentOutput(BaseModel):
    """
    Output model for the Ad video Analysis agent.
    Contains the results from the sub-agents.
    """
    video_analysis: str = Field(..., description="Analysis of the video ad content.")
    video_suggestions: str = Field(..., description="Suggestions to improve the video ad and Instagram post based on the analyses.")
    video_summary: str = Field(..., description="Summary of the video ad content.")
    score: int = Field(..., description="Overall score based on the analyses (0-100).")

# --- Constants ---
GEMINI_MODEL = "gemini-2.0-flash"

# Response Agent
video_response_agent = LlmAgent(
    name="VideoResponseAgent",
    model=GEMINI_MODEL,
    instruction="""
    You are the response agent for responding to the analysis of previous agents.
    """,
    description="This agent is always called after the sub-agents to format the output and provide a final response.",
    output_schema=AgentOutput,
    output_key="final_output",
)