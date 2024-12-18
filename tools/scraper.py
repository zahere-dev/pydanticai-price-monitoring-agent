
import requests
from bs4 import BeautifulSoup, Comment
from markdownify import markdownify as md

async def scrape_url(url: str) -> str | None:
    """
    Fetches and parses the content of a given URL using BeautifulSoup.

    Args:
        url (str): The URL to scrape.

    Returns:
        markdown content of the scrapped HTML
    """
    try:
        # Send a GET request to the URL
        response = requests.get(url)
        response.raise_for_status()  # Raise an HTTPError for bad responses (4xx or 5xx)

        # Parse the HTML content of the page
        soup = BeautifulSoup(response.text, 'html.parser')

        # Remove script and style elements
        for script_or_style in soup(["script", "style"]):
            script_or_style.decompose()

        # Remove comments
        for comment in soup.find_all(string=lambda text: isinstance(text, Comment)):
            comment.extract()

        # Get cleaned text
        cleaned_html = soup.prettify()

        return md(cleaned_html)

    except requests.exceptions.RequestException as e:
        print(f"Error fetching the URL: {e}")
        return None
