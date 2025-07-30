from researchengine.logger import logger
from bs4 import BeautifulSoup
from typing import List
from ddgs import DDGS
import requests

def web_search(web_query: str, max_results: int) -> List[dict]:
    return [r["href"] for r in DDGS().text(web_query, max_results=max_results)]


def web_scrape(url: str) -> str:
    try:
        response = requests.get(url)
        if response.status_code == 200:
            soup = BeautifulSoup(response.content, "html.parser")
            page_text = soup.get_text(separator=" ", strip=True)
            return page_text
        else:
            return f'Could not retrieve the webpage: Status code {response.status_code}'
    except Exception as e:
        logger.error(e)
        return f'Could not scrape webpage : {e}'
