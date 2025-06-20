"""Website crawler tool for crawling and analyzing website content."""

import logging
import requests
from bs4 import BeautifulSoup

# Configure logging
logger = logging.getLogger(__name__)

def get_website_data(url: str) -> str:
    """
    Scrape the content of a website and return its text content.
    Args:
        url (str): The URL of the website to scrape.
    Returns:
        str: The text content of the website.
    """
    logger.info(f"Scraping website content from: {url}")
    
    try:
        # Add http:// prefix if not present
        if not url.startswith(('http://', 'https://')):
            original_url = url
            url = 'http://' + url
            logger.debug(f"Added http:// prefix to URL: {original_url} -> {url}")
            
        # Make the request
        logger.debug(f"Making HTTP request to: {url}")
        response = requests.get(url)
        response.raise_for_status()  # Raise exception for 4XX/5XX responses
        logger.debug(f"Received response with status code: {response.status_code}")
        
        # Parse the HTML content
        logger.debug("Parsing HTML content with BeautifulSoup")
        soup = BeautifulSoup(response.text, 'html.parser')
        
        # Remove script and style elements
        logger.debug("Removing script and style elements")
        for script in soup(["script", "style"]):
            script.extract()
            
        # Get the text content
        text = soup.get_text()
        
        logger.info(f"Successfully scraped website content ({len(text)} characters)")
        return text
    except requests.exceptions.RequestException as e:
        logger.error(f"Error making request to {url}: {str(e)}")
        raise
    except Exception as e:
        logger.error(f"Error scraping website content: {str(e)}")
        raise
