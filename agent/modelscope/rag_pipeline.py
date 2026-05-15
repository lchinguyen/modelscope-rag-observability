from dotenv import load_dotenv
load_dotenv()

import sys
import json
import time
from pathlib import Path

sys.path.append(str(Path(__file__).resolve().parents[2]))

from agent.instrumentation import setup_tracing
setup_tracing()

from llama_index.core import VectorStoreIndex, SimpleDirectoryReader, Settings
from llama_index.core.node_parser import SentenceSplitter
from llama_index.embeddings.huggingface import HuggingFaceEmbedding
from llama_index.llms.google_genai import GoogleGenAI
from long_context_analyzer import analyze_long_context_degradation

from config import (
    USE_MOCK_MODE,
    MODEL_NAME,
    DOCS_PATH,
    BENCHMARK_PATH,
    DEFAULT_EXPERIMENT_CONFIGS,
)

from evaluator import evaluate_answer

from phoenix_evals import (
    compute_hallucination_risk,
    estimate_token_usage,
)

from context_efficiency_analyzer import analyze_context_efficiency

from optimizer import (
    generate_self_improvement_plan,
    generate_next_config,
)

from mock_llm import generate_mock_response
from experiment_store import save_experiment
from failure_taxonomy import classify_retrieval_failure


Settings.embed_model = HuggingFaceEmbedding(
    model_name="sentence-transformers/all-MiniLM-L6-v2"
)

Settings.llm = GoogleGenAI(
    model=MODEL_NAME,
)


def build_query_engine(chunk_size: int, top_k: int):
    documents = SimpleDirectoryReader(DOCS_PATH).load_data()

    splitter = SentenceSplitter(
        chunk_size=chunk_size,
        chunk_overlap=50,
    )

    nodes = splitter.get_nodes_from_documents(documents)
    index = VectorStoreIndex(nodes)

    return index.as_query_engine(similarity_top_k=top_k)


def run_experiment(config: dict) -> dict:
    query_engine = build_query_engine(
        chunk_size=config["chunk_size"],
        top_k=config["top_k"],
    )

    with Path(BENCHMARK_PATH).open("r") as f:
        benchmark_questions = json.load(f)

    question_results = []

    for item in benchmark_questions:
        question = item["question"]
        expected_topics = item["expected_topics"]

        start = time.time()

        try:
            if USE_MOCK_MODE:
                latency = time.time() - start
                answer = generate_mock_response(question)

                retrieved_chunks = [
                    (
                        "Mock retrieved context about GQA, KV-cache efficiency, "
                        "memory usage, inference latency, quantization, and RAG grounding."
                    )
                ]

            else:
                response = query_engine.query(question)
                latency = time.time() - start
                answer = str(response)

                retrieved_chunks = []

                if hasattr(response, "source_nodes"):
                    for node in response.source_nodes:
                        retrieved_chunks.append(node.text[:300])

            token_usage = estimate_token_usage(question + answer)

            eval_result = evaluate_answer(
                answer=answer,
                expected_topics=expected_topics,
                latency_sec=latency,
            )

            eval_result["hallucination_risk"] = compute_hallucination_risk(
                eval_result["grounding_score"]
            )

            eval_result["token_usage_estimate"] = token_usage

            context_analysis = analyze_context_efficiency(
                retrieved_chunks,
                answer,
            )

            failure_modes = classify_retrieval_failure({
                "eval": eval_result,
                "context_analysis": context_analysis,
                "retrieved_chunks": retrieved_chunks,
            })

        except Exception as e:
            latency = time.time() - start
            answer = f"ERROR: {e}"
            retrieved_chunks = []

            eval_result = {
                "grounding_score": 0,
                "matched_topics": [],
                "missing_topics": expected_topics,
                "latency_sec": round(latency, 2),
                "hallucination_risk": "unknown",
                "token_usage_estimate": 0,
            }

            context_analysis = {
                "total_chunk_tokens": 0,
                "useful_chunk_tokens": 0,
                "context_efficiency_ratio": 0,
                "redundant_chunks": 0,
                "recommendations": [
                    "Context analysis unavailable due to failed generation."
                ],
            }

            failure_modes = [
                "generation_or_runtime_error"
            ]

        question_results.append({
            "prompt": question,
            "question": question,
            "answer": answer,
            "retrieved_chunks": retrieved_chunks,
            "context_analysis": context_analysis,
            "failure_modes": failure_modes,
            "eval": eval_result,
        })

    avg_grounding = sum(
        r["eval"]["grounding_score"]
        for r in question_results
    ) / len(question_results)

    avg_latency = sum(
        r["eval"]["latency_sec"]
        for r in question_results
    ) / len(question_results)

    return {
        "config": config,
        "mode": "mock" if USE_MOCK_MODE else "gemini",
        "avg_grounding_score": round(avg_grounding, 2),
        "avg_latency_sec": round(avg_latency, 2),
        "question_results": question_results,
    }


