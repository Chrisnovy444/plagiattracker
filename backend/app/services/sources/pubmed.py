"""
PubMed API Integration
35M+ biomedical articles
"""
import httpx
from typing import List, Dict
import xml.etree.ElementTree as ET


async def search_pubmed(query: str, max_results: int = 10) -> List[Dict]:
    """
    Search PubMed API for biomedical articles

    Args:
        query: Search query
        max_results: Maximum number of results

    Returns:
        List of source documents
    """

    # Step 1: Search for PMIDs
    search_url = "https://eutils.ncbi.nlm.nih.gov/entrez/eutils/esearch.fcgi"
    search_params = {
        "db": "pubmed",
        "term": query,
        "retmax": max_results,
        "retmode": "json",
        "tool": "plagiattracker",
        "email": "checkone076@gmail.com"
    }

    try:
        async with httpx.AsyncClient(timeout=15.0) as client:
            # Get PMIDs
            search_response = await client.get(search_url, params=search_params)
            search_response.raise_for_status()

            search_data = search_response.json()
            pmids = search_data.get("esearchresult", {}).get("idlist", [])

            if not pmids:
                return []

            # Step 2: Fetch article details
            fetch_url = "https://eutils.ncbi.nlm.nih.gov/entrez/eutils/efetch.fcgi"
            fetch_params = {
                "db": "pubmed",
                "id": ",".join(pmids),
                "retmode": "xml",
                "tool": "plagiattracker",
                "email": "checkone076@gmail.com"
            }

            fetch_response = await client.get(fetch_url, params=fetch_params)
            fetch_response.raise_for_status()

            # Parse XML
            root = ET.fromstring(fetch_response.content)

            results = []
            for article in root.findall(".//PubmedArticle"):
                try:
                    # Extract title
                    title_elem = article.find(".//ArticleTitle")
                    title = title_elem.text if title_elem is not None else "No title"

                    # Extract abstract
                    abstract_texts = article.findall(".//AbstractText")
                    abstract = " ".join([at.text for at in abstract_texts if at.text]) if abstract_texts else ""

                    # Extract PMID
                    pmid_elem = article.find(".//PMID")
                    pmid = pmid_elem.text if pmid_elem is not None else ""

                    # URL
                    url = f"https://pubmed.ncbi.nlm.nih.gov/{pmid}/" if pmid else ""

                    # Extract authors
                    authors = article.findall(".//Author")
                    author_names = []
                    for author in authors[:3]:
                        lastname = author.find("LastName")
                        forename = author.find("ForeName")
                        if lastname is not None:
                            name = lastname.text
                            if forename is not None:
                                name = f"{forename.text} {name}"
                            author_names.append(name)

                    results.append({
                        "title": title,
                        "abstract": abstract,
                        "url": url,
                        "pmid": pmid,
                        "authors": ", ".join(author_names) if author_names else "Unknown",
                        "source": "PubMed"
                    })

                except Exception as e:
                    print(f"Error parsing PubMed article: {e}")
                    continue

            return results

    except Exception as e:
        print(f"PubMed API error: {e}")
        return []
