# Model Routing — Systems Thinking Studio

Rule: deterministic first, local fleet second, paid clouds only when the user
names them. The studio must run with zero paid-API balance on this box.

| Role | Model / engine | Endpoint | Why |
|---|---|---|---|
| Archetype match, leverage ranks, card lookups | none — `studio` CLI | local | deterministic, free, instant |
| Phase reasoning (default) | `grok-4.6` | `http://127.0.0.1:8317/v1` (fleet subscription proxy) | fastest verified node for code/reasoning class |
| Long-context synthesis (big frames, many citations) | `kimi-k3` (256k) | same proxy | fits full run-dir context |
| Hard diagnosis / adversarial review | `claude-sonnet-4-5` | same proxy | strongest tool-caller on the proxy |
| Cheap summarize (transcripts, abstracts) | `claude-haiku-4-5` | same proxy | cost-free on subscription |
| Swarm orchestration | frontier `agent_team`/`react` | FrontierAgent (`.env` → local proxy) | task board + deliverables + trace |
| Live KB search | Recall REST (`recall_api.py`) | backend.getrecall.ai | read-only, key in ~/.hermes/.env |
| Paper pulls | arXiv API + Semantic Scholar | public | no key |
| Parallel AI (slot) | TBD | needs `PARALLEL_API_KEY` | GROUND phase booster |
| Consensus MCP (slot) | TBD | needs MCP mount | GROUND phase booster |

Operational notes:
- FrontierAgent `.env` currently points at the local fleet proxy (OpenRouter
  was credit-dry 2026-08-28; backup `.env.bak-openrouter-20260828`). All
  harness phases inherit this routing automatically.
- Never put `RECALL_API_KEY` or proxy keys in phase prompts or deliverables.
- If the fleet proxy is down (`studio doctor` + `curl 127.0.0.1:8317/v1/models`),
  the harness degrades: phases 02-06 fall back to deterministic CLI outputs
  plus a "needs-agent-reasoning" marker — verify phase still runs and fails
  the run honestly rather than silently shipping unreasoned output.
