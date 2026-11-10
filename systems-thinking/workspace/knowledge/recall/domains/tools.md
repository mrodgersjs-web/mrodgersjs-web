> Cards tagged: 436 · Content sources: mirror 254 / API 55

Operating pack for Jake PAI Prime (`/jake`). The `tools` tag is the largest CORE domain (436/853). This pack does **not** inventory all 436. It clusters by tool family and names the highest-leverage stacks a working agent can adopt. GitHub (166) and YouTube (161) dominate the spine. ~52 cards are RIG/Hermes internal build specs (often duplicate “v12 Full Stack Setup” titles); those are treated as fleet context, not as 52 separate tools.

## How to use this pack

Adopt in this order unless a job is already locked to a stack:

1. **Runtime** — Hermes Agent CLI + optional OpenClaw hands + AionUi desktop.
2. **Coding** — Claude Code or Cursor with `CLAUDE.md` / rules + skills (`addyosmani/agent-skills`, `mattpocock/skills`, GitHub spec-kit).
3. **Memory** — Recall.it as the curated KB; Memori or `knowledge-base-server` for session-persistent agent memory; Unblocked-style context engine when repo+Slack+PRs are the source of truth.
4. **Local/private** — Cole Medin `local-ai-packaged` (n8n + Open WebUI + Ollama/Qdrant/Langfuse) or vLLM for Qwen-class inner loops.
5. **Harvest** — Crawlee (+ Playwright) for RAG crawls; n8n templates for Gmail/Slack/Drive; GPT-researcher / STORM for cited research.

---

## Agent CLIs — Hermes, OpenClaw, AionUi

