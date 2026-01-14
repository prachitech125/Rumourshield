from typing import Dict, Any, List


def simple_rumour_signal(cleaned_text: str) -> Dict[str, Any]:
    """
    Beginner-friendly heuristic (not ML):
    Gives a 'risk score' based on suspicious words.
    """
    suspicious_words = [
        "shocking", "breaking", "must share", "forward", "viral",
        "secret", "exposed", "cure", "guaranteed", "100%",
        "proof", "government", "warning"
    ]

    score = 0
    matched = []

    for w in suspicious_words:
        if w in cleaned_text:
            score += 1
            matched.append(w)

    # Convert score to simple label
    if score >= 3:
        label = "Likely Rumour"
    elif score == 0:
        label = "Low Risk"
    else:
        label = "Needs Verification"

    confidence = min(0.95, 0.35 + (score * 0.15))

    return {
        "label": label,
        "confidence": round(confidence, 2),
        "matched_keywords": matched
    }


def extract_factcheck_results(api_response: Dict[str, Any]) -> List[Dict[str, str]]:
    """
    Extracts top fact check sources from API response.
    """
    results = []

    if not api_response or "claims" not in api_response:
        return results

    for claim in api_response["claims"]:
        text = claim.get("text", "Unknown claim")
        claim_reviews = claim.get("claimReview", [])

        for review in claim_reviews[:2]:  # top 2 reviews
            results.append({
                "claim": text,
                "publisher": review.get("publisher", {}).get("name", "Unknown"),
                "rating": review.get("textualRating", "Unknown"),
                "url": review.get("url", "N/A")
            })

    return results
