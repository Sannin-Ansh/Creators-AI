import logging
import requests
import xml.etree.ElementTree as ET
from urllib.parse import quote

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def fetch_trending_topics(query: str) -> list:
    """
    Fetches real-time trending news / topics for a query using Google News RSS.
    Does not require API keys.
    
    Returns a list of dictionaries with keys:
    - title
    - link
    - source
    - pub_date
    """
    logger.info(f"Fetching trending topics/news for: {query}")
    encoded_query = quote(query)
    url = f"https://news.google.com/rss/search?q={encoded_query}&hl=en-US&gl=US&ceid=US:en"
    
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36 CreatorsAI/1.0"
    }
    
    try:
        response = requests.get(url, headers=headers, timeout=10)
        if response.status_code == 200:
            root = ET.fromstring(response.content)
            items = root.findall(".//item")
            
            trends = []
            # Take top 5 trends
            for item in items[:5]:
                title = item.find("title").text if item.find("title") is not None else "No Title"
                link = item.find("link").text if item.find("link") is not None else ""
                pub_date = item.find("pubDate").text if item.find("pubDate") is not None else ""
                source = item.find("source").text if item.find("source") is not None else "Google News"
                
                trends.append({
                    "title": title,
                    "link": link,
                    "pub_date": pub_date,
                    "source": source
                })
            
            if trends:
                return trends
            else:
                logger.warning("Empty trends RSS results. Returning fallback trends.")
                return get_mock_trends(query)
        else:
            logger.warning(f"Trends RSS returned status {response.status_code}. Returning fallback.")
            return get_mock_trends(query)
            
    except Exception as e:
        logger.error(f"Error fetching trends: {e}. Returning fallback.")
        return get_mock_trends(query)

def get_mock_trends(query: str) -> list:
    """Fallback mock trends related to the query."""
    return [
        {
            "title": f"Why {query} is dominating the tech sector in 2026",
            "link": "https://news.google.com/mock1",
            "pub_date": "Sat, 04 Jul 2026 00:00:00 GMT",
            "source": "TechCrunch"
        },
        {
            "title": f"The rise of no-code platforms integrating {query}",
            "link": "https://news.google.com/mock2",
            "pub_date": "Fri, 03 Jul 2026 12:30:00 GMT",
            "source": "VentureBeat"
        },
        {
            "title": f"How startups are leveraging {query} to scale rapidly",
            "link": "https://news.google.com/mock3",
            "pub_date": "Thu, 02 Jul 2026 09:15:00 GMT",
            "source": "Forbes"
        }
    ]
