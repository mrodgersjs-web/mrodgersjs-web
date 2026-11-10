---
source: https://www.youtube.com/watch?v=3XCunZqvVDA
video_id: 3XCunZqvVDA
channel: Alex Ziskind
title: "THIS is the REAL DEAL 🤯 for local LLMs"
scraped: 2026-08-28
tags: [tools, local llms, docker, vllm, quantization]
---
# THIS is the REAL DEAL 🤯 for local LLMs

The video demonstrates how to get high-throughput local LLM code completion by moving from single-request desktop tools to a Docker-backed serving stack using vLLM and FP8 quantization on NVIDIA GPUs.

## Procedure / models distilled
- Use Docker Model Runner to serve local LLMs with GPU support and configurable concurrency through a Docker Compose `docker model` section.
- Run vLLM inside a Docker container with NVIDIA GPU passthrough to handle many concurrent requests and saturate the GPU.
- Select fill-in-the-middle coding models such as Qwen 3 Coder 30B for code-completion and autocomplete scenarios.
- Set runtime flags in Docker Model Runner to define how many parallel requests the model can answer simultaneously.
- Use FP8 floating-point quantization on supported NVIDIA GPUs to shrink model weights and unlock native tensor-core speedups.
- Benchmark with increasing concurrency to verify aggregate throughput scales instead of merely queuing requests.
- Compare serving options: LM Studio is UI-friendly but serializes requests, Ollama supports some parallelism, and Docker + vLLM scales far higher.
- Co-deploy the model runner alongside application services in Docker Compose so the app and its LLM share one orchestrated environment.
- Pass all available GPUs into the inference container when launching vLLM via Docker to maximize compute utilization.
- Recognize platform quantization differences: macOS relies on GGUF, Safetensors, and MLX, while NVIDIA GPUs natively support FP8 and FP4.

## Failure modes named
- LM Studio queues concurrent requests one at a time, so adding users does not increase aggregate tokens-per-second throughput.
- Assuming a single user only needs one request at a time ignores code-completion workloads that flood the backend with many simultaneous prompts.
- Running a normal Docker container without GPU passthrough and runtime flags leaves the model unable to use the GPU.
- Serving unquantized BF16 weights on NVIDIA hardware misses the large speedups available from native FP8/FP4 tensor-core formats.
- Applying FP8 guidance to consumer AMD GPUs fails because FP8 native support is limited to AMD Instinct server cards, not consumer cards.
- Relying on macOS for local inference gives fast per-request latency but poor parallelism and limited model/quantization format support.

## Studio relevance
04 leverage - use this card to choose and configure a GPU-saturated local LLM serving stack when building high-throughput coding assistants or agentic tools.
