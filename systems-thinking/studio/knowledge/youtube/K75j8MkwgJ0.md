---
source: https://www.youtube.com/watch?v=K75j8MkwgJ0
video_id: K75j8MkwgJ0
channel: unknown
title: "Optimize Your AI - Quantization Explained"
scraped: 2026-08-28
tags: [engineering, quantization, ai-inference, ollama, memory-optimization]
---
# Optimize Your AI - Quantization Explained

The video explains quantization as a precision-reduction technique that shrinks AI model weights and context caches, enabling large models to run on modest hardware with practical trade-offs.

## Procedure / models distilled
- AI models are billions of floating-point parameters; full 32-bit precision stores ~4 bytes per parameter, so a 7B model needs ~28 GB of RAM just to hold its weights.
- Quantization reduces the numeric precision per weight (e.g., Q8, Q4, Q2) to compress model size and RAM/VRAM usage at the cost of some accuracy.
- Think of Q8, Q4, and Q2 as rulers with coarser markings: Q8 is centimeter-level, Q4 is roughly every 5 cm, and Q2 is a rough stick—each smaller format saves more space but retains less precision.
- Standard uniform quantization forces every value into a fixed set of buckets, which wastes precision when numbers cluster in different ranges.
- K-quant (KQ) in Ollama creates multiple specialized ranges: small weights get fine-grained buckets, large weights get coarse buckets, improving accuracy for a given size.
- K-quant variants K_S, K_M, and K_L denote small, medium, and large levels of detail in the recovery metadata that records how the model was arranged.
- A practical example shows a Q4_K_M quantized Qwen 2.5 7B model taking only ~4.7 GB on disk.
- Context quantization is a separate process that compresses the key-value conversation cache, not the model weights themselves.
- Long-context models can consume massive memory; extending Qwen 2.5 from 2K to 32K tokens raised context memory from ~2 GB to ~15 GB in the demo.
- Enabling Flash Attention (`ollama flash_attention=true`) can dramatically reduce key-value cache memory.
- Setting KV cache quantization to F16 or Q8 further shrinks context memory; in the demo, Q8 dropped the 32K context from ~40.9 GB to ~30.6 GB.
- Start with a Q4 model, especially Q4_K_M, as the default balance of size and quality.
- If output quality degrades, move up to Q8 or FP16; if a Q4 model works well, try Q2 for maximum RAM savings.
- Test per model and workload because newer models can respond differently to Flash Attention and KV cache quantization, and some configurations may increase memory use instead of reducing it.

## Failure modes named
- Treating full FP32 precision as the only option, which inflates RAM/VRAM costs and prevents local inference on normal hardware.
- Forcing all numeric ranges through one fixed quantization grid, which wastes precision where weights cluster.
- Assuming Flash Attention and KV cache quantization always reduce memory; one newer model in the demo used more memory with Q8 KV cache than without it.
- Picking the lowest quantization (Q2) blindly and accepting unacceptable output quality without testing.
- Ignoring context memory by focusing only on weight quantization while letting long conversation histories consume most of the RAM.

## Studio relevance
04 leverage - use quantization and KV-cache compression to fit bigger models and longer contexts on existing hardware.
