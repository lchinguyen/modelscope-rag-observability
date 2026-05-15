import json
from pathlib import Path

import pandas as pd
import streamlit as st


RESULTS_PATH = Path("results/experiments.json")
EXAMPLE_PATH = Path("results/example_experiments.json")


st.set_page_config(
    page_title="GroundTruth Dashboard",
    layout="wide",
)

st.title("GroundTruth")
st.subheader("Retrieval Diagnostics and Observability Dashboard")


def load_experiments():
    path = RESULTS_PATH if RESULTS_PATH.exists() else EXAMPLE_PATH

    if not path.exists():
        return []

    with path.open("r") as f:
        return json.load(f)


experiments = load_experiments()

if not experiments:
    st.warning("No experiment results found. Run rag_pipeline.py first.")
    st.stop()


rows = []

for exp in experiments:
    config = exp.get("config", {})

    rows.append({
        "mode": exp.get("mode"),
        "chunk_size": config.get("chunk_size"),
        "top_k": config.get("top_k"),
        "grounding": exp.get("avg_grounding_score"),
        "latency": exp.get("avg_latency_sec"),
        "recommendations": exp.get("optimization_recommendations"),
        "next_config": exp.get("adaptive_next_config"),
    })

df = pd.DataFrame(rows)

st.markdown("## Experiment Summary")
st.dataframe(df, use_container_width=True)

col1, col2, col3 = st.columns(3)

latest = experiments[-1]

col1.metric("Latest Grounding Score", latest.get("avg_grounding_score"))
col2.metric("Latest Latency", latest.get("avg_latency_sec"))
col3.metric("Mode", latest.get("mode"))

st.markdown("## Grounding vs Latency")

st.line_chart(
    df[["grounding", "latency"]]
)

st.markdown("## Latest Experiment Details")

for idx, item in enumerate(latest.get("question_results", []), start=1):
    with st.expander(f"Question {idx}: {item.get('question')}"):
        st.markdown("### Prompt")
        st.write(item.get("prompt"))

        st.markdown("### Answer")
        st.write(item.get("answer"))

        st.markdown("### Retrieved Chunks")
        for chunk in item.get("retrieved_chunks", []):
            st.code(chunk)

        st.markdown("### Context Efficiency Analysis")
        st.json(item.get("context_analysis"))

        st.markdown("### Failure Modes")
        st.write(item.get("failure_modes"))

        st.markdown("### Evaluation")
        st.json(item.get("eval"))

st.markdown("## Self-Improvement Recommendations")
st.write(latest.get("optimization_recommendations"))

st.markdown("## Adaptive Next Config")
st.json(latest.get("adaptive_next_config"))