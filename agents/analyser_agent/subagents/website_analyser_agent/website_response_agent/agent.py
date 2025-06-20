"""
Response Agent
"""

from google.adk.agents import LlmAgent
from pydantic import BaseModel, Field
from typing import List

class AgentOutput(BaseModel):
    """
    Output model for the Website analyser agent.
    Contains the results from the sub-agents.
    """
    conflicts: List[str] = Field(..., description="List of conflicts or issues found in the website content.")
    suggestions: List[str] = Field(..., description="List of suggestions to improve the website based on the analysis.")
    summary: str = Field(..., description="Summary of the website content.")
    score: int = Field(..., description="Overall score based on the analyses (0-100).")
    guidelines: List[str] = Field(..., description="Guidelines used for the analysis.")

# --- Constants ---
GEMINI_MODEL = "gemini-2.0-flash"

# Response Agent
website_response_agent = LlmAgent(
    name="WebsiteResponseAgent",
    model=GEMINI_MODEL,
    instruction="""
    You are the response agent for responding to the analysis of previous agents.
    """,
    description="This agent is always called after the sub-agents to format the output and provide a final response.",
    output_schema=AgentOutput,
    output_key="final_output",
)