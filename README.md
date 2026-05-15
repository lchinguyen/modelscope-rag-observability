# ModelScope: Research Platform for Retrieval Diagnostics and Context-Efficient RAG systems

ModelScope is a research-oriented observability and evaluation platform designed for LLM researchers to analyze, diagnose, and optimize inference optimization. This combine retrieval tracing, context efficiency analysis, retrieval failure diagnostics, long-context evaluation efficiency, and adaptive optimization to help researchers investigate how retrieval configurations influence grounding quality, latency, hallucination risk, token efficiency, and overall retrieval performance in modern large language model pipelines. focuses on:


Built for the Arize @ Google Cloud Partnerships Hackathon track: https://rapid-agent.devpost.com/


> Build Gemini Agents with Full Observability and Self-Introspection via MCP

The project combines:
- Gemini-powered RAG runtime
- Arize Phoenix tracing
- OpenInference instrumentation
- Phoenix MCP introspection
- Retrieval diagnostics
- Context efficiency analysis
- Long-context degradation analysis
- Self-improvement optimization
- Experiment tracking dashboard

---

# Core Features

## 1. Phoenix Observability

The system traces:
- prompts
- retrieved chunks
- answers
- latency
- token usage estimates
- grounding scores
- hallucination risk

using:
- OpenInference
- Arize Phoenix

---

## 2. Phoenix MCP Introspection

Gemini CLI can query Phoenix traces directly through MCP.

Example runtime introspection:

```text
Which runs had weak grounding?
Which traces showed noisy retrieval?
Which retrieval settings caused high latency?
```

---

## 3. Context Efficiency Analysis

Measures:
- total retrieved context tokens
- useful retrieved context tokens
- redundant retrieval chunks
- context efficiency ratio

Designed for:
- long-context LLM analysis
- token efficiency research
- retrieval optimization

---

## 4. Retrieval Failure Intelligence

Detects:
- low grounding
- redundant retrieval
- noisy retrieval
- retrieval omission
- hallucinated synthesis

Then generates:
- retrieval diagnostics
- optimization recommendations
- adaptive next retrieval config

---

## 5. Long-Context Degradation Analysis

Analyzes whether increasing retrieval context improves or degrades answer quality.

Tracks:
- context window size
- retrieval efficiency
- degradation risk
- context dilution

---

## 6. Self-Improvement Optimization Loop

ModelScope uses evaluation and observability signals from previous experiments to improve and recommend retrieval improvements over time.

After each experiment run, the optimizer analyzes:
- grounding quality
- latency
- hallucination risk
- context efficiency
- retrieval failure patterns

then generate adaptive recommendations such as:
- increasing chunk size to preserve missing context
- reducing chunk size to lower latency
- adjusting top-k retrieval to reduce noisy or redundant context
- applying stricter grounded prompting when hallucination risk is high

---

## 7. Experiment Tracking Dashboard

Experiments are stored in:

```text
results/experiments.json
```

and compared using:

```bash
PYTHONPATH=. uv run python agent/modelscope/comparison_dashboard.py
```

The dashboard compares:
- chunk size
- top-k
- grounding score
- latency
- recommendations
- adaptive next configs

---

# Architecture

```text
User Query
   ↓
RAG Pipeline
   ↓
Gemini Runtime / Mock Runtime
   ↓
Phoenix Tracing
   ↓
Evaluation Engine
   ↓
Context Efficiency Analyzer
   ↓
Retrieval Failure Intelligence
   ↓
Long-Context Degradation Analysis
   ↓
Self-Improvement Optimizer
   ↓
Experiment Tracking Dashboard
```

---

# Project Structure

```text
agent/modelscope/
  comparison_dashboard.py
  config.py
  context_efficiency_analyzer.py
  evaluator.py
  experiment_store.py
  failure_taxonomy.py
  long_context_analyzer.py
  mock_llm.py
  optimizer.py
  phoenix_evals.py
  rag_pipeline.py

data/
  benchmark_questions.json
  docs/

results/
  example_experiments.json
```

---
## Demo Workflow 

# 1. Reproducible Offline Research Mode

Designed for:
- reproducibility
- open-source testing
- permanent research usage

In:

```text
agent/modelscope/config.py
```

set:

```python
USE_MOCK_MODE = True
```

Run:

```bash
PYTHONPATH=. uv run python agent/modelscope/rag_pipeline.py
```

Then launch dashboard:

```bash
PYTHONPATH=. uv run python agent/modelscope/comparison_dashboard.py
```

This mode still runs:
- retrieval diagnostics
- grounding evaluation
- context efficiency analysis
- failure taxonomy
- optimization recommendations
- experiment tracking

without requiring Gemini API calls.

---

# 2. Live Gemini + Phoenix Mode for Google Cloud Rapid Agent Hackathon

Designed for:
- real tracing
- production observability
- hackathon demos

In:

```text
agent/modelscope/config.py
```

set:

```python
USE_MOCK_MODE = False
```

Run:

```bash
PYTHONPATH=. uv run python agent/modelscope/rag_pipeline.py
```

Then inspect traces inside Phoenix Cloud.

This mode enables:
- real Gemini inference
- real Phoenix traces
- MCP introspection over live traces

---

# Setup

## 1. Clone repository

```bash
git clone https://github.com/lchinguyen/modelscope-rag-observability.git

cd modelscope-rag-observability
```

---

## 2. Install dependencies

```bash
uv sync
```

---

## 3. Configure environment variables

Copy:

```bash
cp .env.example .env
```

Fill in:

```env
GOOGLE_API_KEY=your_google_api_key

PHOENIX_API_KEY=your_phoenix_api_key

PHOENIX_COLLECTOR_ENDPOINT=https://app.phoenix.arize.com/s/your-space-name

PHOENIX_PROJECT_NAME=gemini-hackathon
```

---

# Arize Track Alignment

ModelScope satisfies the Arize track by implementing:

- Gemini-powered runtime
- code-owned observability pipeline
- OpenInference instrumentation
- Phoenix tracing
- Phoenix MCP introspection
- code-based evaluations
- self-improvement recommendations
- experiment tracking
- retrieval diagnostics
