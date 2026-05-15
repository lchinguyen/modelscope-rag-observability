USE_MOCK_MODE = True
# for demo use USE_MOCK_MODE = False

MODEL_NAME = "gemini-2.5-flash" 

DOCS_PATH = "data/docs"

BENCHMARK_PATH = "data/benchmark_questions.json"

RESULTS_PATH = "results/experiments.json"

DEFAULT_EXPERIMENT_CONFIGS = [
    {
        "chunk_size": 512,
        "top_k": 3,
    },
    {
        "chunk_size": 1000,
        "top_k": 5,
    },
]