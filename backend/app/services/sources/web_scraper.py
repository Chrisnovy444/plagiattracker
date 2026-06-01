"""
Web Scraper for non-academic sources
Searches web content using DuckDuckGo + BeautifulSoup
"""
import httpx
from bs4 import BeautifulSoup
from typing import List, Dict
import re


async def search_web(query: str, max_results: int = 5) -> List[Dict]:
    """
    Search web content using DuckDuckGo HTML search

    Args:
        query: Search query
        max_results: Maximum number of results

    Returns:
        List of source documents
    """

    # Use DuckDuckGo HTML search (no API key required)
    search_url = "https://html.duckduckgo.com/html/"

    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"
    }

    data = {
        "q": query,
        "kl": "wt-wt"  # All regions
    }

    try:
        async with httpx.AsyncClient(timeout=15.0, follow_redirects=True) as client:
            # Get search results
            response = await client.post(search_url, data=data, headers=headers)
            response.raise_for_status()

            soup = BeautifulSoup(response.text, 'html.parser')

            # Find all result links
            result_links = soup.find_all('a', class_='result__a', limit=max_results)

            results = []

            for link in result_links:
                url = link.get('href', '')
                title = link.get_text(strip=True)

                if not url or not title:
                    continue

                # Try to fetch and extract content
                try:
                    page_response = await client.get(url, headers=headers, timeout=10.0)
                    page_response.raise_for_status()

                    page_soup = BeautifulSoup(page_response.text, 'html.parser')

                    # Remove script and style elements
                    for script in page_soup(["script", "style", "nav", "footer", "header"]):
                        script.decompose()

                    # Extract text from paragraphs
                    paragraphs = page_soup.find_all('p')
                    text = ' '.join([p.get_text(strip=True) for p in paragraphs[:10]])  # First 10 paragraphs

                    # Clean text
                    text = re.sub(r'\s+', ' ', text)
                    text = text[:1000]  # Limit to 1000 chars

                    if len(text) > 50:  # Minimum content length
                        results.append({
                            "title": title,
                            "abstract": text,
                            "url": url,
                            "source": "Web"
                        })

                except Exception as e:
                    # If can't fetch content, add just the link
                    results.append({
                        "title": title,
                        "abstract": "",
                        "url": url,
                        "source": "Web"
                    })
                    print(f"Error fetching {url}: {e}")

            return results

    except Exception as e:
        print(f"Web search error: {e}")
        return []
