"""
CrossRef API Integration
150M+ DOI-registered articles
"""
import httpx
from typing import List, Dict


async def search_crossref(query: str, max_results: int = 10) -> List[Dict]:
    """
    Search CrossRef API for academic papers

    Args:
        query: Search query
        max_results: Maximum number of results

    Returns:
        List of source documents
    """

    url = "https://api.crossref.org/works"
    params = {
        "query": query,
        "rows": max_results,
        "select": "DOI,title,abstract,URL,author,published"
    }

    headers = {
        "User-Agent": "PLAGIATTRACKER/1.0 (mailto:checkone076@gmail.com)"
    }

    try:
        async with httpx.AsyncClient(timeout=15.0) as client:
            response = await client.get(url, params=params, headers=headers)
            response.raise_for_status()

            data = response.json()
            items = data.get("message", {}).get("items", [])

            results = []
            for item in items:
                # Extract title
                title_list = item.get("title", [])
                title = title_list[0] if title_list else "No title"

                # Extract abstract (if available)
                abstract = item.get("abstract", "")

                # Extract DOI and URL
                doi = item.get("DOI", "")
                url = item.get("URL", f"https://doi.org/{doi}" if doi else "")

                # Extract authors
                authors = item.get("author", [])
                author_names = []
                for author in authors[:3]:  # First 3 authors
                    given = author.get("given", "")
                    family = author.get("family", "")
                    if given or family:
                        author_names.append(f"{given} {family}".strip())

                results.append({
                    "title": title,
                    "abstract": abstract,
                    "url": url,
                    "doi": doi,
                    "authors": ", ".join(author_names) if author_names else "Unknown",
                    "source": "CrossRef"
                })

            return results

    except Exception as e:
        print(f"CrossRef API error: {e}")
        return []
