"""
Instagram Agent

This agent is responsible for analyzing Instagram posts to ensure they adhere to specific guidelines.
"""

from google.adk.agents import SequentialAgent
from .insta_response_agent import insta_response_agent
from .insta_act_agent import insta_act_agent

# Instagram Agent
insta_analyser_agent = SequentialAgent(
    name="InstaPostAnalyserAgent",
    description=("""This is the Instagram Analysis Agent that coordinates the analysis of Instagram posts."""),
    sub_agents=[insta_act_agent, insta_response_agent],
)
