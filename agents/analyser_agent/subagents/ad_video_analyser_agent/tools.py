"""
Get summary description along with the audio to text of a video using Google Gemini.
"""

import os
import google.generativeai as genai
from dotenv import load_dotenv
from .prompt import VIDEO_GUIDELINES

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
    prompt += f"\n\nYou must use the following guidelines for the video ad: {VIDEO_GUIDELINES}\n\nAlso, provide a score out of 100 based on the guidelines."
    file1 = genai.upload_file(path=path)
    file1 = genai.get_file(file1.name)

    model = genai.GenerativeModel(model_name="models/gemini-2.0-flash")

    response = model.generate_content([prompt, file1], request_options={"timeout": 600})
    genai.delete_file(file1.name)

    return response.text
