"""
Task Manager for the Analyser Agent (pre MLR version).
This module handles task processing for the Analyser Agent in A2A mode.
"""

import os
import logging
import tempfile
import uuid
from typing import Dict, Any, Optional

from google.adk.agents import Agent
from google.adk.runners import Runner
from google.adk.sessions import InMemorySessionService
from google.adk.artifacts.in_memory_artifact_service import InMemoryArtifactService
from google.genai import types as adk_types

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Define app name for the runner
A2A_APP_NAME = "pre_mlr_app"

class TaskManager:
    """Task Manager for the Analyser Agent in A2A mode (pre MLR implementation)."""
    
    def __init__(self, agent: Agent):
        """Initialize with an Agent instance and set up ADK Runner."""
        logger.info(f"Initializing TaskManager for agent: {agent.name}")
        self.agent = agent

    @classmethod
    async def create(cls, agent):
        """
        Async factory method to create and configure a TaskManager instance.

        Args:
            agent: The agent instance to manage.

        Returns:
            TaskManager: Configured instance.
        """
        self = cls(agent)
        await self.initialize_runner()

        return self

    async def initialize_runner(self):
        """Initialize the ADK Runner with the agent and services."""
        
        # Initialize ADK services
        self.session_service = InMemorySessionService()
        self.artifact_service = InMemoryArtifactService()
        
        # Create the runner
        self.runner = Runner(
            agent=self.agent,
            app_name=A2A_APP_NAME,
            session_service=self.session_service,
            artifact_service=self.artifact_service
        )
        logger.info(f"ADK Runner initialized for app '{self.runner.app_name}'")

    async def process_task(self, message: str, context: Dict[str, Any], session_id: Optional[str] = None) -> Dict[str, Any]:
        """
        Process an A2A task request by running the agent.
        
        Args:
            message: The text message to process.
            context: Additional context data.
            session_id: Session identifier (generated if None).
            
        Returns:
            Response dict with message, status, and data.
        """
        # Get user_id from context or use default
        user_id = context.get("user_id", "default_a2a_user")
        
        # Create or get session
        if not session_id:
            session_id = str(uuid.uuid4())
            logger.info(f"Generated new session_id: {session_id}")
            
        session = await self.session_service.get_session(app_name=A2A_APP_NAME, user_id=user_id, session_id=session_id)
        if not session:
            session = await self.session_service.create_session(app_name=A2A_APP_NAME, user_id=user_id, session_id=session_id, state={})
            logger.info(f"Created new session: {session_id}")
        
        # Create user message
        request_content = adk_types.Content(role="user", parts=[adk_types.Part(text=message)])
        
        try:
            # Run the agent
            events_async = self.runner.run_async(
                user_id=user_id, 
                session_id=session_id, 
                new_message=request_content
            )
            
            # Process response
            final_message = "(No response generated)"
            raw_events = []

            # Process events
            async for event in events_async:
                raw_events.append(event.model_dump(exclude_none=True))
                
                # Only extract from the final response
                if event.is_final_response() and event.content and event.content.role == "model":
                    if event.content.parts and event.content.parts[0].text:
                        final_message = event.content.parts[0].text
                        logger.info(f"Final response: {final_message}")
                        
            # Return formatted response
            return {
                "message": final_message, 
                "status": "success",
                "data": {
                    "raw_events": raw_events[-3:]
                }
            }

        except Exception as e:
            logger.error(f"Error running agent: {str(e)}")
            return {
                "message": f"Error processing your request: {str(e)}",
                "status": "error",
                "data": {"error_type": type(e).__name__}
            }