- **Hermes Agent (Nous Research)** is the fleet’s default CLI/runtime: install + Web UI + workspace, slash-command registry, skill catalog, Super Hermes prisms. Cheat-sheet stack to actually install: `hermes-workspace` (daily UI), `mission-control` (builderz-labs, 3.7K+ stars — dispatch, cost, workflow coord), `hermes-skill-factory` (meta-skill that writes skills from workflows), `hindsight` (Vectorize — retain/recall/reflect, semantic+graph+temporal), `honcho-self-hosted` (cross-session memory), `hermes-web-search-plus` (Serper/Tavily/Exa routing), `lintlang` (static linter for agent configs), `AgentCash` (300+ premium APIs behind a wallet). [Card: Hermes Agent Master Cheat Sheet — Complete Slash Command Registry, Skill Catalog, Super Hermes Prisms, Design Libraries, and Global Capability Prompt](https://github.com/NousResearch/hermes-agent)
- Official install/docs path for Codex + Web UI + SEO swarms: Hermes Workspace getting-started. [Card: Hermes Agent + Hermes Workspace setup for Codex: install, Web UI, and SEO swarms](https://hermes-agent.nousresearch.com/docs/getting-started/installation)
- Catalog of skills/tools/integrations: [Card: 0xNyk/awesome-hermes-agent: A curated list of awesome skills, tools, integrations, and resources for Hermes Agent by Nous Research](https://github.com/0xNyk/awesome-hermes-agent)
- **OpenClaw** is the “hands” layer (browser/desktop actions). Pairing pattern: Hermes owns reasoning/skills; OpenClaw executes UI/OS actions; do not let both own the same workflow. [Card: How I have my Hermes and OpenClaw AI Agents.. WORKING TOGETHER!](https://www.youtube.com/watch?v=ziSeVy5p9ck) · [Card: Meet OpenClaw: How One Developer Gave AI Hands (Ep. 02)](https://www.youtube.com/watch?v=rzF5vSA9MEc)
- **Mission Control / org chart before more agents.** Bottleneck is structure, not prompting: visibility (dashboard) + ownership (org chart). Each agent: one category, one coordinator, no overlapping “do everything.” Phone-side Max HQ is for fetch/status, not a second brain. [Card: OpenClaw is 10x Better With This Mission Control Setup](https://www.youtube.com/watch?v=TveC4m3GQ_0)
- **Hermes Kanban** = multi-agent task board (work items, owners, state). Use as the operational surface for fleet jobs rather than chat-only dispatch. [Card: Hermes Agent Kanban Setup Guide (Multi-Agent Task Board)](https://www.youtube.com/watch?v=R_aLVXYzDac)
- **AionUi** — one free desktop shell that fronts Claude Code, OpenClaw, and Hermes so operators are not bouncing three CLIs. [Card: AionUi: One Free Desktop for Claude Code, OpenClaw & Hermes Agent](https://www.youtube.com/watch?v=-DffE5frG-0)
- OpenClaw skill firehose: **5,400+** skills filtered from the official OpenClaw Skills Registry — treat as a catalog, not an install-all. [Card: VoltAgent/awesome-openclaw-skills: The awesome collection of OpenClaw skills. 5,400+ skills filtered and categorized from the official OpenClaw Skills Registry.🦞](https://github.com/VoltAgent/awesome-openclaw-skills)

---

## Coding agents — Claude Code, Cursor, Codex, skills, spec-kit

- **Cursor 2026 agent pattern:** two customization layers — **rules** (markdown checked into git, included in every conversation; keep *minimal and high-quality* or they burn context and confuse the agent) vs **skills** (occasional specialized workflows). Shift-Tab **plan mode** for vague product asks; iterate the plan before implement. Agents should be allowed to use installed CLIs (gh, AWS, kubectl, Docker). Use them to speed test suites, trim deps, and optimize CI — not only to write features. [Card: Cursor: coding agents tutorial (2026)](https://www.youtube.com/watch?v=kF2WQgk1LtY)
- **Claude Code as a business OS, not a coder:** repo layout `company-os/CLAUDE.md` (global brain) + `.mcp.json` (Gmail, Drive/Docs/Sheets, Notion, HubSpot) + `.claude/settings.json` (permissions). Build **only the top 3 workflows** first. Score = time-saved/week × team-pain(1–10): proposal writing 4h×9=36 (1st), content repurposing 5h×6=30 (2nd), weekly reports 3h×8=24 (2nd), onboarding 2h×9=18 (3rd). Weekly report agent: pull HubSpot/Notion/Drive → max 400 words → **STOP for approval** → then Drive `/Reports/[Client]/[YYYY-WW]/` + email. Rollout: week 1 = one AI Champion runs all 3 agents. [Card: Claude Code AI Business Operating System — Full Build Guide](https://www.mindstudio.ai/blog/connect-claude-code-notion-gmail-mcp-servers/)
- **GitHub spec-kit** — spec-driven development toolkit for Claude Code / other agents. Prereqs: Python 3.11+, Git, uv or pipx. Pattern: write the spec, then ask the agent to research rapidly-changing stacks (e.g. .NET Aspire, JS frameworks) into a research doc and spawn **parallel** web-research tasks; nudge when it researches the wrong thing. Extensions include Agent Assign, Architecture Guard, API Evolve (semver + deprecation gates), Brownfield Bootstrap. [Card: github/spec-kit: 💫 Toolkit to help you get started with Spec-Driven Development](https://github.com/github/spec-kit)
- **addyosmani/agent-skills** (production engineering skills): `incremental-implementation` (thin vertical slices, feature flags, rollback), `test-driven-development` (red-green-refactor, pyramid 80/15/5, Beyoncé Rule: if it matters it has a test), `context-engineering` (rules + packing + MCP when quality drops), `source-driven-development` (cite official docs), `frontend-ui-engineering` (WCAG 2.1 AA), `api-and-interface-design` (Hyrum’s Law, One-Version Rule). [Card: GitHub - addyosmani/agent-skills: Production-grade engineering skills for AI coding agents.](https://github.com/addyosmani/agent-skills)
- **mattpocock/skills** — run `setup-matt-pocock-skills` **once per repo** before the rest. Daily loop: `/to-prd` (synthesize current chat → GitHub issue, no interview; quizzes which modules you touch), `/to-issues` (vertical-slice GitHub issues), `/tdd`, `/zoom-out`, `/improve-codebase-architecture` (run every few days — agents accelerate entropy), `/prototype`. Token saver: **caveman** (~75% fewer tokens, keep technical accuracy). Dangerous-git blocker: `git-guardrails-claude-code` hooks (push, reset --hard, clean). Shared `CONTEXT.md` / ubiquitous language so the agent stops using 20 words for 1 jargon term. [Card: GitHub - mattpocock/skills: Skills for Real Engineers. Straight from my .claude directory.](https://github.com/mattpocock/skills)
- Index of Claude Code skills/hooks/slash-commands/orchestrators: [Card: GitHub - hesreallyhim/awesome-claude-code: A curated list of awesome skills, hooks, slash-commands, agent orchestrators, applications, and plugins for Claude Code by Anthropic](https://github.com/hesreallyhim/awesome-claude-code)
- Companion tools around Codex/Claude Code (input quality, not the model): **Raycast** as clipboard manager (`Cmd+M`, month of history, images + x.com links) so research dumps into the agent in one paste. Codex framed as “Claude Code + Claude Cowork” — files on the right, any document type. [Card: 7 Tools That Make Codex 10x MORE Powerful](https://www.youtube.com/watch?v=SNAlFLV9MBE)
- Recurring Codex **engineering loops** (not one-shot chat): weekly RFC drift vs GitHub+Linear history; shipped-work table (repo / PR / first release / date); open-PR scan for “do not merge” that is now unblocked; Friday review stats (example: 7 PRs reviewed, 6 merged, 1 left). [Card: 5 Engineering Loops I'd Actually Run with Codex](https://www.youtube.com/watch?v=5dHRqb51fs0)
- **gsd-2** — meta-prompting + context engineering so agents run long without losing the big picture. Extension surface: Playwright browser tools, Brave/Tavily/Jina search, Context7 (fresh library docs), Subagent (isolated windows), GitHub `/gh`, MCP client, Ollama, Claude Code CLI provider, remote questions to Slack/Discord in headless/CI. [Card: gsd-build/gsd-2: A powerful meta-prompting, context engineering and spec-driven development system that enables agents to work for long periods of time autonomously without losing track of the big picture](https://github.com/gsd-build/gsd-2)
- Role-specialized “agency in a folder” personas (frontend → reality-checker) if you need named expert agents rather than one generalist: [Card: msitarzewski/agency-agents: A complete AI agency at your fingertips - From frontend wizards to Reddit community ninjas, from whimsy injectors to reality checkers. Each agent is a specialized expert with personality, processes, and proven deliverables.](https://github.com/msitarzewski/agency-agents)

---

## LLM runtimes — vLLM, Ollama, llama.cpp, OpenRouter, local-ai-packaged

- **Inner/outer model split:** outer orchestrator = Opus / GPT-5.4/5.5; inner coding loop = locally hosted **Qwen 3.6 via vLLM** (BF16 activations). Reported **~75% fewer tokens on premium models** after 6–7 realistic project tasks; 1.7M-token eval card is the worked example. Multi-agent concurrency prefers CUDA/vLLM; single-agent can feel faster on Mac (memory bandwidth). Target: one `docker compose` for Spark/CUDA boxes. [Card: 1.7M Tokens Later: Qwen via vLLM Crushes GPT-5.4 on Complex Code!](https://www.youtube.com/watch?v=pdZROva8FSo)
- Local setup companion: Qwen3.6 + llama.cpp + TurboQuant. [Card: Ultimate Guide Local AI Setup (Qwen3.6 + LlamaC++ + TurboQuant)](https://www.youtube.com/watch?v=5jkAlqbk66A)
- **Cole Medin `local-ai-packaged`** is **infrastructure, not an agent framework**. Profiles: `--profile cpu | gpu-nvidia | gpu-amd | none`. Mac: run Ollama natively, point n8n at `host.docker.internal:11434` (Docker `localhost` will miss it). Interfaces: n8n `http://localhost:5678/`, Open WebUI `http://localhost:3000/`; also Flowise, Supabase Studio, Neo4j, Langfuse, SearXNG, Qdrant. Wire Open WebUI → n8n via production Webhook + `n8n_pipe.py`. Import `n8n/backup/workflows/` for RAG templates. Supabase storage crash `"Region is missing"` → set `GLOBAL_S3_BUCKET`, `REGION`, `STORAGE_TENANT_ID`, S3 protocol keys from `.env.example`. Pairs with Hermes (ops), Space Agent (Qdrant+Neo4j knowledge), Archon (deterministic coding). [Card: Setup Guide: Cole Medin's local-ai-packaged Stack (Self-Hosted AI Infrastructure)](https://github.com/coleam00/local-ai-packaged) · [Card: local-ai-packaged](https://github.com/coleam00/local-ai-packaged)
- **Ollama + Home Assistant** for on-prem voice/home automation without sending household data out. [Card: Run a Local LLM: Ollama + Home Assistant](https://www.youtube.com/watch?v=j7yumDPWAEA)
- Cloud model router when local is not enough: [Card: OpenRouter](https://openrouter.ai/)

---

## Scraping / crawlers / browsers

- **Crawlee (Apify)** — Node/TS crawler for AI/RAG extraction. Adopt when you need: auto-scale, **proxy rotation + sessions**, hooks, CLI bootstrap, retries/routing, ready Dockerfiles. HTTP path: HTTP2, browser-like headers, TLS fingerprint replica, Cheerio/JSDOM, JSON APIs. Browser path: Playwright **or** Puppeteer same interface, headful/headless, Chrome/Firefox/Webkit, human-like fingerprints. Install: `npm install crawlee playwright` (Playwright not bundled). Apache-2.0; runs anywhere, optional Apify cloud. [Card: apify/crawlee: Crawlee—A web scraping and browser automation library for Node.js to build reliable crawlers. In JavaScript and TypeScript. Extract data for AI, LLMs, RAG, or GPTs. Download HTML, PDF, JPG, PNG, and other files from websites. Works with Puppeteer, Playwright, Cheerio, JSDOM, and raw HTTP. Both headful and headless mode. With proxy rotation.](https://github.com/apify/crawlee)
- Selenium bot-mitigation path (Cloudflare IUAM, Distil, Imperva, DataDome): [Card: ultrafunkamsterdam/undetected-chromedriver: Custom Selenium Chromedriver | Zero-Config | Passes ALL bot mitigation systems (like Distil / Imperva/ Datadadome / CloudFlare IUAM)](https://github.com/ultrafunkamsterdam/undetected-chromedriver)
- Hosted browser-for-agents: Browserbase skills appear in the OSS radar next to Hermes. [Card: Top Open-Source GitHub Projects : Browserbase Skills, sim, Hermes Agent, Symphony & Trellis #253](https://www.youtube.com/watch?v=chIJ5eLn-h8)
- OSINT catalogs exist on the spine (`jivoi/awesome-osint`, `The-Osint-Toolbox/AI-Resources`, LangGraph OSINT agent) — use as **research indexes**, not as default production crawlers. Prefer Crawlee/Playwright unless the job is explicitly OSINT.

---

## Automation — n8n, Retool

- **n8n template library (280+)** — largest OSS collection on the spine. Import JSON, set credentials, activate. High-leverage starters: Autonomous AI crawler; Hugging Face paper fetch/summarize/categorize; RAG chatbots on **Qdrant + OpenAI/Mistral** (finance docs, tax code, movies); Telegram LangChain agent with memory + tools; image-analysis Telegram bot. Departments tagged (Support, Ops, Finance, AI Research). [Card: GitHub - enescingoz/awesome-n8n-templates: 280+ free n8n automation templates — ready-to-use workflows for Gmail, Telegram, Slack, Discord, WhatsApp, Google Drive, Notion, OpenAI, and more. AI agents, RAG   chatbots, email automation, social media, DevOps, and document processing. The largest open-source n8n template collection.](https://github.com/enescingoz/awesome-n8n-templates)
- Modular **B2B outreach** n8n system (lead → sequence → send → log). Use as the outreach skeleton rather than inventing a new graph. [Card: AI Outreach Automation Platform — Modular n8n B2B Outreach System](https://github.com/anshwysmcbel2710/ai-outreach-automation-platform)
- **Retool** when the job is an internal admin app on existing DBs/APIs and n8n’s graph is the wrong UX. [Card: Retool | Build internal software better, with AI.](https://retool.com/)
- Combined local stack = n8n inside `local-ai-packaged` (above), not a second n8n.

---

## PKM / notes — Obsidian, Notion alternatives

- Doctrine: **system, not a second brain.** One surface beats Obsidian-plus-five-dashboards. Agents + Obsidian as an intelligence layer (work happens in the vault). Friction of multiple apps kills momentum. [Card: Build an Obsidian SYSTEM Not a Second Brain!](https://www.youtube.com/watch?v=OZ3ZNhrPbF4)
- **Claude Code + Obsidian** so the vault actually learns (agent writes/structures notes, not a dump). [Card: Claude Code + Obsidian: Build a Second Brain That Actually Learns](https://www.youtube.com/watch?v=XuRfik_tHd4)
- Plugin/theme/workflow index: [Card: kmaasrud/awesome-obsidian: 🕶️ Awesome stuff for Obsidian](https://github.com/kmaasrud/awesome-obsidian)

---

## Recall / context engines / agent memory

- **Recall.it** is the live curated KB this mission is built on (853 cards; API read-only). Product: “curate an AI that knows what you know.” [Card: Your AI Knowledge Base](https://www.recall.it/) · [Card: Recall 2.0 The Demo: Curate an AI that knows what you know](https://www.youtube.com/watch?v=eRr7yuxPsYg)
- **Unblocked context engine** (Peter Werry) — MCP + CLI + dashboard over repo/Slack/people graph. Hard lesson: wiring tools + a knowledge graph is **not** enough; you must distill, not just retrieve. Numbers from the talk: same engineering task **2.5 hours / 21M tokens** without the engine vs **25 minutes / 10M tokens** with it (~50% token drop, ~6× wall-clock) because it **stops doom-loops**. “Center a div” will not show the gain; feature/fix work will. Experts-by-vector-cluster (who owns this code) + LLM distillations of Slack/history beat raw graph walk. Observed IDE mix: Cursor and Claude Code dominate; VS Code/Codex smaller; Claude Desktop unexpectedly common; people wire Claude Code into CI. [Card: Mergeable by default: Building the context engine to save time and tokens — Peter Werry, Unblocked](https://www.youtube.com/watch?v=5ID22ACI7IM)
- Pinecone-side signal: naive RAG is being replaced by **structured / agentic memory patterns** (not “more chunks”). [Card: Pinecone Just Admitted RAG Is Broken. Here's the Pattern Replacing It.](https://www.youtube.com/watch?v=0TPq43Wpbz0)
- **knowledge-base-server** — shared brain across Claude/Codex/Gemini/ChatGPT/MCP. Pipeline: Obsidian/code/transcripts/bookmarks → SQLite+FTS5+embeddings → MCP+REST. Layers: capture → classify → promote (insights/lessons/decisions/runbooks) → synthesize. Three-tier memory (hot/warm/cold). Retrieve **summaries first**, full reads only when needed. Self-learning: session corrections become future context. [Card: willynikes2/knowledge-base-server — Persistent AI Agent Memory and Knowledge Pipeline](https://github.com/willynikes2/knowledge-base-server)
- **Memori** — LLM-agnostic agent-native memory. LoCoMo: **81.95% overall accuracy** at **1,294 tokens/query** = **4.97% of full-context** footprint; ~67% smaller prompts vs Zep; >20× cheaper than stuffing full context. OpenClaw default is forget-between-sessions; plugin `pip install hermes-memori` then `hermes config set memory.provider memori`. [Card: MemoriLabs/Memori: Memori is agent-native memory infrastructure. A LLM-agnostic layer that turns agent execution and conversation into structured, persistent state for production systems.](https://github.com/MemoriLabs/Memori)

---

## Design / presentation

- **oh-my-design** — `npx oh-my-design-cli install-skills` then restart the agent. Ships **67 real-company `DESIGN.md` files** (install is zero AI calls). `DESIGN.md` = Google Stitch tokens + Voice/Narrative/Principles/Personas/States/Motion. No API keys; runs inside Claude Code / Codex / OpenCode / Cursor. [Card: kwakseongjae/oh-my-design: Generate DESIGN.md from 77 real company design systems — brand tokens, components, philosophy. Drop into Claude Code or any AI agent.](https://github.com/kwakseongjae/oh-my-design)
- Open-source **deck stack** to install once: **Slidev + Mermaid + D2 + Plotly + Pandoc**. [Card: Hermes Install Prompt — Open-Source Presentation Stack (Slidev + Mermaid + D2 + Plotly + Pandoc) for RIG Deviation-Calibrated Decks](https://github.com/runablehq/Awesome-presentation-tools)
- Consulting-style PPT skill for agents: [Card: Mck-ppt-design-skill — Consulting-Style PowerPoint Design System for AI Agents](https://github.com/likaku/Mck-ppt-design-skill)
- **Spline AI** — generate **individual 3D objects**, not full scroll-driven sites. Access: text-to-3D, image-to-3D. Then assemble/name/animate in Spline; export Vanilla JS (preferred) or React; coding agent embeds as hero. Real-time variable API, webhooks, scroll/collision events. [Card: Spline AI Prompt Best Practices — Text-to-3D, Image-to-3D, and Ideawake Prism Workflow](https://docs.spline.design/spline-ai/ai-3d-generation)
- shadcn-adjacent component blocks: [Card: Shadcn UI Components, Blocks & Templates](https://www.cult-ui.com/)

---

## Infra / self-host / personal AI OS

- **Coolify** — self-hosted PaaS as Vercel/Supabase alternative: Git deploy, SSL, DB backups, extra servers, private git sources, storage buckets, shared env vars. Cost control when Vercel scales past “small site.” [Card: Coolify: STOP PAYING for VERCEL & SUPABASE with this NEW, FREE & SELF-HOSTED Alternative](https://www.youtube.com/watch?v=hl8ebudhqZU)
- Homelab dashboard (status, widgets, themes, UI editor): [Card: GitHub - Lissy93/dashy: 🚀 A self-hostable personal dashboard built for you. Includes status-checking, widgets, themes, icon packs, a UI editor and tons more!](https://github.com/Lissy93/dashy)
- Broader self-host map (LLMs, WireGuard, HA, networking): [Card: mikeroyal/Self-Hosting-Guide: Self-Hosting Guide. Learn all about  locally hosting (on premises & private web servers) and managing software applications by yourself or your organization. Including Cloud, LLMs, WireGuard, Automation, Home Assistant, and Networking.](https://github.com/mikeroyal/Self-Hosting-Guide)
- **danielmiessler PAI v5.0.0** — Life OS, not “AI scaffolding.” Install: `curl -sSL https://ourpai.ai/install.sh | bash` (v4→v5 is a different system; read migration first). Pulse daemon dashboard `localhost:31337`. **ISA** primitive: 12 sections (Problem → Vision → Out of Scope → Principles → Constraints → Goal → Criteria → Test Strategy → Features → Decisions → Changelog → Verification). Counts: 45 skills, 171 workflows, 37 hooks. Privacy is structural (`containment-zones.ts` + ContainmentGuard PreToolUse). Memory v7.6 buckets: WORK / KNOWLEDGE / LEARNING / RELATIONSHIP / OBSERVABILITY / STATE. Packs install into any coding harness without full PAI. [Card: danielmiessler/Personal_AI_Infrastructure: Agentic AI Infrastructure for magnifying HUMAN capabilities.](https://github.com/danielmiessler/Personal_AI_Infrastructure)

---

## Research agents, GUI agents, catalogs

- **GPT-researcher** — autonomous deep research on any data, any LLM provider. Default when the fleet needs a cited research run without standing up STORM. [Card: assafelovic/gpt-researcher: An autonomous agent that conducts deep research on any data using any LLM providers](https://github.com/assafelovic/gpt-researcher)
- **Stanford STORM** — LLM knowledge-curation: outline → collect → article generation with citations. Use when the output must look like a report, not a chat. [Card: stanford-oval/storm: LLM-powered knowledge curation system for research reports with citations](https://github.com/stanford-oval/storm)
- **UI-TARS desktop** (ByteDance) — open-source multimodal GUI agent stack (OS-level computer use). [Card: bytedance/UI-TARS-desktop: The Open-Source Multimodal AI Agent Stack: Connecting Cutting-Edge AI Models and Agent Infra](https://github.com/bytedance/UI-TARS-desktop)
- Public API index for wiring tools: [Card: GitHub - marcelscruz/public-apis: A collaborative list of public APIs for developers](https://github.com/marcelscruz/public-apis)
- MCP prompt library (25 research prompts: self-calibration, autonomous gates, RSI, swarm, market intel) — fleet-specific, not a product: [Card: RIG OS Consensus MCP Prompt Library: 25 Research Prompts for V10 Doctrine Architecture — Self-Calibration, Autonomous Gates, RSI, Swarm Intelligence, Market Intelligence](https://openreview.net/forum?id=OU9nFEYR2M)

GitHub awesome-lists on this spine (46 cards, almost no mirrors) that are **indexes, not runtimes**: `awesome-langchain`, `awesome-home-assistant`, `awesome-data-engineering`, `awesome-test-automation`, `awesome-shadcn-ui`, `awesome-vite`, `awesome-css-frameworks`, `awesome_ai_agents`. Consult, do not vendor.

---

## Default adoption stacks (copy these)

**A. Coding agent (repo work)**  
Claude Code or Cursor + git-checked **minimal rules** + `mattpocock/skills` (`setup-matt-pocock-skills` once) + `addyosmani/agent-skills` (TDD, incremental slices) + GitHub **spec-kit** for greenfield/brownfield specs + Raycast clipboard into the agent.

**B. Fleet operator (Jake PAI)**  
Hermes Agent + Hermes Workspace + Kanban + Mission Control org chart + AionUi. OpenClaw only for hands. Memory: Recall.it (curated) + Memori plugin (`hermes-memori`) or knowledge-base-server. Search: `hermes-web-search-plus`.

**C. Private AI for a client (one-day install)**  
`local-ai-packaged` (`gpu-nvidia` or Mac `none` + native Ollama) → n8n RAG import → Open WebUI pipe → Langfuse traces → Qdrant/Neo4j if knowledge-graph. Host apps on **Coolify**.

**D. Harvest + automate**  
Crawlee+Playwright crawlers → n8n 280-template library (Qdrant RAG, Gmail/Slack/Drive) → GPT-researcher/STORM for cited briefs.

**E. Design output**  
`oh-my-design` DESIGN.md + Slidev/Mermaid/D2/Pandoc decks + Spline for **components only**.

---

## Open gaps

- **Mirror stubs:** 254/436 cards have `mirror_path`, but **239 are <800 bytes** (title + “imported from recall.it” only). Substance for this pack came from **12 fat mirrors** plus **55 Recall `card` fetches** and 4 exhaustive searches (`Claude Code Cursor Hermes`, `n8n Crawlee vLLM`, `Obsidian Recall PKM`, `OpenClaw MCP agent tools`) saved at `outputs/raw/tools-search.json`.
- **Duplicate RIG/Hermes cards** (~52 “RIG OS Hermes v12 Full Stack Setup” / Design Studio Ultra-Install twins) inflate the 436 count; they are one stack, not 52 tools.
- Thin real coverage vs. the requested families: **Playwright/Firecrawl/Crawl4AI as first-class cards** (Crawlee is the stand-in); **Zapier/Make/Temporal**; **Continue.dev / Cline / Aider / Windsurf / Devin**; **llama.cpp/LM Studio as dedicated cards** (they appear inside local-AI walkthroughs); **MCP protocol itself** (only 2 cards, one is a RIG prompt library).
- YouTube-heavy how-tos (99 unclassified walkthroughs) are adoption-weak without timestamps; prefer the GitHub README cards when installing.
- Empty/`localhost`/`127.0.0.1` source_urls exist (Hermes dashboard, Pulse `localhost:31337`, Browser-First runtime). Treat as environment snapshots, not citations for other agents.
- Awesome-lists (46) have **0 mirrors** — titles/URLs only unless API-fetched.
