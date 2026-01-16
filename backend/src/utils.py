from typing import Any, Dict


def safe_strip(text: str) -> str:
    """
    Safely strip a string. If None comes, return empty string.
    """
    if not text:
        return ""
    return text.strip()


def build_response(
    input_text: str,
    prediction: str,
    confidence: float,
    keywords: list,
    factchecks: list
) -> Dict[str, Any]:
    
    return {
        "input": input_text,
        "prediction": prediction,
        "confidence": confidence,
        "keywords": keywords or [],
        "factchecks": factchecks or []
    }
