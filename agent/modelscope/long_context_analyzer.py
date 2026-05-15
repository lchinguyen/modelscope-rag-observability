def analyze_long_context_degradation(result: dict):
    analyses = []

    for item in result["question_results"]:
        context = item["context_analysis"]

        total_tokens = context["total_chunk_tokens"]
        efficiency = context["context_efficiency_ratio"]

        if total_tokens < 500:
            context_class = "short_context"
        elif total_tokens < 2000:
            context_class = "medium_context"
        elif total_tokens < 8000:
            context_class = "long_context"
        else:
            context_class = "very_long_context"

        degradation_risk = "low"

        if context_class in ["long_context", "very_long_context"] and efficiency < 0.3:
            degradation_risk = "high"
        elif context_class == "medium_context" and efficiency < 0.3:
            degradation_risk = "medium"

        analyses.append({
            "question": item["question"],
            "context_class": context_class,
            "total_context_tokens": total_tokens,
            "context_efficiency_ratio": efficiency,
            "degradation_risk": degradation_risk,
        })

    return analyses