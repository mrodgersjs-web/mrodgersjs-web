# Capabilities by role

[Profile](../README.md) · [Fleet case studies](fleet-case-studies.md)

This map connects employer needs to Mike Rodgers' public projects and internal RIG operating history. It describes demonstrated work and its limits, not a proficiency score or a claim that every listed technology is in customer production.

Mike directs architecture, priorities, operating decisions, and acceptance criteria. AI agents assist code implementation, diagnostics, and verification. Repository contribution history and individual receipts are the appropriate sources for authorship of a particular change. The condensed public form of this map, one row per capability area, is the [skills-to-project matrix](https://github.com/mrodgersjs-web/fde-portfolio/blob/main/SKILLS-MATRIX.md); the workflow doctrine behind the evidence tiers is [here](https://github.com/mrodgersjs-web/fde-portfolio/blob/main/AI-ENGINEERING-WORKFLOW.md).

## Role fit

| Role | Relevant work | Evidence to review |
| --- | --- | --- |
| AI engineering leadership | Define acceptance criteria, choose model and tool boundaries, prioritize reliability work, and make release decisions from evidence. | [Verification projects](../README.md#selected-work) and [operating decisions](fleet-case-studies.md#service-recovery-that-respects-active-workloads). |
| Forward-deployed AI engineering | Diagnose tool and client incompatibilities, integrate applications and data, preserve existing workflows, and test the user's actual path. | [MCP repair](fleet-case-studies.md#mcp-process-lifecycle-and-schema-repair), [desktop persistence](fleet-case-studies.md#database-recovery-and-desktop-persistence), and [ai-user-testing-mcp](https://github.com/mrodgersjs-web/ai-user-testing-mcp). |
| AI platform and inference engineering | Operate pretrained models, reconcile routing and contexts, test tools and streaming, and manage GPU and host constraints. | [Inference case studies](fleet-case-studies.md#model-serving-and-client-compatibility) and [jev-route](https://github.com/mrodgersjs-web/jev-route). |
| Infrastructure and reliability engineering | Diagnose service startup, migrate containers and data, protect archives, trace process leaks, and retain rollback evidence. | [Infrastructure case studies](fleet-case-studies.md#fleet-infrastructure-and-recovery). |
| AI assurance and integration quality | Separate installation from execution and acceptance, validate failure cases, and reject unsupported completion claims. | [proof-studio](https://github.com/mrodgersjs-web/proof-studio), [rigforge](https://github.com/mrodgersjs-web/rigforge), and [case-study boundaries](fleet-case-studies.md#evidence-and-scope). |

The internal RIG work supports technical discussions for these roles. It does not by itself establish customer deployment scale, enterprise team size, budget ownership, or organization-wide production responsibility.

## Technical coverage

| Area | Mechanisms and technologies | Evidence level and boundary |
| --- | --- | --- |
| Python | Validation, operational scripts, test runners, evidence processing, and the stdlib profile steward. | Public repository code and workflow receipts. Inspect each project's tests for scope. |
| TypeScript and JavaScript | MCP adapters, schema contracts, application integration, Node.js process lifecycle, and monorepo tooling. | Public TypeScript project plus internal MCP repair records. This does not imply manual authorship of every module. |
| Rust | Deterministic routing, exclusions, confidence thresholds, and fallbacks in `jev-route`. | Public code and CI. Fleet-wide adoption of any version needs separate evidence. |
| C++ | Histogram and rate-limiting work in [latency-probe](https://github.com/mrodgersjs-web/latency-probe). | Public project reference. No general C++ systems-performance or production-scale claim is inferred. |
| Linux and macOS operations | systemd, launchd, process/listener inspection, service domains, runtime images, and native diagnostics. | Historical internal execution and incident reports. Reboot and endurance acceptance vary by service. |
| Networking | OpenSSH identities, host-key checks, LAN-first access, Tailscale fallback, forwarding, and endpoint behavior. | Dated route and service checks. No broad network-appliance administration claim. |
| Containers | Docker, Colima, contexts, image-ID migration, cold snapshots, volume retention, and resource controls. | Migration reports and scheduled receipts. No Kubernetes production claim. |
| Storage and recovery | QNAP NAS archival, metadata-preserving packaging, SHA-256 validation, bounded extraction, and external-drive diagnostics. | Inspected archive evidence. Full restore, RAID, ZFS, and HBS administration not established. |
| Relational and local databases | PostgreSQL, Supabase service migration, table/user consistency checks, TLS negative tests, and SQLite recovery. | Historical reports. Counts and integrity checks do not establish complete content parity. |
| Vector and document services | Qdrant, Chroma, Weaviate, FalkorDB, Tika, and retained snapshots during migration. | Endpoint and preservation evidence. Retrieval quality and collection parity remain separate. |
| Local inference | vLLM, SGLang, llama.cpp, MLX, Ollama, CUDA/NCCL topology, model pinning, parser repair, and bounded tuning. | Historical internal tests. Specific routes require fresh qualification. |
| Routing and client compatibility | LiteLLM audits, provider IDs, effective-config precedence, fallback chains, context metadata, account isolation, and native pickers. | Dated audits and bounded client tests. Catalog entries are not availability proof. |
| Model evaluation | Exact-output chat, SSE, structured tools, continuation, embeddings, vision, context boundary tests, and negative cases. | Explicit per-test results. No universal model-quality score or fleet-wide service-level guarantee. |
| Protocol integration | MCP stdio lifecycle, tool exposure, JSON schemas, validation, and credential boundaries. | Runtime and isolated-test evidence with original-conversation limits stated. |
| Workflow control | Atomic queue claims, idempotent progress, capacity accounting, scheduler locks, timeouts, and observation-only telemetry. | Isolated controls and scheduled receipts. Autonomous business dispatch remained off in the audited queue integration. |
| Desktop and browser integration | Native UI checks, persistent create/edit/save/reopen tests, component updates, SQLite state recovery, and browser-control design. | Mixed runtime and staged work. Electron/WebRTC browser control was not accepted. |
| Knowledge and governance | Authenticated retrieval, source provenance, research classification, private-data boundaries, rollback records, and independent review. | Historical audit method and public evidence tooling. Full knowledge-index coverage was unavailable. |

## Research and proposed architecture

Saved research considered Temporal, n8n, Dify, LangSmith, Langfuse, Phoenix, Redis/BullMQ, Neo4j, MinIO, quantization methods, and additional evaluation tools. Those records establish research and design context. They do not establish deployment or operational proficiency for every tool.

A technology can appear in both operational and research records. The case study's specific result controls the claim. For example, a service endpoint responding after migration says less about that database than a complete application migration and acceptance test would.

## How to assess the work

1. Pick a [public repository](../README.md#selected-work) that matches your role's technical problem.
2. Review its source, tests, verification instructions, and dated [workflow receipt](../README.md#recent-receipts).
3. Use a [fleet case study](fleet-case-studies.md) to discuss the operating constraint, decision, observed result, and remaining acceptance work.
4. Separate Mike's architecture and operating ownership from AI-assisted implementation and from third-party software used in the solution.

## Background

- U.S. Army Counterintelligence veteran
- B.S. Industrial Engineering, Iowa State University
- Six Sigma Black Belt
- Project Management Professional (PMP)

[Discuss a role](mailto:mrodgersjs@gmail.com) · [LinkedIn](https://www.linkedin.com/in/mike-rodgers-ai/)
