---
source: https://www.youtube.com/watch?v=A2PfSnYl-u8
video_id: A2PfSnYl-u8
channel: unknown
title: "Stop AI From Guessing: Accurate Infographics with Gemini & NotebookLM"
scraped: 2026-08-28
tags: [tools, ai-generated-images, infographics, hallucination, fact-checking]
---
# Stop AI From Guessing: Accurate Infographics with Gemini & NotebookLM

A practical guide to producing infographics with Gemini and NotebookLM while controlling for the image generator's tendency to hallucinate technical details.

## Procedure / models distilled
- Use Gemini's "thinking" or "pro" mode instead of "fast" for noticeably better infographic results.
- For well-known general topics, simple prompts work reliably because the model has broad accurate training data.
- For technical subjects, specify exact model, brand, and year rather than generic categories to reduce invented details.
- Add component-level detail sections to the prompt to constrain output to specific parts such as body, electronics, hardware, and neck.
- Request blank callout boxes in the prompt so you can add verified, factual labels manually in Photoshop, Figma, or Paint.
- Use NotebookLM by adding source resources such as links, PDFs, manuals, and documentation to ground the infographic in factual content.
- Customize NotebookLM infographic output via the infographic options, including orientation and professional style.
- Iterate technical infographics multiple times until the visual output is acceptable, since quality varies across generations.
- Validate every technical detail yourself, especially for specialized or professional deliverables.
- Treat the text/reasoning layer and the image-generation layer as separate systems with different reliability profiles.

## Failure modes named
- Generic prompts lead the model to invent plausible-but-wrong components.
- Image generators hallucinate internal technical parts (bolts, wires, chips, batteries, microchips) because they visually imagine rather than factually render.
- Non-expert users accept outputs as correct because the infographic looks convincing.
- Reusing the same chat for multiple infographic generations can confuse the model.
- Even correct source material in NotebookLM does not eliminate visual errors from the underlying image generator.
- Handing auto-generated infographics to clients without verification risks professional and factual mistakes.

## Studio relevance
07 verify - how the studio uses this card
