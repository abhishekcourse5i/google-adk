"""
Check whether the instagram post adheres to the provided guidelines.
"""

import os
import google.generativeai as genai
from dotenv import load_dotenv
from .prompt import INSTA_GUIDELINES

load_dotenv()

api_key = os.getenv("GEMINI_API_KEY")
genai.configure(api_key=api_key)

def get_insta_summary(
        path: str,
        prompt: str,
    ) -> str:
    """
    Analyzes an Instagram post and provides a summary using Google Gemini.
    Args:
        path (str): The path to the Instagram post file.
        prompt (str): The prompt to guide the analysis.
    Returns:
        str: The summary of the Instagram post.
    """
    prompt += f"\n\nYou must use the following guidelines for the Instagram post: {INSTA_GUIDELINES}\n\nAlso, provide a score out of 100 based if the post follows the guidelines."
    
    file1 = genai.upload_file(path=path)
    file1 = genai.get_file(file1.name)

    model = genai.GenerativeModel(model_name="models/gemini-2.0-flash")

    response = model.generate_content([prompt, file1], request_options={"timeout": 600})
    genai.delete_file(file1.name)

    return response.text
