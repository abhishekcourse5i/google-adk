"""
Standardized Agent to Agent (A2A) server implementation following Google ADK standards (pre MLR version).
This module provides a FastAPI server implementation for agent-to-agent communication.
"""

import os
import json
import inspect
import logging
from typing import Dict, Any, Callable, Optional, List

from fastapi import FastAPI, Body, HTTPException, Request, File, UploadFile, Form
from fastapi.responses import JSONResponse
from pydantic import BaseModel, Field

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class AgentRequest(BaseModel):
    """Standard A2A agent request format."""
    message: str = Field(..., description="The message to process")
    context: Dict[str, Any] = Field(default_factory=dict, description="Additional context for the request")
    session_id: Optional[str] = Field(None, description="Session identifier for stateful interactions")

class AgentResponse(BaseModel):
    """Standard A2A agent response format."""
    message: str = Field(..., description="The response message")
    status: str = Field(default="success", description="Status of the response (success, error)")
    data: Dict[str, Any] = Field(default_factory=dict, description="Additional data returned by the agent")
    session_id: Optional[str] = Field(None, description="Session identifier for stateful interactions")

def create_agent_server(
    name: str, 
    description: str, 
    task_manager: Any, 
) -> FastAPI:
    """
    Create a FastAPI server for an agent following A2A protocol.
    
    Args:
        name: The name of the agent
        description: A description of the agent's functionality
        task_manager: The TaskManager instance for handling tasks
        endpoints: Optional dictionary of additional endpoints to register
        well_known_path: Optional path to the .well-known directory
        
    Returns:
        A configured FastAPI application
    """
    app = FastAPI(title=f"{name} Agent", description=description)

    # Standard A2A run endpoint
    @app.post("/run", response_model=AgentResponse)
    async def run(request: AgentRequest = Body(...)):
        """Standard A2A run endpoint for processing agent requests."""
        try:
            result = await task_manager.process_task(request.message, request.context, request.session_id)

            return AgentResponse(
                message=result.get("message", "Task completed"),
                status="success",
                data=result.get("data", {}),
                session_id=request.session_id
            )
        except Exception as e:
            return AgentResponse(
                message=f"Error processing request: {str(e)}",
                status="error",
                data={"error_type": type(e).__name__},
                session_id=request.session_id
            )
        
    return app