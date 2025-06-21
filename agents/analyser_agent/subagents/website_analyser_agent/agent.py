"""
Website Agent

This agent is responsible for analyzing websites to ensure they adhere to specific guidelines.
"""

from google.adk.agents import SequentialAgent
from .website_response_agent import website_response_agent
from .website_act_agent import website_act_agent

# Instagram Agent
website_analyser_agent = SequentialAgent(
    name="WebsiteAnalyserAgent",
    description=("""This is the Website Analysis Agent that coordinates the analysis of websites."""),
    sub_agents=[website_act_agent, website_response_agent],
)
