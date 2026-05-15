def generate_self_improvement_plan(result: dict) -> list[str]:
    recommendations = []

    avg_grounding = result["avg_grounding_score"]
    avg_latency = result["avg_latency_sec"]

    for r in result["question_results"]:
        context_ratio = r["context_analysis"]["context_efficiency_ratio"]

        if context_ratio < 0.3:
            recommendations.append("Reduce top_k to remove noisy retrieval.")

        if avg_grounding < 0.5:
            recommendations.append("Increase chunk_size to preserve context.")

        if avg_latency > 3:
            recommendations.append("Reduce chunk_size for lower latency.")

    if not recommendations:
        recommendations.append("Current retrieval pipeline appears stable.")

    return list(set(recommendations))


def generate_next_config(result: dict) -> dict:
    config = result["config"].copy()

    avg_grounding = result["avg_grounding_score"]
    avg_latency = result["avg_latency_sec"]

    context_ratios = [
        r["context_analysis"]["context_efficiency_ratio"]
        for r in result["question_results"]
    ]

    avg_context_ratio = sum(context_ratios) / len(context_ratios)

    if avg_context_ratio < 0.3:
        config["top_k"] = max(1, config["top_k"] - 1)

    if avg_grounding < 0.5:
        config["chunk_size"] = min(1500, config["chunk_size"] + 256)

    if avg_latency > 3:
        config["chunk_size"] = max(256, config["chunk_size"] - 256)

    return config