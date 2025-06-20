"""
Video Agent

This agent is responsible for analysing videos.
"""

from google.adk.agents import SequentialAgent
from .video_response_agent import video_response_agent
from .video_act_agent import video_act_agent

# Video Agent
ad_video_analyser_agent = SequentialAgent(
    name="VideoAnalyserAgent",
    description=("""This is the root agent that coordinates the analysis of video ads."""),
    sub_agents=[video_act_agent, video_response_agent],
)
