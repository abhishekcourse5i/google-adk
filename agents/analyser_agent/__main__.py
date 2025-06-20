"""
Entry point for the Analyser Agent (pre MLR version).
Initializes and starts the agent's A2A server with API endpoints.
"""

import os
import sys
import logging
import argparse
import uvicorn
import asyncio
from contextlib import AsyncExitStack
from dotenv import load_dotenv
from fastapi import FastAPI, HTTPException, Request
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel

# Use relative imports within the agent package
from .task_manager import TaskManager
from .agent import root_agent
from .api import create_api_router
from common.a2a_server import AgentRequest, AgentResponse, create_agent_server

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    handlers=[logging.StreamHandler()],
)
logger = logging.getLogger(__name__)

# Load environment variables
dotenv_path = os.path.join(os.path.dirname(__file__), '..', '..', '.env')
load_status = load_dotenv(dotenv_path=dotenv_path, override=True)

async def main():
    """Initialize and start the Analyser Agent server (pre MLR implementation)."""

    logger.info("Starting Analyser Agent A2A Server initialization...")
    
    # Await the root_agent coroutine to get the actual agent and exit_stack
    logger.info("Awaiting root_agent creation...")
    agent_instance = await root_agent
    logger.info(f"Agent instance created: {agent_instance.name}")

    # Initialize the TaskManager with the resolved agent instance
    task_manager_instance = await TaskManager.create(agent=agent_instance)
    logger.info("TaskManager initialized with agent instance.")

    # Configuration for the A2A server
    host = os.getenv("ANALYSER_A2A_HOST", "127.0.0.1")
    port = int(os.getenv("ANALYSER_A2A_PORT", 8003))
    
    # Create the FastAPI app
    app = create_agent_server(
        name=agent_instance.name,
        description=agent_instance.description,
        task_manager=task_manager_instance 
    )
    
    # Add API router
    api_router = create_api_router(task_manager_instance)
    app.include_router(api_router)
    
    # Add CORS middleware
    app.add_middleware(
        CORSMiddleware,
        allow_origins=["*"],  # Allows all origins
        allow_credentials=True,
        allow_methods=["*"],  # Allows all methods
        allow_headers=["*"],  # Allows all headers
    )
    
    logger.info(f"Analyser Agent A2A server with API endpoints starting on {host}:{port}")
    
    # Configure uvicorn
    config = uvicorn.Config(app, host=host, port=port, log_level="info")
    server = uvicorn.Server(config)
    
    # Run the server
    await server.serve()
    
    # This part will be reached after the server is stopped (e.g., Ctrl+C)
    logger.info("Analyser Agent A2A server stopped.")

if __name__ == "__main__":
    try:
        # Run the async main function
        asyncio.run(main())
    except KeyboardInterrupt:
        logger.info("Analyser Agent server stopped by user.")
        sys.exit(0)
    except Exception as e:
        logger.error(f"Error during server startup: {str(e)}", exc_info=True)
        sys.exit(1)
