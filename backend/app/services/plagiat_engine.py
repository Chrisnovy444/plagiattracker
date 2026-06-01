"""
Plagiarism Detection Engine
Detects copied content using MinHash, Sentence-BERT and academic APIs
"""
from datasketch import MinHash, MinHashLSH
from typing import List, Dict
import hashlib

SBERT_LOADED = False
sbert_model = None

try:
    from sentence_transformers import SentenceTransformer, util
    import torch
    sbert_model = SentenceTransformer('all-MiniLM-L6-v2')
    SBERT_LOADED = True
except Exception as e:
    print(f"Warning: Sentence-BERT unavailable (MinHash-only mode): {e}")


def calculate_similarity(text1: str, text2: str) -> float:
    """Calculate similarity between two texts using MinHash"""

    # Create MinHash objects
    m1 = MinHash(num_perm=128)
    m2 = MinHash(num_perm=128)

    # Add words to MinHash
    for word in text1.lower().split():
        m1.update(word.encode('utf8'))

    for word in text2.lower().split():
        m2.update(word.encode('utf8'))

    # Calculate Jaccard similarity
    return m1.jaccard(m2)


def calculate_semantic_similarity(text1: str, text2: str) -> float:
    """Calculate semantic similarity using Sentence-BERT (detects paraphrasing)"""

    if not SBERT_LOADED:
        return 0.0

    try:
        # Generate embeddings
        embeddings = sbert_model.encode([text1, text2], convert_to_tensor=True)

        # Calculate cosine similarity
        similarity = util.cos_sim(embeddings[0], embeddings[1])

        return float(similarity.item())

    except Exception as e:
        print(f"Error calculating semantic similarity: {e}")
        return 0.0


def detect_plagiarism(text: str, sources: List[Dict]) -> Dict:
    """
    Detect plagiarism in text against sources using both MinHash and Sentence-BERT

    Args:
        text: Text to check
        sources: List of source documents from APIs

    Returns:
        Plagiarism detection results with highlighted passages
    """

    results = {
        "total_sources_checked": len(sources),
        "matches": [],
        "plagiarism_score": 0.0,
        "plagiarism_level": "low",
        "highlighted_passages": []
    }

    if not sources:
        return results

    # Split text into sentences for passage-level detection
    import re
    sentences = re.split(r'[.!?]+', text)
    sentences = [s.strip() for s in sentences if s.strip() and len(s.split()) > 3]

    # Check against each source
    similarities = []
    passage_matches = []

    for source in sources:
        source_text = source.get("abstract", "") or source.get("text", "")
        if not source_text:
            continue

        # 1. MinHash similarity (exact/near-exact copies)
        minhash_sim = calculate_similarity(text, source_text)

        # 2. Semantic similarity (paraphrasing detection)
        semantic_sim = calculate_semantic_similarity(text, source_text)

        # Combined similarity (weighted)
        combined_sim = max(minhash_sim, semantic_sim * 0.85)

        if combined_sim > 0.3:  # Threshold 30%
            match = {
                "source": source.get("title", "Unknown"),
                "url": source.get("url", ""),
                "similarity": round(combined_sim * 100, 2),
                "minhash_similarity": round(minhash_sim * 100, 2),
                "semantic_similarity": round(semantic_sim * 100, 2),
                "type": "exact_copy" if minhash_sim > 0.7 else "paraphrase" if semantic_sim > 0.6 else "similar"
            }
            results["matches"].append(match)
            similarities.append(combined_sim)

            # Find matching passages
            for i, sentence in enumerate(sentences):
                sent_sim = calculate_semantic_similarity(sentence, source_text)
                if sent_sim > 0.5:  # Passage threshold
                    passage_matches.append({
                        "text": sentence,
                        "position": i,
                        "similarity": round(sent_sim * 100, 2),
                        "source": source.get("title", "Unknown"),
                        "type": "exact" if sent_sim > 0.8 else "paraphrase"
                    })

    # Calculate overall score
    if similarities:
        results["plagiarism_score"] = round(max(similarities) * 100, 2)

        # Determine level
        if results["plagiarism_score"] > 50:
            results["plagiarism_level"] = "high"
        elif results["plagiarism_score"] > 25:
            results["plagiarism_level"] = "medium"
        else:
            results["plagiarism_level"] = "low"

    # Sort matches by similarity
    results["matches"].sort(key=lambda x: x["similarity"], reverse=True)

    # Add highlighted passages (deduplicate and sort)
    seen = set()
    for pm in sorted(passage_matches, key=lambda x: x["similarity"], reverse=True):
        if pm["text"] not in seen:
            results["highlighted_passages"].append(pm)
            seen.add(pm["text"])

    # Limit to top 20 passages
    results["highlighted_passages"] = results["highlighted_passages"][:20]

    return results
