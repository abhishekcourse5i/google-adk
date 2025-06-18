import asyncio, os
from google.adk.agents import Agent
from dotenv import load_dotenv
from .subagents.ad_video_analyser_agent import ad_video_analyser_agent
from .subagents.instapost_analyser_agent import insta_analyser_agent
from .subagents.website_analyser_agent import website_analyser_agent

# --- Constants ---
GEMINI_MODEL = "gemini-2.0-flash"

# Load environment variables from the project root .env file
load_dotenv(dotenv_path=os.path.join(os.path.dirname(__file__), '..', '..', '.env'))

# --- Agent Creation ---

# For Uvicorn compatibility, we need to define the agent creation function

async def create_agent():
        
    agent_instance = Agent(
        name="manager_agent",
        model=GEMINI_MODEL,
        description="Manager Agent for handling various tasks related to video and Instagram post analysis.",
        instruction="""
        You are the manager agent responsible for coordinating the analysis of video ads and Instagram posts.
        Your task is to manage the sub-agents that analyze video ads and Instagram posts, and to format the output from these analyses.
        IMPORTANT: You MUST use the response agent to format the output from the sub-agents.""",
        sub_agents=[ad_video_analyser_agent, insta_analyser_agent, website_analyser_agent],
        output_key="agent_output",
    )

    return agent_instance

root_agent = create_agent()

# For google adk compatibility, we need to define the agent directly

# root_agent = Agent(
#         name="analyser_agent",
#         model=GEMINI_MODEL,
#         description="Manager Agent for handling various tasks related to Ad videos, Instagram post and Website analysis.",
#         instruction="""
#         You are the manager agent.
#         Your task is to manage the sub-agents that analyze video ads, Instagram posts and Websites, and to format the output from these analyses""",
#         sub_agents=[ad_video_analyser_agent, insta_analyser_agent, website_analyser_agent],
#         output_key="agent_output",
#     )