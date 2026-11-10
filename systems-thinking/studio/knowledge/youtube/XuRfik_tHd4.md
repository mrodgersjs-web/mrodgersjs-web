---
source: https://www.youtube.com/watch?v=XuRfik_tHd4
video_id: XuRfik_tHd4
channel: Nuno Tavares | Automated Marketer
title: "Claude Code + Obsidian: Build a Second Brain That Actually Learns"
scraped: 2026-08-28
tags: [productivity, obsidian, claude-code, knowledge-management, ai]
---
# Claude Code + Obsidian: Build a Second Brain That Actually Learns

Use Claude Code to turn an Obsidian vault into a living, linkable expert wiki by dropping raw documents into a structured folder system and letting the AI build, connect, and update notes automatically.

## Procedure / models distilled
- **Goal-first vault design:** create one Obsidian vault per domain (e.g., a tool, business, or personal second brain) rather than dumping everything into a single massive vault.
- **Use the Obsidian Web Clipper browser extension** to clip webpages directly into the vault as raw source material.
- **Establish a three-folder structure inside the vault:** `raw/` for unprocessed inputs, `wiki/` for synthesized guides and SOPs, and a schema/cache file that Claude reads as its rulebook.
- **Bootstrap the vault with a single Claude Code prompt:** paste a system prompt that instructs Claude to create the folder structure, write a `Claude.md` schema, and scaffold the initial wiki.
- **Define the primary domain topic** in the initial prompt so Claude knows whether the vault is a research topic, business knowledge base, or personal second brain.
- **Feed Claude raw files** (transcripts, docs, changelogs, screenshots) and ask it to create or link wiki pages from them.
- **Make Claude maintain cross-links:** explicitly request that Claude search for related pages and create `[[wiki-style links]]` so the graph view and index stay connected.
- **Generate derivative artifacts** from the wiki: SOPs, troubleshooting guides, presentations, or canvases by combining the stored knowledge with other Claude skills.
- **Run the system as Obsidian RAG:** Claude loads the schema, reads the index, pulls only the relevant pages, cross-references existing links, reasons, answers, and writes updates back into the notes.
- **Reserve Pinecone/Superbase RAG for massive archives:** use vector databases when source counts grow beyond ~100 documents, since Obsidian RAG loads full pages and consumes context window.
- **Keep `Claude.md` short (under ~200 lines)** as the static identity/rulebook; use the vault itself as the living knowledge store.
- **Name pages clearly and descriptively** because Obsidian RAG locates pages by filename, not by semantic meaning.
- **Schedule three maintenance triggers:** drop new release changelogs into `raw/` and tell Claude to update affected wiki pages; run a bi-weekly wiki lint for contradictions and stale claims; paste error details into Claude and ask if the troubleshooting wiki covers them.
- **Re-drop updated external files into `raw/`** because Claude does not auto-sync outside changes; stale summaries are a recurring risk.

## Failure modes named
- **Hallucinated expertise:** relying on Claude's training data or built-in memory instead of a curated vault leads to outdated or fabricated answers.
- **Mass-dumping everything:** throwing hundreds of files into a single vault breaks link quality and burns context; ~100 sources is the practical ceiling for Obsidian RAG.
- **Vague page names:** filenames that do not clearly describe the topic prevent Claude from finding the right page, because there is no semantic search.
- **Stale summaries:** docs updated outside the vault do not auto-sync, so the wiki gradually drifts from reality.
- **Bloated schema/index:** letting the `Claude.md` or index grow large consumes tokens on every query and degrades performance.
- **Context-window saturation:** at scale Claude cannot load every relevant page before running out of context, making a vector database necessary.

## Studio relevance
06 synthesize - use as a blueprint for consolidating scattered project docs, transcripts, and source material into a linked, queryable wiki that the studio can iteratively update via Claude Code.
