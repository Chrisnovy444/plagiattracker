"""
AI Content Detection Service
Detects AI-generated content using perplexity, burstiness, and RoBERTa/DeBERTa classifiers.
Falls back to heuristic-only mode if torch/transformers unavailable.
"""
import re
from typing import Dict, List

try:
    import numpy as np
    NUMPY_LOADED = True
except ImportError:
    NUMPY_LOADED = False

try:
    import torch
    from transformers import GPT2LMHeadModel, GPT2Tokenizer, AutoTokenizer, AutoModelForSequenceClassification
    TORCH_AVAILABLE = True
except ImportError:
    TORCH_AVAILABLE = False

GPT2_LOADED = False
ROBERTA_LOADED = False

if TORCH_AVAILABLE:
    try:
        gpt2_tokenizer = GPT2Tokenizer.from_pretrained('gpt2')
        gpt2_model = GPT2LMHeadModel.from_pretrained('gpt2')
        gpt2_model.eval()
        GPT2_LOADED = True
    except Exception as e:
        print(f"Warning: Could not load GPT-2 model: {e}")

    try:
        roberta_tokenizer = AutoTokenizer.from_pretrained('roberta-base-openai-detector')
        roberta_model = AutoModelForSequenceClassification.from_pretrained('roberta-base-openai-detector')
        roberta_model.eval()
        ROBERTA_LOADED = True
    except Exception as e:
        print(f"Warning: Could not load RoBERTa model: {e}")


def calculate_perplexity(text: str) -> float:
    """Calculate perplexity of text using GPT-2"""
    if not GPT2_LOADED:
        return _heuristic_perplexity(text)

    try:
        encodings = gpt2_tokenizer(text, return_tensors='pt', truncation=True, max_length=512)
        with torch.no_grad():
            outputs = gpt2_model(**encodings, labels=encodings['input_ids'])
            loss = outputs.loss
        return torch.exp(loss).item()
    except Exception:
        return _heuristic_perplexity(text)


def _heuristic_perplexity(text: str) -> float:
    """Estimate perplexity without ML model using text statistics"""
    words = text.split()
    if len(words) < 5:
        return 50.0

    unique_ratio = len(set(words)) / len(words)
    avg_word_len = sum(len(w) for w in words) / len(words)
    # Higher vocabulary diversity and longer words suggest human writing (higher perplexity)
    estimated = 20 + (unique_ratio * 60) + (avg_word_len * 3)
    return min(max(estimated, 10.0), 150.0)


def detect_ai_roberta(text: str) -> Dict:
    """Detect AI content using RoBERTa classifier"""
    if not ROBERTA_LOADED:
        return _heuristic_ai_score(text)

    try:
        inputs = roberta_tokenizer(text, return_tensors='pt', truncation=True, max_length=512)
        with torch.no_grad():
            outputs = roberta_model(**inputs)
            logits = outputs.logits
            probs = torch.softmax(logits, dim=-1)
        ai_prob = probs[0][1].item()
        confidence = max(probs[0]).item()
        return {"score": round(ai_prob * 100, 2), "confidence": round(confidence * 100, 2)}
    except Exception:
        return _heuristic_ai_score(text)


def _heuristic_ai_score(text: str) -> Dict:
    """Estimate AI likelihood using text patterns without ML model"""
    sentences = re.split(r'[.!?]+', text)
    sentences = [s.strip() for s in sentences if s.strip()]

    if len(sentences) < 2:
        return {"score": 30.0, "confidence": 40.0}

    # AI indicators
    score = 0.0
    lengths = [len(s.split()) for s in sentences]
    mean_len = sum(lengths) / len(lengths)

    # Uniform sentence length (AI tendency)
    if len(lengths) > 2:
        variance = sum((l - mean_len) ** 2 for l in lengths) / len(lengths)
        std = variance ** 0.5
        cv = std / mean_len if mean_len > 0 else 0
        if cv < 0.3:
            score += 30
        elif cv < 0.5:
            score += 15

    # Transition words frequency (AI uses many)
    transitions = ['however', 'moreover', 'furthermore', 'additionally', 'consequently',
                   'therefore', 'nevertheless', 'in conclusion', 'in summary']
    text_lower = text.lower()
    transition_count = sum(1 for t in transitions if t in text_lower)
    if transition_count > 3:
        score += 20
    elif transition_count > 1:
        score += 10

    # Repetitive structure patterns
    starts = [s.split()[0].lower() if s.split() else '' for s in sentences]
    unique_starts = len(set(starts)) / len(starts) if starts else 1
    if unique_starts < 0.5:
        score += 15

    # Average sentence length (AI tends medium 15-25 words)
    if 15 < mean_len < 25:
        score += 10

    return {"score": min(score, 95.0), "confidence": 50.0}


