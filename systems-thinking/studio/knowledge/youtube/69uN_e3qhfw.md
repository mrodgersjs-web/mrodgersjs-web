---
source: https://www.youtube.com/watch?v=69uN_e3qhfw
video_id: 69uN_e3qhfw
channel: Tonbi's AI Garage
title: "I Built an Open-Source Local AI Video Studio for OpenRouter Models"
scraped: 2026-08-28
tags: [tools, local-first, openrouter, video-generation]
---
# I Built an Open-Source Local AI Video Studio for OpenRouter Models

A developer builds a minimal, local-first, open-source web studio that lets users add an OpenRouter API key, browse video models, generate videos, and compare results from multiple providers in one place.

## Procedure / models distilled
- Start by scoping a focused "video workbench" rather than a full creative suite to keep the project small and forkable.
- Use OpenRouter's unified video API to access multiple providers (Google Veo, Kling, MiniMax, Sora, Seedance, etc.) through a single key.
- Store the OpenRouter API key locally only, keeping it out of cloud services, Docker, or hosted platforms.
- Scaffold a local desktop web app with a model browser, generation form, async job tracker, local gallery, and side-by-side comparison view.
- Pull current model capabilities from the OpenRouter docs and expose them as simple filterable options in the UI.
- Submit single video generation jobs asynchronously by selecting model, prompt, duration, resolution, and audio toggle, then save completed outputs locally.
- Display an estimated cost panel before generation based on model pricing, duration, resolution, and audio so users see the price up front.
- Run multi-model batch generation from a single prompt across up to three selected models to compare how different providers interpret the same request.
- Filter duration, resolution, and other options in a batch to only values supported by all selected models to prevent rejected jobs.
- Attach reference media such as an image to a prompt for image-to-video or style-consistent generation.
- Review results in a comparison viewer that plays outputs side by side so you can pick the best model for the prompt.
- Catch provider-specific errors like "duration not supported" and use them to constrain the available parameter choices.
- Keep the UI lightweight and dark-themed rather than adding heavy features, leaving room for future MCP/CPSC integrations.

## Failure modes named
- Over-building the tool into a bloated creative suite instead of a clean, focused local workbench.
- Storing or transmitting the API key through cloud or hosted platforms instead of keeping it on local files.
- Running multi-model batches without checking each model's supported durations and resolutions, causing job conflicts.
- Assuming all video models share the same parameter limits, leading to rejected generation requests.
- Generating without checking the estimated cost first and accidentally spending more credits than intended.
- Comparing outputs with mismatched dimensions, which makes side-by-side previews look distorted.

## Studio relevance
04 leverage - use OpenRouter as a single API gateway to run, save, and compare multiple local video-generation models without external dependencies.
