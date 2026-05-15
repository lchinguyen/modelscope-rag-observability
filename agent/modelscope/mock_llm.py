def generate_mock_response(question: str) -> str:
    q = question.lower()

    if "grouped-query attention" in q:
        return (
            "Grouped-query attention improves KV-cache efficiency, "
            "reduces memory usage, and improves inference latency."
        )

    if "quantization" in q:
        return (
            "Quantization improves LLM inference using INT8 and INT4 "
            "compression to reduce memory and latency."
        )

    if "rag" in q:
        return (
            "RAG reduces hallucination by grounding generation in "
            "retrieved external knowledge."
        )

    return "Mock offline response for reproducible research evaluation."