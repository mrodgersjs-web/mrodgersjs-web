---
source: https://www.youtube.com/watch?v=B18zBnjZKmc
video_id: B18zBnjZKmc
channel: Caleb Writes Code
title: "Why Inference is hard.."
scraped: 2026-08-28
tags: [engineering, inference, quantization, memory-hierarchy, llms]
---
# Why Inference is hard..

Loading and serving a local LLM is not as simple as running an executable; it requires navigating memory hierarchy limits, choosing an inference engine with the right load/serve trade-offs, and applying the appropriate quantization strategy for the target hardware.

## Procedure / models distilled
- Treat downloaded model files as build artifacts, not executables: the artifacts include weights, architecture config, and tokenizer data that an inference engine must operationalize.
- Use the memory hierarchy deliberately: model weights typically move from SSD to RAM to CPU/VRAM/GPU, and each hop has different bandwidth, capacity, and latency characteristics.
- Split a model across memory tiers so weights can stay partly in RAM while the accelerator handles portions of the compute when the full model does not fit in VRAM.
- Use memory-mapped I/O (mmap) for lazy, OS-managed loading: weights are logically mapped from SSD and paged into RAM only when needed, avoiding an eager full copy.
- Treat mmap eviction as a trade-off: if weights are evicted from RAM, the OS reloads them from SSD; for a 15 GB model, reloading ~5% over a PCIe 4 NVMe link at ~7 GB/s adds roughly 100 ms.
- Choose an inference engine based on its load/serve strategy, not its language: language overhead is usually secondary to compilation, import, scheduling, and concurrency design choices.
- Shrink model footprint by lowering weight precision from BF16 to INT4/INT8/FP8, accepting a quality/compression trade-off.
- Apply grouped quantization with per-group scale and zero-point/bias: quantize blocks of weights using a local scale so the original values can be approximately reconstructed at inference.
- Pick symmetric quantization when the weight distribution is centered, and asymmetric quantization with a bias when it is not, improving reconstruction for non-centered groups.
- Use K-quants to add hierarchical scaling and mixed precision: a 256-weight block gets an outer scale while inner 32-weight groups keep finer scales, and more sensitive layers receive higher precision.
- Use activation-aware quantization (AWQ) to protect salient weights: run calibration data, identify weights with large activation magnitudes, and scale them to reduce reconstruction error.
- Use error-driven mixed-precision quantization (EXL2/EXL3) to assign higher precision to high-error groups and lower precision to low-error groups, using Hessian-based sensitivity.
- Match quantization formats to hardware capabilities: FP8 is native on Hopper, NVFP4 is native on Blackwell, while general formats like GGUF prioritize broad consumer hardware.

## Failure modes named
- Assuming an inference engine’s speed is determined by its implementation language rather than its scheduling, concurrency, and load-time strategy.
- Eagerly duplicating model weights during load, which wastes temporary RAM before the final copy is retained.
- Treating a downloaded model as a runnable executable that can be launched directly.
- Applying uniform round-to-nearest quantization without grouping or scaling, causing severe accuracy loss as values are rounded into a tiny integer grid.
- Ignoring memory-hierarchy constraints when planning model serving, leading to unexpected reload latency or out-of-memory errors.
- Picking an engine for raw inference throughput without accounting for long initialization and import overheads that affect time-to-first-token.
- Quantizing all layers with the same bit width, missing that embeddings, attention, normalization, and feed-forward layers have different sensitivity to precision loss.
- Using hardware-specific formats like FP8 or NVFP4 without the required GPU architecture, causing unsupported or degraded execution.

## Studio relevance
04 leverage - use this card when selecting an inference engine, quantization format, and memory-loading strategy to fit a model into available hardware and minimize time-to-first-token.
