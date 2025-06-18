"""Website crawler tool for crawling and analyzing website content."""

import requests
from bs4 import BeautifulSoup

def get_website_data(url: str) -> str:
    """
    Scrape the content of a website and return its text content.
    Args:
        url (str): The URL of the website to scrape.
    Returns:
        str: The text content of the website.
    """
    # Add http:// prefix if not present
    if not url.startswith(('http://', 'https://')):
        url = 'http://' + url
        
    # Make the request
    response = requests.get(url)
    
    # Parse the HTML content
    soup = BeautifulSoup(response.text, 'html.parser')
    
    # Remove script and style elements
    for script in soup(["script", "style"]):
        script.extract()
        
    # Get the text content
    text = soup.get_text()
    
    return text
