<p align="center">
  <img src="assets/profile-banner-v2.jpg" alt="Mike Rodgers, Head of AI" width="100%" />
</p>

<div align="center">
  <h1>Mike Rodgers</h1>
  <p><strong>I turn AI pilots into production systems you can defend in a board meeting.</strong></p>
</div>

<p align="center">
  Head of AI · Forward-Deployed AI Engineering · Denver · <a href="mailto:mrodgersjs@gmail.com">mrodgersjs@gmail.com</a> · <a href="https://www.linkedin.com/in/mike-rodgers-ai/">LinkedIn</a> · <a href="https://rodgersintelligence.com/">rodgersintelligence.com</a>
</p>

<div align="center">

[![public repositories](https://img.shields.io/badge/dynamic/json?url=https%3A%2F%2Fapi.github.com%2Fusers%2Fmrodgersjs-web&query=%24.public_repos&label=public%20repositories&logo=github)](https://github.com/mrodgersjs-web?tab=repositories)
[![CI covered](https://img.shields.io/badge/CI%20on%20public%20repos-29%20of%2032-brightgreen)](https://github.com/mrodgersjs-web?tab=repositories)
[![steward score](https://img.shields.io/endpoint?url=https%3A%2F%2Fraw.githubusercontent.com%2Fmrodgersjs-web%2Fmrodgersjs-web%2Fmain%2Fsteward%2Fscoreboard%2Fbadge.json)](https://github.com/mrodgersjs-web/mrodgersjs-web/tree/main/steward/scoreboard)
[![rigforge smoke](https://github.com/mrodgersjs-web/rigforge/actions/workflows/smoke.yml/badge.svg?branch=main)](https://github.com/mrodgersjs-web/rigforge/actions/workflows/smoke.yml)

</div>

> **One operator. One machine. Every receipt public.**

## What this estate measures

| | Public | With CI | Licensed |
|---|---|---|---|
| Systems you can clone and run today | **32 repositories** | **29 of 32** | **32 of 32** |

Languages on this profile: Python, TypeScript, JavaScript. The fleet that runs my company is 64 repositories; 35 stay private because they carry client data, and that split has been deliberate rather than tidy. Nothing here is a demo directory.

## Pinned systems

| System | What it demonstrates | Verify |
| --- | --- | --- |
| [**rigforge**](https://github.com/mrodgersjs-web/rigforge) | Builds and checks ProofPacket evidence through a reproducible smoke path. | `git clone https://github.com/mrodgersjs-web/rigforge.git && (cd rigforge && python3 -m venv .venv && . .venv/bin/activate && bash scripts/smoke.sh)` |
| [**proof-studio**](https://github.com/mrodgersjs-web/proof-studio) | Verifies signed completion evidence and detects tampering. | `git clone https://github.com/mrodgersjs-web/proof-studio.git && (cd proof-studio && python3 -m venv .venv && . .venv/bin/activate && bash scripts/smoke.sh)` |
| [**mesh-studio**](https://github.com/mrodgersjs-web/mesh-studio) | Probes, boots, and recovers a local agent-service mesh. | `git clone https://github.com/mrodgersjs-web/mesh-studio.git && (cd mesh-studio && python3 -m venv .venv && . .venv/bin/activate && bash scripts/smoke.sh)` |
| [**communications-studio**](https://github.com/mrodgersjs-web/communications-studio) | Scores a draft message against formulas and hard gates, then emits or rejects it, with pytest as the claim under test. | `git clone https://github.com/mrodgersjs-web/communications-studio.git && (cd communications-studio && python3 -m venv .venv && . .venv/bin/activate && bash scripts/smoke.sh)` |
| [**ai-user-testing-mcp**](https://github.com/mrodgersjs-web/ai-user-testing-mcp) | TypeScript MCP server: drives a real browser as a synthetic user and fails a flow on evidence rather than vibes. Newest public surface, CI on `ci.yml`. | `git clone https://github.com/mrodgersjs-web/ai-user-testing-mcp.git && (cd ai-user-testing-mcp && npm ci && npm run build)` |
| [**rig-os-agency**](https://github.com/mrodgersjs-web/rig-os-agency) | Next.js and React operator console over an AI SDK control plane. The delivery-surface half of the fleet. | `git clone https://github.com/mrodgersjs-web/rig-os-agency.git && (cd rig-os-agency && npm ci && npm run build)` |
| [**jake-studio**](https://github.com/mrodgersjs-web/jake-studio) | Checks the L10 harness modules offline: certainty engine, cognition stack, nocturne and agent factory. | `git clone https://github.com/mrodgersjs-web/jake-studio.git && (cd jake-studio && python3 -m venv .venv && . .venv/bin/activate && bash scripts/smoke.sh)` |
| [**deviatrix-genesis**](https://github.com/mrodgersjs-web/deviatrix-genesis) | Runs an idea through three diamonds, three expeditions and seven stages, with a verifier that signs each sealed proof packet. | `git clone https://github.com/mrodgersjs-web/deviatrix-genesis.git && (cd deviatrix-genesis && python3 -m venv .venv && . .venv/bin/activate && pip install sympy && PYTHONPATH=. python3 -m unittest deviatrix_genesis.tests.test_deviatrix deviatrix_genesis.v3.tests.test_v3 deviatrix_genesis.v4.tests.test_memory_export deviatrix_genesis.v5.tests.test_v5)` |

## Which requirement each system answers

Cross-checked against the requirement language in 108 live Head-of-AI, VP-AI, Forward-Deployed-Engineer and AI-infra postings, October 2026. The percentages are how often that requirement appeared, not how much I rate it.

| The posting says | Frequency at this tier | What I have that answers it |
|---|---|---|
| "eval infrastructure" · reliability, observability, drift | 60% leadership · 32% FDE | [rig-enhanced-evals](https://github.com/mrodgersjs-web/rig-enhanced-evals), [rig-enhanced-guardrails](https://github.com/mrodgersjs-web/rig-enhanced-guardrails) — schema, format, toxicity and fact checks that sign a receipt |
| "write and review production-grade code across frontend and backend using JavaScript or Python" | 50% FDE · named in OpenAI and Anthropic leadership reqs | [ai-user-testing-mcp](https://github.com/mrodgersjs-web/ai-user-testing-mcp), [rig-os-agency](https://github.com/mrodgersjs-web/rig-os-agency), [mrodgersjs-web-teammate](https://github.com/mrodgersjs-web/mrodgersjs-web-teammate) (`npx` CLI) |
| "agents, tool-calling, orchestration" | 58% leadership · 41% FDE | [rig-agent-firm](https://github.com/mrodgersjs-web/rig-agent-firm), [rig-domain-agents](https://github.com/mrodgersjs-web/rig-domain-agents), [mesh-studio](https://github.com/mrodgersjs-web/mesh-studio) |
| "retrieval, data integration, ontology" | 27% leadership · 45% FDE | `rig-memory-os` — Brier-scored prediction memory with signed provenance and paged retrieval. Private today; see Known gaps |
| "governance, model risk, compliance, approval boundaries" | 73% leadership | [doctrine](https://github.com/mrodgersjs-web/doctrine), [proof-gate-action](https://github.com/mrodgersjs-web/proof-gate-action), [rig-doctrine-overlay](https://github.com/mrodgersjs-web/rig-doctrine-overlay) |
| "measurable business value, ROI, cost" | 61% leadership | [fde-portfolio](https://github.com/mrodgersjs-web/fde-portfolio) — discovery to handoff as data · [resume](https://github.com/mrodgersjs-web/resume) with the sourced numbers |
| "did it actually ship?" | every tier | [rigforge](https://github.com/mrodgersjs-web/rigforge), [proof-studio](https://github.com/mrodgersjs-web/proof-studio), [doneseal](https://github.com/mrodgersjs-web/doneseal) — hash-verifiable, Ed25519-signed completion evidence |
| "at least one systems language such as Go, Rust, or C/C++" | 0% leadership · 46% of infra reqs name Rust, 42% name C++ | Not yet. Claiming the gap rather than the badge — see What happens next |

## Languages, stated plainly

**Python** — the working language of the systems above: harnesses, MCP servers, evals, data plumbing, CI. This is what the profile has mostly shown, and it is accurate as far as it goes.

**TypeScript** — the delivery surface, and the half of the Forward-Deployed bar my public profile used to hide. Ten TypeScript repositories exist in the estate; `ai-user-testing-mcp` and `rig-os-agency` are now public so the claim is checkable instead of asserted.

**JavaScript** — [mrodgersjs-web-teammate](https://github.com/mrodgersjs-web/mrodgersjs-web-teammate), installable with `npx`, with a green CI run.

**Rust** — in flight, not claimed. `jev-route`: a routing-policy CLI that takes a task and a candidate list and returns a choice, a confidence and a fallback verdict, as a single binary with the benchmark checked in. It lands here when it compiles and tests, not before.

**C++** — I read and profile serving and kernel stacks. No authorship claim until there is a repo behind it.

## How I work

> Code owns decisions. LLMs assist transformation. Gates decide if it ships.

- Deterministic before agentic. Any rule that can be a function does not get a prompt.
- Every claim names its source, every completion carries a receipt, every migration is reversible.
- Fewer repositories, deeper modules, clearer ownership.
- Local-first and private by default. A hosted model is a per-call decision, not a default.

## How a recruiter should spend 10 minutes

1. **0–2 minutes.** Open [`rigforge`](https://github.com/mrodgersjs-web/rigforge) and its [latest smoke receipt](https://github.com/mrodgersjs-web/rigforge/actions/workflows/smoke.yml).
2. **2–4 minutes.** Select the pinned system closest to the role you are hiring for.
3. **4–7 minutes.** Copy its Verify command and run the public smoke path on your own machine.
4. **7–9 minutes.** Inspect the linked receipt's state, date and commit SHA.
5. **9–10 minutes.** Read Known gaps below and decide whether those gaps matter for your role.

## Known gaps, before you find them

- **Steward score: 75/100.** The badge up top is honest and it is red. It is a self-audit of repository hygiene, not a benchmark, and the 25 points missing are documentation and release discipline on the smaller studios.
- **`rig-os-agency` has no enforced CI yet.** It went public on 29 October and carries an MIT license, but its only workflow, `rig-lattice.yml`, is gated behind a repository variable that is currently off: inherited from an unpublished scorer, not a passing build. `ai-user-testing-mcp` is the stronger TypeScript evidence, with `ci.yml`, `rig-lattice.yml` and `weekly-catalog-refresh.yml`. A smoke workflow for the console is item one below.
- **`rig-memory-os` is still private.** It is the strongest retrieval-and-memory artifact in the estate and the one FDE interviewers ask about. It comes out once the client identifiers are stripped.
- **No compiled-language artifact yet.** At the leadership tier that is a non-issue. Against the AI-infra bar it is a real one, and the fix is the Rust CLI above rather than a claim.
- **No distributed serving layer, no training runs.** I deploy and govern systems other people trained. I am not going to imply otherwise.

## What happens next, in order

1. `rig-os-agency`: add `smoke.yml` and turn on an enforced build, so nothing public ships without a receipt. Licensing already closed the same day it went public — every public repository here now declares one.
2. `jev-route` in Rust: the routing policy that already governs this fleet, as a standalone binary with a benchmark.
3. Strip client identifiers out of `rig-memory-os` and make it public.
4. Retire the `rodgemd1-lgtm` handle into this one so there is a single hiring-facing estate.

Public repositories here are deliberate release surfaces, and each one that clears its security, licensing and documentation boundary ships. Two TypeScript surfaces cleared that boundary on 29 October. Reach me at [rodgersintelligence.com](https://rodgersintelligence.com).
