"""
Semantic Scholar API Integration
200M+ papers with AI-powered relevance
"""
import httpx
from typing import List, Dict


async def search_semantic_scholar(query: str, max_results: int = 10) -> List[Dict]:
    """
    Search Semantic Scholar API for academic papers

    Args:
        query: Search query
        max_results: Maximum number of results

    Returns:
        List of source documents
    """

    url = "https://api.semanticscholar.org/graph/v1/paper/search"
    params = {
        "query": query,
        "limit": max_results,
        "fields": "paperId,title,abstract,url,authors,year,citationCount"
    }

    headers = {
        "User-Agent": "PLAGIATTRACKER/1.0 (checkone076@gmail.com)"
    }

    try:
        async with httpx.AsyncClient(timeout=15.0) as client:
            response = await client.get(url, params=params, headers=headers)
            response.raise_for_status()

            data = response.json()
            papers = data.get("data", [])

            results = []
            for paper in papers:
                # Extract basic info
                title = paper.get("title", "No title")
                abstract = paper.get("abstract", "")
                paper_url = paper.get("url", "")
                paper_id = paper.get("paperId", "")

                # Fallback URL
                if not paper_url and paper_id:
                    paper_url = f"https://www.semanticscholar.org/paper/{paper_id}"

                # Extract authors
                authors = paper.get("authors", [])
                author_names = [a.get("name", "") for a in authors[:3]]

                results.append({
                    "title": title,
                    "abstract": abstract or "",
                    "url": paper_url,
                    "authors": ", ".join(author_names) if author_names else "Unknown",
                    "year": paper.get("year", ""),
                    "citations": paper.get("citationCount", 0),
                    "source": "Semantic Scholar"
                })

            return results

    except Exception as e:
        print(f"Semantic Scholar API error: {e}")
        return []
