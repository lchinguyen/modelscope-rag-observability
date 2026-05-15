def classify_retrieval_failure(result: dict) -> list[str]:
    failures = []

    eval_result = result["eval"]
    context = result["context_analysis"]
    retrieved_chunks = result["retrieved_chunks"]

    if eval_result["grounding_score"] < 0.5:
        failures.append("low_grounding")

    if context["redundant_chunks"] > 0:
        failures.append("redundant_retrieval")

    if context["context_efficiency_ratio"] < 0.3:
        failures.append("context_dilution")

    if len(retrieved_chunks) == 0:
        failures.append("retrieval_omission")

    if eval_result.get("hallucination_risk") == "high":
        failures.append("hallucinated_synthesis")

    if len(failures) == 0:
        failures.append("no_major_failure_detected")

    return failures