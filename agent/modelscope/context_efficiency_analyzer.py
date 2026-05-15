def analyze_context_efficiency(
    retrieved_chunks,
    answer,
):

    total_chunk_tokens = 0
    useful_chunk_tokens = 0

    answer_words = set(
        answer.lower().split()
    )

    redundant_chunks = 0

    seen_chunks = set()

    for chunk in retrieved_chunks:

        chunk_words = chunk.lower().split()

        total_chunk_tokens += len(
            chunk_words
        )

        overlap = [
            word
            for word in chunk_words
            if word in answer_words
        ]

        useful_chunk_tokens += len(
            overlap
        )

        chunk_signature = " ".join(
            chunk_words[:20]
        )

        if chunk_signature in seen_chunks:
            redundant_chunks += 1

        seen_chunks.add(
            chunk_signature
        )

    if total_chunk_tokens == 0:
        efficiency_ratio = 0

    else:
        efficiency_ratio = round(
            useful_chunk_tokens
            / total_chunk_tokens,
            2,
        )

    recommendations = []

    if efficiency_ratio < 0.3:
        recommendations.append(
            "Large amount of retrieved context may be unused."
        )

    if redundant_chunks > 0:
        recommendations.append(
            "Redundant retrieval chunks detected."
        )

    if efficiency_ratio > 0.7:
        recommendations.append(
            "Retrieved context appears highly relevant."
        )

    return {
        "total_chunk_tokens":
            total_chunk_tokens,

        "useful_chunk_tokens":
            useful_chunk_tokens,

        "context_efficiency_ratio":
            efficiency_ratio,

        "redundant_chunks":
            redundant_chunks,

        "recommendations":
            recommendations,
    }