def print_report(title: str, result: dict):
    print("\n" + "=" * 60)
    print(title)
    print("=" * 60)

    print("\nMODE:")
    print(result["mode"])

    print("\nCONFIG:")
    print(result["config"])

    print("\nSUMMARY:")
    print({
        "avg_grounding_score": result["avg_grounding_score"],
        "avg_latency_sec": result["avg_latency_sec"],
    })

    for r in result["question_results"]:
        print("\nQUESTION:")
        print(r["question"])

        print("\nPROMPT:")
        print(r["prompt"])

        print("\nANSWER:")
        print(r["answer"])

        print("\nRETRIEVED CHUNKS:")
        for chunk in r["retrieved_chunks"]:
            print("-" * 40)
            print(chunk)

        print("\nCONTEXT EFFICIENCY ANALYSIS:")
        print(r["context_analysis"])

        print("\nFAILURE MODES:")
        print(r["failure_modes"])

        print("\nEVAL:")
        print(r["eval"])
        
        print("\nLONG-CONTEXT ANALYSIS:")
        print(result.get("long_context_analysis"))


if __name__ == "__main__":
    all_results = []

    for config in DEFAULT_EXPERIMENT_CONFIGS:
        result = run_experiment(config)
        result["long_context_analysis"] = analyze_long_context_degradation(result)
        
        improvement_plan = generate_self_improvement_plan(result)
        next_config = generate_next_config(result)
        result["optimization_recommendations"] = improvement_plan
        result["adaptive_next_config"] = next_config
        save_experiment(result)
        
        all_results.append(result)

        title = (
            f"RUN: chunk={config['chunk_size']}, "
            f"top_k={config['top_k']}"
        )

        print_report(title, result)

        title = (
            f"RUN: chunk={config['chunk_size']}, "
            f"top_k={config['top_k']}"
        )

        print_report(title, result)

    improvement_plan = generate_self_improvement_plan(all_results[0])
    next_config = generate_next_config(all_results[0])

    print("\n" + "=" * 60)
    print("SELF-IMPROVEMENT PLAN")
    print("=" * 60)

    for item in improvement_plan:
        print("-", item)

    print("\nADAPTIVE NEXT CONFIG:")
    print(next_config)

    print("\n" + "=" * 60)
    print("MODEL SCOPE SUMMARY")
    print("=" * 60)

    for result in all_results:
        config = result["config"]

        print({
            "mode": result["mode"],
            "chunk_size": config["chunk_size"],
            "top_k": config["top_k"],
            "avg_grounding_score": result["avg_grounding_score"],
            "avg_latency_sec": result["avg_latency_sec"],
        })

    best_grounding = max(
        all_results,
        key=lambda r: r["avg_grounding_score"]
    )

    fastest = min(
        all_results,
        key=lambda r: r["avg_latency_sec"]
    )

    print("\nBEST GROUNDING CONFIG:")
    print(best_grounding["config"])

    print("\nFASTEST CONFIG:")
    print(fastest["config"])