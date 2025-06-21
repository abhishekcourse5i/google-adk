"""
API endpoints for the Analyser Agent.
This module defines the API endpoints for the Analyser Agent.
"""

import os
import ast
import logging
import shutil
import uuid
from typing import Dict, Any, Optional, List
from fastapi import APIRouter, Body, HTTPException, Form, UploadFile, File
from fastapi.responses import JSONResponse
from pydantic import BaseModel, Field
import json

from .database import AnalysisDatabase

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Define response model
class AnalysisResponse(BaseModel):
    """Standard response model for analysis results."""
    message: str = Field(..., description="The analysis result")
    status: str = Field(default="success", description="Status of the response (success, error)")
    data: Dict[str, Any] = Field(default_factory=dict, description="Additional data returned by the agent")
    session_id: Optional[str] = Field(None, description="Session identifier for stateful interactions")

def create_api_router(task_manager):
    """
    Create an API router with a unified endpoint for all types of analysis.
    
    Args:
        task_manager: The TaskManager instance for handling tasks
        
    Returns:
        An APIRouter instance with the defined endpoints
    """
    router = APIRouter(prefix="/api/v1", tags=["analysis"])
    
    # Initialize the database
    db = AnalysisDatabase()
    
    @router.post("/analyze", response_model=AnalysisResponse)
    async def analyze_content(
        document_name: Optional[str] = Form(None),
        session_id: Optional[str] = Form(None),
        context: Optional[str] = Form("{}"),
        url: Optional[str] = Form(None),
        document_type: Optional[str] = Form(None),
        guidelines: Optional[str] = Form(None),
        file: Optional[UploadFile] = File(None)
    ):
        """
        Unified endpoint to analyze content (Instagram post, video, or website).
        
        Args:
            request: The analysis request containing URL, file_path, guidelines, session_id, and context
            
        Returns:
            Analysis results
        """
        logger.info("Starting content analysis request")
        try:
            
            context = json.loads(context or "{}")
            
            # Initialize file_path to None
            file_path = None
            
            # Handle file upload if provided
            if file:
                logger.info(f"File upload detected: {file.filename}")
                # Create static directory if it doesn't exist
                static_dir = os.path.join(os.getcwd(), "static")
                os.makedirs(static_dir, exist_ok=True)
                
                # Save the file to the static directory
                file_location = os.path.join(static_dir, file.filename)
                with open(file_location, "wb") as buffer:
                    shutil.copyfileobj(file.file, buffer)
                
                # Update file_path to point to the saved file
                file_path = file_location
                logger.info(f"File saved to: {file_path}")
            
            # Determine the type of content to analyze
            provided_inputs = sum(1 for x in [url, file_path] if x)
            logger.info(f"Inputs provided: url={bool(url)}, file_path={bool(file_path)}, file_upload={bool(file)}")
            
            if provided_inputs > 1:
                logger.warning("Multiple inputs provided, raising exception")
                raise HTTPException(status_code=400, detail="Cannot provide multiple inputs. Choose one: URL or file path.")
            
            if provided_inputs == 0:
                logger.warning("No inputs provided, raising exception")
                raise HTTPException(status_code=400, detail="Must provide one input: URL or file path.")
            
            # Process inputs
            if file_path:
                logger.info(f"Processing file from path: {file_path}")
                # Verify the file exists
                if not os.path.exists(file_path):
                    logger.warning(f"File not found at path: {file_path}")
                    raise HTTPException(status_code=400, detail=f"File not found at path: {file_path}")
                
                # Determine if it's a video or image based on file extension
                file_ext = os.path.splitext(file_path)[1].lower()
                video_extensions = ['.mp4', '.mov', '.avi', '.wmv', '.flv', '.mkv']
                image_extensions = ['.jpg', '.jpeg', '.png', '.gif', '.bmp', '.tiff']
                
                # Add file path to context
                context["file_path"] = file_path
                
                if file_ext in video_extensions:
                    # It's a video
                    message = "Analyze this video ad" + f" in file path: {file_path}"
                    logger.info(f"Detected video file with extension: {file_ext}")
                elif file_ext in image_extensions:
                    # It's an image
                    # Assume it's an Instagram post
                    message = "Analyze this Instagram post" + f" in file path: {file_path}"
                    logger.info(f"Detected image file with extension: {file_ext}")
                else:
                    # Unsupported file type
                    logger.error(f"Unsupported file type: {file_ext}")
                    raise HTTPException(status_code=400, detail=f"Unsupported file type: {file_ext}")

            else:
                # It's a website
                logger.info(f"Processing website URL: {url}")
                context["url"] = url
                message = "Analyze this website" + f" at URL: {url}"

            
            # Add guidelines to context if provided
            if guidelines:
                context["guidelines"] = guidelines
                message += f" with guidelines: {guidelines}"
            
            # Process the task
            logger.info(f"Sending task to task manager: {message}")
            logger.debug(f"Context: {context}")
            result = await task_manager.process_task(message, context, session_id)

            ast_result = ast.literal_eval(result.get("message", "{}"))

            logger.info("Task processing completed")
            
            # Store the result in the database
            try:

                logger.info("Storing analysis result in database")
                # Extract data from the result
                data = ast_result
                
                logger.debug(f"Extracted data: {data}")

                # Generate a unique document ID if not provided
                document_id = context.get("document_id", str(uuid.uuid4()))
                
                if float(data.get("score", 0.0)) > 70:
                    status = "Approved"
                else:
                    status = "Reject"
                
                # Extract other fields from the result data
                # These fields might need to be adjusted based on the actual structure of your result data
                score = float(data.get("score", 0.0))
                suggestions = data.get("suggestions", [])
                conflicts = data.get("conflicts", [])
                summary = data.get("summary", "")
                guidelines_used = data.get("guidelines", [])
                
                # Store in database
                db.store_analysis_result(
                    document_id=document_id,
                    document_name=document_name,
                    status=status,
                    score=score,
                    document_type=document_type or "",
                    file_url=file_path or url or "",
                    suggestions=suggestions,
                    conflicts=conflicts,
                    guidelines=guidelines_used or "",
                    summary=summary
                )
                
                logger.info(f"Analysis result stored in database with ID: {document_id}")
                
                # Add document_id to the response data
                result["data"]["document_id"] = document_id
            except Exception as e:
                logger.error(f"Error storing analysis result in database: {str(e)}")
            
            logger.info("Returning analysis response")
            return AnalysisResponse(
                message=result.get("message", "Analysis completed"),
                status="success",
                data=result.get("data", {}),
                session_id=session_id
            )
        except Exception as e:
            logger.error(f"Error analyzing content: {str(e)}", exc_info=True)
            
            logger.info("Returning error response")
            return AnalysisResponse(
                message=f"Error analyzing content: {str(e)}",
                status="error",
                data={"error_type": type(e).__name__},
                session_id=session_id
            )
    
    @router.get("/health", response_model=Dict[str, str])
    async def health_check():
        """
        Health check endpoint.
        
        Returns:
            Health status
        """
        logger.info("Health check requested")
        return {"status": "healthy"}
    
    @router.get("/analysis/{document_id}", response_model=Dict[str, Any])
    async def get_analysis(document_id: str):
        """
        Get analysis result by document ID.
        
        Args:
            document_id: The document ID to retrieve
            
        Returns:
            Analysis result
        """
        logger.info(f"Retrieving analysis result for document ID: {document_id}")
        result = db.get_analysis_result(document_id)
        
        if result:
            return result
        else:
            raise HTTPException(status_code=404, detail=f"Analysis result not found for document ID: {document_id}")
    
    @router.get("/analysis", response_model=List[Dict[str, Any]])
    async def get_all_analyses():
        """
        Get all analysis results.
        
        Returns:
            List of all analysis results
        """
        logger.info("Retrieving all analysis results")
        results = db.get_all_analysis_results()
        return results
    
    @router.delete("/analysis/{document_id}", response_model=Dict[str, Any])
    async def delete_analysis(document_id: str):
        """
        Delete analysis result by document ID.
        
        Args:
            document_id: The document ID to delete
            
        Returns:
            Status of the operation
        """
        logger.info(f"Deleting analysis result for document ID: {document_id}")
        success = db.delete_analysis_result(document_id)
        
        if success:
            return {"status": "success", "message": f"Analysis result deleted for document ID: {document_id}"}
        else:
            raise HTTPException(status_code=404, detail=f"Analysis result not found for document ID: {document_id}")
    
    @router.post("/reset-database", response_model=Dict[str, Any])
    async def reset_database():
        """
        Reset the database by dropping and recreating the analysis_results table.
        
        Returns:
            Status of the operation
        """
        logger.info("Resetting database")
        success = db.reset_database()
        
        if success:
            return {"status": "success", "message": "Database reset successfully"}
        else:
            raise HTTPException(status_code=500, detail="Error resetting database")
    
    return router
