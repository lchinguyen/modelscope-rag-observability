def compute_hallucination_risk(grounding_score: float):

    if grounding_score >= 0.8:
        return "low"

    if grounding_score >= 0.5:
        return "medium"

    return "high"


def estimate_token_usage(text: str):

    return int(len(text.split()) * 1.3)