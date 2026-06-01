"""
Text Correction Service
Provides suggestions for plagiarism and AI content correction
"""
from typing import Dict, List, Optional
import os


def suggest_plagiarism_corrections(matches: List[Dict]) -> List[Dict]:
    """Generate correction suggestions for plagiarism matches"""

    corrections = []

    for match in matches:
        if match["similarity"] > 70:
            # High similarity - suggest citation
            corrections.append({
                "type": "citation",
                "severity": "high",
                "source": match["source"],
                "suggestion": f"Add citation: {match['source']}",
                "action": "cite",
                "details": "This passage appears to be directly copied. Add proper citation or quotation marks."
            })
        elif match["similarity"] > 40:
            # Medium similarity - suggest paraphrase or citation
            corrections.append({
                "type": "paraphrase",
                "severity": "medium",
                "source": match["source"],
                "suggestion": f"Paraphrase or cite: {match['source']}",
                "action": "rephrase",
                "details": "This passage is similar to existing work. Consider paraphrasing or adding citation."
            })

    return corrections


def suggest_ai_corrections(ai_score: float, ai_level: str) -> List[Dict]:
    """Generate correction suggestions for AI-detected content"""

    corrections = []

    if ai_score > 70:
        corrections.append({
            "type": "ai_humanization",
            "severity": "high",
            "suggestion": "Rewrite to add personal voice and variation",
            "action": "humanize",
            "details": "This text appears highly AI-generated. Add:\n"
                      "- Personal examples and experiences\n"
                      "- Varied sentence structures\n"
                      "- Natural transitions and connectors\n"
                      "- Domain-specific terminology"
        })
    elif ai_score > 40:
        corrections.append({
            "type": "ai_variation",
            "severity": "medium",
            "suggestion": "Add more sentence variation and personal touch",
            "action": "vary",
            "details": "Text shows AI characteristics. Consider:\n"
                      "- Varying sentence lengths\n"
                      "- Adding specific examples\n"
                      "- Using more active voice"
        })

    return corrections


def apply_ai_correction(text: str, correction_type: str) -> Optional[str]:
    """
    Apply correction using Claude via AWS Bedrock or Groq as fallback.

    Args:
        text: Text to correct
        correction_type: Type of correction (cite, rephrase, humanize, vary)

    Returns:
        Corrected text or None
    """

    prompts = {
        "cite": f"Add proper academic citations to this text:\n\n{text}",
        "rephrase": f"Rephrase this text to make it original while keeping the meaning:\n\n{text}",
        "humanize": f"Rewrite this text to sound more natural and human, with varied sentence structures:\n\n{text}",
        "vary": f"Improve this text by adding sentence variation and personal voice:\n\n{text}"
    }
    prompt = prompts.get(correction_type, prompts["humanize"])

    # Try Claude via Bedrock first
    bedrock_token = os.getenv("AWS_BEARER_TOKEN_BEDROCK")
    if bedrock_token:
        try:
            import httpx
            import json
            import base64

            region = os.getenv("AWS_REGION", "us-east-1")
            model = os.getenv("AWS_BEDROCK_MODEL", "us.anthropic.claude-sonnet-4-6-v1")
            url = f"https://bedrock-runtime.{region}.amazonaws.com/model/{model}/invoke"

            body = json.dumps({
                "anthropic_version": "bedrock-2023-05-31",
                "max_tokens": 1024,
                "messages": [
                    {"role": "user", "content": prompt}
                ],
                "system": "You are a helpful academic writing assistant. Respond only with the corrected text, no explanations."
            })

            headers = {
                "Content-Type": "application/json",
                "Authorization": f"Bearer {bedrock_token}",
            }

            response = httpx.post(url, content=body, headers=headers, timeout=30.0)
            if response.status_code == 200:
                data = response.json()
                return data["content"][0]["text"]
        except Exception as e:
            print(f"Bedrock error: {e}")

    # Fallback to Groq
    groq_api_key = os.getenv("GROQ_API_KEY")
    if groq_api_key:
        try:
            from openai import OpenAI

            client = OpenAI(
                api_key=groq_api_key,
                base_url="https://api.groq.com/openai/v1"
            )

            response = client.chat.completions.create(
                model="llama3-8b-8192",
                messages=[
                    {"role": "system", "content": "You are a helpful academic writing assistant. Respond only with the corrected text."},
                    {"role": "user", "content": prompt}
                ],
                temperature=0.7,
                max_tokens=1024
            )

            return response.choices[0].message.content
        except Exception as e:
            print(f"Groq error: {e}")

    return None


def generate_correction_report(plagiarism_matches: List[Dict], ai_result: Dict) -> Dict:
    """Generate complete correction report"""

    plagiarism_corrections = suggest_plagiarism_corrections(plagiarism_matches)
    ai_corrections = suggest_ai_corrections(ai_result["ai_score"], ai_result["ai_level"])

    return {
        "total_corrections": len(plagiarism_corrections) + len(ai_corrections),
        "plagiarism_corrections": plagiarism_corrections,
        "ai_corrections": ai_corrections,
        "contact": {
            "email": "checkone076@gmail.com",
            "phone": "+237690895735",
            "message": "Need help with corrections? Contact us!"
        }
    }