def analyze_per_sentence(text: str) -> List[Dict]:
    """Analyze AI likelihood for each sentence"""
    sentences = re.split(r'[.!?]+', text)
    sentences = [s.strip() for s in sentences if s.strip() and len(s.split()) > 3]

    results = []
    for i, sentence in enumerate(sentences[:20]):
        perplexity = calculate_perplexity(sentence)
        roberta_result = detect_ai_roberta(sentence)

        ai_score = (
            (max(0, 100 - (perplexity * 2)) * 0.4) +
            (roberta_result["score"] * 0.6)
        )

        results.append({
            "sentence": sentence,
            "position": i,
            "ai_score": round(ai_score, 2),
            "perplexity": round(perplexity, 2),
            "roberta_score": roberta_result["score"],
            "level": "high" if ai_score > 70 else "medium" if ai_score > 40 else "low"
        })

    return results


def calculate_burstiness(text: str) -> float:
    """
    Calculate burstiness (sentence length variation).
    AI text tends to have uniform sentence lengths (low burstiness).
    """
    sentences = re.split(r'[.!?]+', text)
    sentences = [s.strip() for s in sentences if s.strip()]

    if len(sentences) < 3:
        return 0.5

    lengths = [len(s.split()) for s in sentences]
    mean_length = sum(lengths) / len(lengths)

    if mean_length == 0:
        return 0

    variance = sum((l - mean_length) ** 2 for l in lengths) / len(lengths)
    std_dev = variance ** 0.5

    return std_dev / mean_length


def detect_ai_content(text: str) -> Dict:
    """
    Detect AI-generated content using multiple methods.
    Works in degraded mode without torch/transformers.
    """
    perplexity = calculate_perplexity(text)
    burstiness = calculate_burstiness(text)
    roberta_result = detect_ai_roberta(text)

    perplexity_score = max(0, 100 - (perplexity * 2))
    burstiness_score = max(0, 100 - (burstiness * 200))
    roberta_score = roberta_result["score"]

    if ROBERTA_LOADED:
        ai_score = (perplexity_score * 0.25) + (burstiness_score * 0.15) + (roberta_score * 0.60)
    else:
        ai_score = (perplexity_score * 0.35) + (burstiness_score * 0.25) + (roberta_score * 0.40)

    if ai_score > 70:
        ai_level = "high"
    elif ai_score > 40:
        ai_level = "medium"
    else:
        ai_level = "low"

    sentence_analysis = analyze_per_sentence(text)

    highlighted_ai_passages = [
        {
            "text": sa["sentence"],
            "position": sa["position"],
            "ai_score": sa["ai_score"],
            "level": sa["level"]
        }
        for sa in sentence_analysis
        if sa["ai_score"] > 50
    ]

    mode = "full" if (GPT2_LOADED and ROBERTA_LOADED) else "heuristic"

    return {
        "ai_score": round(ai_score, 2),
        "ai_level": ai_level,
        "detection_mode": mode,
        "metrics": {
            "perplexity": round(perplexity, 2),
            "burstiness": round(burstiness, 3),
            "roberta_score": roberta_score,
            "roberta_confidence": roberta_result["confidence"],
            "perplexity_score": round(perplexity_score, 2),
            "burstiness_score": round(burstiness_score, 2)
        },
        "interpretation": {
            "perplexity": "Low perplexity suggests AI-generated text (predictable)",
            "burstiness": "Low burstiness suggests uniform AI writing style",
            "roberta": f"RoBERTa classifier confidence: {roberta_result['confidence']}%"
        },
        "sentence_analysis": sentence_analysis,
        "highlighted_ai_passages": highlighted_ai_passages
    }
