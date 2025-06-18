"""
Response Agent
"""

from google.adk.agents import LlmAgent
from pydantic import BaseModel, Field

class AgentOutput(BaseModel):
    """
    Output model for the Insta post analyser agent.
    Contains the results from the sub-agents.
    """
    insta_analysis: str = Field(..., description="Analysis of the Instagram post content.")
    insta_suggestions: str = Field(..., description="Suggestions to improve the Instagram post based on the analysis.")
    insta_summary: str = Field(..., description="Summary of the Instagram post content.")
    score: int = Field(..., description="Overall score based on the analyses (0-100).")

# --- Constants ---
GEMINI_MODEL = "gemini-2.0-flash"

# Response Agent
insta_response_agent = LlmAgent(
    name="InstaResponseAgent",
    model=GEMINI_MODEL,
    instruction="""
    You are the response agent for responding to the analysis of previous agents.
    """,
    description="This agent is always called after the sub-agents to format the output and provide a final response.",
    output_schema=AgentOutput,
    output_key="final_output",
)