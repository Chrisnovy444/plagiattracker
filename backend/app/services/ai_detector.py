"""
AI Content Detection Service
Detects AI-generated content using perplexity, burstiness, and RoBERTa/DeBERTa classifiers
"""
import torch
from transformers import GPT2LMHeadModel, GPT2Tokenizer, AutoTokenizer, AutoModelForSequenceClassification
import numpy as np
from typing import Dict, List
import re


# Load GPT-2 model for perplexity
try:
    gpt2_tokenizer = GPT2Tokenizer.from_pretrained('gpt2')
    gpt2_model = GPT2LMHeadModel.from_pretrained('gpt2')
    gpt2_model.eval()
    GPT2_LOADED = True
except Exception as e:
    print(f"Warning: Could not load GPT-2 model: {e}")
    GPT2_LOADED = False

# Load RoBERTa AI detector
try:
    roberta_tokenizer = AutoTokenizer.from_pretrained('roberta-base-openai-detector')
    roberta_model = AutoModelForSequenceClassification.from_pretrained('roberta-base-openai-detector')
    roberta_model.eval()
    ROBERTA_LOADED = True
except Exception as e:
    print(f"Warning: Could not load RoBERTa model: {e}")
    ROBERTA_LOADED = False


def calculate_perplexity(text: str) -> float:
    """Calculate perplexity of text using GPT-2"""

    if not GPT2_LOADED:
        return 50.0  # Default value if model not loaded

    try:
        # Tokenize
        encodings = gpt2_tokenizer(text, return_tensors='pt', truncation=True, max_length=512)

        # Calculate loss
        with torch.no_grad():
            outputs = gpt2_model(**encodings, labels=encodings['input_ids'])
            loss = outputs.loss

        # Perplexity = exp(loss)
        perplexity = torch.exp(loss).item()

        return perplexity

    except Exception as e:
        print(f"Error calculating perplexity: {e}")
        return 50.0


def detect_ai_roberta(text: str) -> Dict:
    """Detect AI content using RoBERTa classifier"""

    if not ROBERTA_LOADED:
        return {"score": 0.0, "confidence": 0.0}

    try:
        # Tokenize
        inputs = roberta_tokenizer(text, return_tensors='pt', truncation=True, max_length=512)

        # Predict
        with torch.no_grad():
            outputs = roberta_model(**inputs)
            logits = outputs.logits
            probs = torch.softmax(logits, dim=-1)

        # Get AI probability (class 1 = AI-generated)
        ai_prob = probs[0][1].item()
        confidence = max(probs[0]).item()

        return {
            "score": round(ai_prob * 100, 2),
            "confidence": round(confidence * 100, 2)
        }

    except Exception as e:
        print(f"Error in RoBERTa detection: {e}")
        return {"score": 0.0, "confidence": 0.0}


def analyze_per_sentence(text: str) -> List[Dict]:
    """Analyze AI likelihood for each sentence"""

    # Split into sentences
    sentences = re.split(r'[.!?]+', text)
    sentences = [s.strip() for s in sentences if s.strip() and len(s.split()) > 3]

    results = []

    for i, sentence in enumerate(sentences[:20]):  # Limit to 20 sentences
        # Calculate perplexity for sentence
        perplexity = calculate_perplexity(sentence)

        # RoBERTa detection for sentence
        roberta_result = detect_ai_roberta(sentence)

        # Burstiness doesn't apply per sentence, so use perplexity + RoBERTa
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
    Calculate burstiness (sentence length variation)
    AI text tends to have uniform sentence lengths (low burstiness)
    Human text has more variation (high burstiness)
    """

    # Split into sentences
    sentences = re.split(r'[.!?]+', text)
    sentences = [s.strip() for s in sentences if s.strip()]

    if len(sentences) < 3:
        return 0.5

    # Calculate sentence lengths
    lengths = [len(s.split()) for s in sentences]

    # Calculate standard deviation (variation)
    mean_length = np.mean(lengths)
    std_dev = np.std(lengths)

    # Burstiness = coefficient of variation
    if mean_length > 0:
        burstiness = std_dev / mean_length
    else:
        burstiness = 0

    return burstiness


def detect_ai_content(text: str) -> Dict:
    """
    Detect AI-generated content using multiple methods

    Returns:
        Detection results with overall score, per-sentence analysis, and highlighted AI passages
    """

    # Calculate global metrics
    perplexity = calculate_perplexity(text)
    burstiness = calculate_burstiness(text)
    roberta_result = detect_ai_roberta(text)

    # Score calculation (0-100)
    perplexity_score = max(0, 100 - (perplexity * 2))
    burstiness_score = max(0, 100 - (burstiness * 200))
    roberta_score = roberta_result["score"]

    # Weighted average (RoBERTa gets highest weight as it's specifically trained)
    ai_score = (
        (perplexity_score * 0.25) +
        (burstiness_score * 0.15) +
        (roberta_score * 0.60)
    )

    # Determine level
    if ai_score > 70:
        ai_level = "high"
    elif ai_score > 40:
        ai_level = "medium"
    else:
        ai_level = "low"

    # Per-sentence analysis
    sentence_analysis = analyze_per_sentence(text)

    # Extract high AI-score sentences for highlighting
    highlighted_ai_passages = [
        {
            "text": sa["sentence"],
            "position": sa["position"],
            "ai_score": sa["ai_score"],
            "level": sa["level"]
        }
        for sa in sentence_analysis
        if sa["ai_score"] > 50  # Only highlight medium/high AI likelihood
    ]

    return {
        "ai_score": round(ai_score, 2),
        "ai_level": ai_level,
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
