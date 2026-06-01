"""
OpenAlex API Integration
Search academic works from OpenAlex.org (200M+ articles)
"""
import httpx
from typing import List, Dict


OPENALEX_API_URL = "https://api.openalex.org/works"


async def search_openalex(query: str, max_results: int = 5) -> List[Dict]:
    """
    Search OpenAlex for similar papers

    Args:
        query: Search query
        max_results: Maximum number of results

    Returns:
        List of work metadata
    """

    params = {
        "search": query,
        "per_page": max_results,
        "sort": "relevance_score:desc"
    }

    headers = {
        "User-Agent": "PLAGIATTRACKER/1.0 (checkone076@gmail.com)"
    }

    try:
        async with httpx.AsyncClient(timeout=10.0) as client:
            response = await client.get(OPENALEX_API_URL, params=params, headers=headers)
            response.raise_for_status()

        data = response.json()

        papers = []
        for work in data.get("results", []):
            # Extract abstract
            abstract = ""
            if work.get("abstract_inverted_index"):
                # Reconstruct abstract from inverted index
                inverted = work["abstract_inverted_index"]
                words = [""] * sum(len(positions) for positions in inverted.values())
                for word, positions in inverted.items():
                    for pos in positions:
                        if pos < len(words):
                            words[pos] = word
                abstract = " ".join(words)

            papers.append({
                "source": "OpenAlex",
                "title": work.get("title", "Unknown"),
                "abstract": abstract,
                "url": work.get("doi", "") or work.get("id", ""),
                "text": abstract  # For similarity check
            })

        return papers

    except Exception as e:
        print(f"Error searching OpenAlex: {e}")
        return []
