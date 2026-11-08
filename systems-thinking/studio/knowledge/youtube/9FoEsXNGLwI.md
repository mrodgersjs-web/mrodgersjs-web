---
source: https://www.youtube.com/watch?v=9FoEsXNGLwI
video_id: 9FoEsXNGLwI
channel: Indie Hacker News
title: "Someone open-sourced a hedge fund (53k stars on GitHub)"
scraped: 2026-08-28
tags: [finance, llm-agents, systematic-trading, multi-agent-systems, langgraph]
---
# Someone open-sourced a hedge fund (53k stars on GitHub)

A UCLA research project turned open-source "Trading Agents" uses a multi-agent LLM architecture to mirror a Wall Street trading firm, producing traceable, debatable, and auditable stock trading decisions.

## Procedure / models distilled
- Model real-world organizational structure as specialized LLM agents: fundamentals analyst, sentiment analyst, news analyst, technical analyst, bullish researcher, bearish researcher, trader, risk management, and portfolio manager.
- Run four analyst agents in parallel to generate written reports rather than collapsing outputs into a single numeric vector.
- Treat disagreement between analysts and researchers as signal, not noise, by preserving divergent reports in the decision chain.
- Use structurally opposed research agents (bull and bear) to debate across configurable rounds, citing specific numbers from analyst reports.
- Sequence decisions through multiple review stages: trader proposes timing and position size, risk management evaluates volatility and liquidity, and portfolio manager approves or rejects.
- Send approved orders to a simulated exchange, and terminate rejected trades with a written explanation.
- Orchestrate the entire workflow as a directed graph in LangGraph, with each agent as a node and checkpointed transitions for crash resumption.
- Maintain a persistent markdown decision log that records every run's reasoning, realized returns, alpha vs SPY benchmark, and a reflection injected into future portfolio manager prompts.
- Use Pydantic structured output schemas for decision agents so decisions parse cleanly and failure modes drop.
- Apply a consistent five-tier rating scale (buy, overweight, hold, underweight, sell) across the research manager, portfolio manager, and decision log.
- Position the project as a research framework and reference implementation rather than a production trading system or financial advice.
- Use an Apache 2.0 license to make the codebase a forkable foundation for retail fintech tooling and systematic strategy experiments.

## Failure modes named
- Most existing algorithmic trading tools are either rigid rule-based systems or black-box ML models that emit buy/sell signals with no explanation.
- Running the full agent graph on every ticker burns real money in LLM tokens due to parallel analyst calls plus debate rounds plus decision agents.
- The simulated exchange is only a backtest; there is no live broker integration, so users must wire real execution themselves.
- The authors explicitly warn against deploying real retirement capital based on the portfolio manager's output.

## Studio relevance
02 frame - use this card to frame how real-world organizations and decision workflows can be mapped into traceable, multi-agent LLM systems with explicit roles, disagreement, and audit trails.
