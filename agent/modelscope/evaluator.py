import time


def evaluate_answer(
    answer: str,
    expected_topics: list[str],
    latency_sec: float,
):

    answer_lower = answer.lower()

    matched_topics = []

    for topic in expected_topics:

        topic_words = topic.lower().split()

        if any(
            word in answer_lower
            for word in topic_words
        ):
            matched_topics.append(topic)

    grounding_score = round(
        len(matched_topics)
        / len(expected_topics),
        2,
    )

    missing_topics = [
        topic
        for topic in expected_topics
        if topic not in matched_topics
    ]

    hallucination_risk = (
        "low"
        if grounding_score >= 0.8
        else "medium"
        if grounding_score >= 0.5
        else "high"
    )

    return {
        "grounding_score":
            grounding_score,

        "matched_topics":
            matched_topics,

        "missing_topics":
            missing_topics,

        "latency_sec":
            round(latency_sec, 2),

        "hallucination_risk":
            hallucination_risk,
    }