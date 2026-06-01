"""
arXiv API Integration
Search academic papers from arXiv.org
"""
import httpx
from typing import List, Dict
import xml.etree.ElementTree as ET


ARXIV_API_URL = "http://export.arxiv.org/api/query"


async def search_arxiv(query: str, max_results: int = 5) -> List[Dict]:
    """
    Search arXiv for similar papers

    Args:
        query: Search query (keywords from document)
        max_results: Maximum number of results

    Returns:
        List of paper metadata
    """

    params = {
        "search_query": f"all:{query}",
        "start": 0,
        "max_results": max_results,
        "sortBy": "relevance",
        "sortOrder": "descending"
    }

    try:
        async with httpx.AsyncClient(timeout=10.0) as client:
            response = await client.get(ARXIV_API_URL, params=params)
            response.raise_for_status()

        # Parse XML response
        root = ET.fromstring(response.content)

        # Namespace
        ns = {'atom': 'http://www.w3.org/2005/Atom'}

        papers = []
        for entry in root.findall('atom:entry', ns):
            title_elem = entry.find('atom:title', ns)
            summary_elem = entry.find('atom:summary', ns)
            link_elem = entry.find('atom:id', ns)

            if title_elem is not None and summary_elem is not None:
                papers.append({
                    "source": "arXiv",
                    "title": title_elem.text.strip(),
                    "abstract": summary_elem.text.strip(),
                    "url": link_elem.text if link_elem is not None else "",
                    "text": summary_elem.text.strip()  # For similarity check
                })

        return papers

    except Exception as e:
        print(f"Error searching arXiv: {e}")
        return []
