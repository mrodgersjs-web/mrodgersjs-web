<p align="center">
  <img src="assets/profile-banner.svg" alt="Mike Rodgers, Head of AI. AI infrastructure, model serving, and agent workflows." width="100%" />
</p>

# Mike Rodgers

**Head of AI at [Rodgers Intelligence Group](https://rodgersintelligence.com/). I take AI from pilot to production in regulated operations, and I build the checks that prove an agent's work is actually done.**

20+ years leading technology into operations, from a Caterpillar fabrication line to five hospital systems to a $6B health-tech business unit. Programs I've led add up to $35M in combined operating impact. In 2025 I founded Rodgers Intelligence Group (RIG), my AI practice. I run it on a private multi-node AI fleet and publish the verification tools I built to keep that fleet honest.

Denver · [Email](mailto:mrodgersjs@gmail.com) · [LinkedIn](https://www.linkedin.com/in/mike-rodgers-ai/) · [rodgersintelligence.com](https://rodgersintelligence.com/)

## Selected work

Six open-source tools from RIG. Each repo ships tests, CI, and instructions to verify it yourself.

| Project | What it does | Built with |
| --- | --- | --- |
| [**rigforge**](https://github.com/mrodgersjs-web/rigforge) | Catches AI coding agents when they say work is done but it isn't. | Python, MCP server |
| [**proof-studio**](https://github.com/mrodgersjs-web/proof-studio) | Tamper scenarios and benchmarks that show rigforge catching forged agent results. | Python |
| [**communications-studio**](https://github.com/mrodgersjs-web/communications-studio) | Checks AI-written messages against your rules and blocks the ones that fail. | Python |
| [**deviatrix-genesis**](https://github.com/mrodgersjs-web/deviatrix-genesis) | An idea pipeline that checks every generated claim with SymPy and statistics, then seals a verdict. | Python, SymPy |
| [**ai-user-testing-mcp**](https://github.com/mrodgersjs-web/ai-user-testing-mcp) | Governed AI user testing: reviewed tool adapters, a sandboxed runner, and evidence for every run. | TypeScript |
| [**jev-route**](https://github.com/mrodgersjs-web/jev-route) | Picks the model or tool for a task with a deterministic policy: choice, confidence, and fallback. | Rust |

<a href="https://github.com/mrodgersjs-web/rigforge"><img src="https://raw.githubusercontent.com/mrodgersjs-web/rigforge/main/docs/rigforge-demo.gif" alt="rigforge demo: a forged BUILD COMPLETE claim is caught by the signature check" width="100%" /></a>

<sub>rigforge in action: an agent's forged "BUILD COMPLETE" is caught by the signature check.</sub>

## Track record

- **Health systems.** At Advocate Health, led teletriage across five hospital systems that cut ED waits from about three hours to 15 minutes for 130,000+ patients. Emergency Care Innovation of the Year.
- **Teams and ventures.** Founded and scaled 83 Tech Harbor: 28 direct reports, $27M in operating budgets, $28M in venture investments.
- **Enterprise AI.** At Oracle Health (formerly Cerner), built an internal AI-powered competitive-intelligence capability that processed 150+ market signals a day and was adopted across every market segment.
- **Startups.** At EmOpti, delivered $1M in first-year revenue and supported a $10M Series A.

<sub>Career figures are from my resume, available on request.</sub>

## What I run day to day

I build and operate RIG's private AI fleet hands-on: Apple Silicon hosts, a Linux GPU server, and NAS storage, running local inference, MCP servers, and agents that work through real applications. I set the architecture and acceptance criteria; AI coding agents help implement and verify. Recent operating work:

- **Moved 66 container images across hosts** with rollback data retained and database and service checks.
- **Fixed an MCP process leak** of orphaned stdio servers, then tested disconnects and LAN cycles with 21 tools exposed.
- **Qualified inference routes test by test:** chat, streaming, tools, continuation, embeddings, vision, and context limits. A route that chats but fails tools does not get used for tools.
- **Verified 47 application archives** on QNAP storage with SHA-256 checks before anything was removed.

Stack: Python · TypeScript · Rust · MCP · vLLM · SGLang · llama.cpp · MLX · Docker · PostgreSQL · Qdrant

This is internal RIG work, not customer production. Each case study states what it proved and what is still open. [Fleet case studies →](docs/fleet-case-studies.md) · [Capabilities by role →](docs/career-capabilities.md)

## How I work

1. **Define done first.** What a result must demonstrate is written before the build starts, and tested through the client that will actually use it.
2. **Code decides when code can.** Deterministic rules for repeatable decisions. Models and agents for bounded work where they earn their place.
3. **Leave a receipt.** Tests, rollback data, and open items in writing. "Configured," "responds," and "accepted" are three different milestones.

## Recent receipts

Updated automatically from public GitHub records. Each row links the exact release and CI run.

<!-- recent_receipts starts -->
Steward score. **94/100 green**. Measured `2026-10-30`.

| Pinned system | Latest release | Latest smoke run |
| --- | --- | --- |
| [rigforge](https://github.com/mrodgersjs-web/rigforge) | [v1.1.0](https://github.com/mrodgersjs-web/rigforge/releases/tag/v1.1.0) · `2026-10-20` | [success](https://github.com/mrodgersjs-web/rigforge/actions/runs/40978301697) · `2026-10-30` · `413e511` |
| [proof-studio](https://github.com/mrodgersjs-web/proof-studio) | [v1.0.0](https://github.com/mrodgersjs-web/proof-studio/releases/tag/v1.0.0) · `2026-10-20` | [success](https://github.com/mrodgersjs-web/proof-studio/actions/runs/40977587451) · `2026-10-30` · `8f808f0` |
| [communications-studio](https://github.com/mrodgersjs-web/communications-studio) | [v11.1.0](https://github.com/mrodgersjs-web/communications-studio/releases/tag/v11.1.0) · `2026-10-20` | [success](https://github.com/mrodgersjs-web/communications-studio/actions/runs/40977564667) · `2026-10-30` · `a96f96b` |
| [deviatrix-genesis](https://github.com/mrodgersjs-web/deviatrix-genesis) | [v0.2.0](https://github.com/mrodgersjs-web/deviatrix-genesis/releases/tag/v0.2.0) · `2026-10-20` | [success](https://github.com/mrodgersjs-web/deviatrix-genesis/actions/runs/40977569733) · `2026-10-30` · `5b00262` |
| [ai-user-testing-mcp](https://github.com/mrodgersjs-web/ai-user-testing-mcp) | no release | [success](https://github.com/mrodgersjs-web/ai-user-testing-mcp/actions/runs/40980588870) · `2026-10-30` · `61b969a` |
| [jev-route](https://github.com/mrodgersjs-web/jev-route) | no release | [success](https://github.com/mrodgersjs-web/jev-route/actions/runs/40990218966) · `2026-10-30` · `394239f` |
<!-- recent_receipts ends -->

## Background

- U.S. Army Counterintelligence veteran
- B.S. Industrial Engineering, Iowa State University
- Six Sigma Black Belt
- Project Management Professional (PMP)
- Executive Board Member and Chairman, Milwaukee Tech Hub Coalition (2017–2020)

## Let's talk

Hiring a Head of AI, or someone to take agents from demo to production? [Email me](mailto:mrodgersjs@gmail.com) with the role and the system your team needs built or fixed.
