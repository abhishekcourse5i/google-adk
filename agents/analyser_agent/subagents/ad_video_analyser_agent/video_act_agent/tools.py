"""
Get summary description along with the audio to text of a video using Google Gemini.
"""

import os
import logging
import time
import google.generativeai as genai
from dotenv import load_dotenv
from .prompt import VIDEO_GUIDELINES

# Configure logging
logger = logging.getLogger(__name__)

load_dotenv()

api_key = os.getenv("GEMINI_API_KEY")
genai.configure(api_key=api_key)

def get_video_summary(
        path: str,
        prompt: str,
    ) -> str:
    """
    Get a summary description and audio to text of a video using Google Gemini.
    Args:
        path (str): The path of the video to analyze.
        prompt (str): The prompt to use for generating the summary.
    Returns:
        str: The generated summary of the video.
    """
    logger.info(f"Getting video summary for file: {path}")
    
    prompt += f"\n\nYou must use the following guidelines for the video ad: {VIDEO_GUIDELINES}\n\nAlso, provide a score out of 100 based on the guidelines."
    
    try:
        logger.debug(f"Uploading video file: {path}")
        file1 = genai.upload_file(path=path)

        # Check whether the file is ready to be used.
        while file1.state.name == "PROCESSING":
            print('.', end='')
            time.sleep(10)
            gen_file = genai.get_file(gen_file.name)
        
        logger.debug("Initializing Gemini model")
        model = genai.GenerativeModel(model_name="models/gemini-2.0-flash")
        
        logger.info("Generating content with Gemini")
        response = model.generate_content([prompt, file1], request_options={"timeout": 600})
        
        logger.debug(f"Deleting uploaded file: {file1.name}")
        genai.delete_file(file1.name)
        
        logger.info("Video summary generated successfully")
        return response.text
    except Exception as e:
        logger.error(f"Error generating video summary: {str(e)}")
        raise
