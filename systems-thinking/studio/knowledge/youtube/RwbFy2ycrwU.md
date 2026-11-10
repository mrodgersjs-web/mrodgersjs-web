---
source: https://www.youtube.com/watch?v=RwbFy2ycrwU
video_id: RwbFy2ycrwU
channel: Optimized AI Conference
title: "Beyond Orchestration: An Open Source Architecture for Agentic Systems - Ashok Prakash"
scraped: 2026-08-28
tags: [ai-agents, safety, open-source, governance]
---
# Beyond Orchestration: An Open Source Architecture for Agentic Systems - Ashok Prakash

Ashok Prakash presents an open-source reference architecture for making agentic systems safe, reliable, and trustworthy by surrounding the orchestration layer with durable execution, controlled inference, contracted tools, policy enforcement, artifact signing, and closed-loop observability.

## Procedure / models distilled
- Treat the agent controller as a durable execution environment (e.g., Temporal or Celery) where each step is checkpointed, conditional, and retry-safe.
- Bound every agent run with token/cost budgets to prevent runaway retries and surprise inference bills.
- Add a dedicated serving layer (KServe, RayServe, vLLM, SGLang) with LLM-specific optimizations, batching, autoscaling, and GPU memory awareness.
- Expose capabilities to agents as contracted tools/services with explicit scope, purpose, and data restrictions rather than open-ended APIs.
- Run agents in a bounded loop: evaluate outputs, observe, retry until safe, then act.
- Sign and version every artifact (models, tools, datasets) after evaluation and red-teaming so only approved artifacts enter inference.
- Encode guardrails as structured policy-as-code (e.g., Open Policy Agent) instead of relying on ambiguous natural-language instructions.
- Apply a safety checklist covering consent tracking, PII sensitivity, bias risk, and auditability/tracing.
- Implement data-access and PII-reduction policies at the tool boundary, tracing each redaction to avoid losing needed context.
- Mitigate latency/cost overhead from safety components with caching, serving-layer optimization, and right-sized models.
- Bake safety into CI/CD using shadow mode, canaries, and regular triage to catch silent drift and unbounded agents.

## Failure modes named
- Unsafe actions that ignore user preferences, project scope, or broader context.
- Cost overruns from unbounded retries and uncontrolled token consumption.
- Black-box decisions where intermediate steps are invisible.
- Silent drift: high initial success rate masks gradual failure over time.
- Tools accessing PII or data beyond their defined contract.
- Ambiguous English-language policies that agents interpret inconsistently.
- Shadow agents running without clear need or visibility.
- Over-redaction that strips context required for the task.
- Deep fan-out orchestration becoming unmanageable beyond one-to-three depth.
- Treating the agent demo as production-ready while neglecting safety plumbing.

## Studio relevance
03 diagnose - use the reference architecture as a checklist to map where a demo agent stack lacks durable execution, policy enforcement, and observability before production.
