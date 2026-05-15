from experiment_store import load_experiments


def print_experiment_dashboard() -> None:
    experiments = load_experiments()

    if not experiments:
        print("No experiments found.")
        return

    print("\n" + "=" * 70)
    print("MODEL SCOPE EXPERIMENT DASHBOARD")
    print("=" * 70)

    for exp in experiments[-10:]:
        config = exp["config"]

        print({
            "timestamp": exp.get("timestamp"),
            "chunk_size": config.get("chunk_size"),
            "top_k": config.get("top_k"),
            "avg_grounding": exp.get("avg_grounding_score"),
            "avg_latency": exp.get("avg_latency_sec"),
            "recommendations": exp.get("optimization_recommendations"),
            "next_config": exp.get("adaptive_next_config"),
        })


if __name__ == "__main__":
    print_experiment_dashboard()