# Fleet engineering case studies

[Profile](../README.md) · [Capabilities by role](career-capabilities.md)

These case studies summarize a historical technical audit completed on October 30, 2026. RIG is Mike Rodgers' internal engineering environment. Mike directs its architecture, priorities, operating decisions, and acceptance criteria, with AI agents assisting implementation and verification. The audit does not assign every command or code change to Mike personally.

This record is summarized for external readers, in runnable form, as the public [case-study set in fde-portfolio](https://github.com/mrodgersjs-web/fde-portfolio/blob/main/CASE-STUDIES.md); that file states evidence tiers per case and is sanitized of internal paths and ports.

The work spans Apple Silicon hosts, a Linux GPU server, NAS storage, desktop applications, and hosted providers. It is evidence of internal engineering and operations, not customer production deployment or a current availability report.

## Evidence and scope

The audit combined dated operational reports, selected machine-readable receipts, historical session summaries, and research notes. A report-backed result means the audit inspected the report, not that it re-ran every test. A summary-backed result has less direct support. Research and proposed designs remain separate from executed work.

The private audit contains 106 overlapping competency and use records. That is not a count of unique skills, tools, or completed projects. The full knowledge index was unavailable during the audit, so all-time completeness is not claimed.

Original records contain private infrastructure and application data. This public version retains mechanisms, dates, results, and limitations while omitting addresses, local paths, credentials, account identifiers, and private transcripts. The source register below identifies the underlying report families without publishing those records.

## Fleet infrastructure and recovery

### Storage offload with integrity checks

**Problem.** A workstation under disk and swap pressure needed storage offload without losing recoverable application copies.

The workflow packaged macOS applications with metadata-preserving archives, recorded manifests, and compared SHA-256 hashes after transfer to QNAP NAS storage. Removal depended on remote verification. Bounded extraction checked archive contents, metadata, and symlinks.

**Recorded result.** The October 24–25 archive audit verified 47 application archives and transferred 10 media files. It recorded remaining cleanup targets instead of declaring the entire request complete. Original JSON and archive manifests were inspected for this audit. [Source F1](#source-register)

**Limit.** Bounded extraction did not prove full application restoration. The archive count does not measure net disk space reclaimed. A separate external-drive incident passed a native device-reset call but failed disk detection; the drive remained unrecovered.

### Container and service migration across hosts

**Problem.** Local container workloads competed with model and desktop workloads. Offload had to retain service identity, data, and a rollback path.

The migration used Docker contexts, Colima, image-ID comparisons, cold archives, retained volumes, and persistent service forwarding. Database checks compared table and user counts. TLS checks included trusted connections and rejection of incorrect hostnames. Vector and document services received endpoint checks and retained snapshots.

**Recorded result.** The October 13 report recorded all 66 original image IDs at the destination. A Supabase migration matched 9 authentication users and 42 public tables. Voice services answered protocol probes, and remote desktop profiles survived bounded screenshot and file-list checks. These are report-backed results. [Source F2](#source-register)

**Limit.** The overall migration report remained partial. Table counts and healthy endpoints do not prove row-level parity, complete user journeys, full voice conversations, or vector collection parity. Retained rollback data is not a tested disaster-recovery plan.

### Service recovery that respects active workloads

**Problem.** A reachable machine could still lack model listeners after reboot, while another service on the same host remained usable.

Diagnostics compared SSH access, process and listener state, launchd domains, service definitions, login state, and Docker contexts. This isolated a login-dependent macOS startup failure without assuming that every remote service was down. Linux GPU recovery checked scheduler queues, active jobs, and ownership before changing service state.

**Recorded result.** October reports identified missing GUI launchd domains and absent model listeners while separately confirming usable Docker services. A Linux model service was restored after idle checks and passed an exact-output chat probe. An unrelated optimizer activation stopped when new application work appeared. [Sources F3 and I1](#source-register)

**Limit.** Startup diagnosis did not prove reboot survival. Successful recovery probes were bounded. Continuous availability and fleet-wide service-level objectives were not established.

## Model serving and client compatibility

### Qualifying local inference beyond a model list

**Problem.** An endpoint can advertise a model and answer one text prompt while failing the tool loop an agent needs.

Work across vLLM, SGLang, llama.cpp, MLX, and Ollama separated API-family detection, model inventory, exact-output chat, streaming, structured tool calls, and multi-turn continuation. Embedding shape and vision requests received separate probes. Client catalogs were checked against server behavior.

**Recorded result.** October tests found routes that passed chat and structured tools, routes that timed out under load, and a NAS route that passed continuation without tools but failed normal tool continuation. The audit retained those distinctions rather than giving the fleet one pass flag. [Source I1](#source-register)

**Limit.** A direct HTTP pass does not establish native application acceptance. A valid embedding vector does not establish retrieval quality. Individual modality checks do not apply to every model or client.

### Multi-GPU serving and runtime compatibility

**Problem.** Large local models required compatible GPU placement, serving runtimes, tool parsers, and reproducible configuration.

Historical work included llama.cpp layer splitting, vLLM and SGLang service operation, CUDA and NCCL topology, PCIe peer-to-peer constraints, model revision and container-image pinning, and parser repair. One repair corrected tool parsing and disabled unstable speculative decoding before rerunning agent loops.

**Recorded result.** July records described successful multi-GPU inventory, chat, streaming, tools, context, and recovery checks on specific configurations. One certification recorded 24 successful quality trials. October reconciliation downgraded routes without fresh tests to historical or conditional status. [Source I2](#source-register)

**Limit.** These results are historical and configuration-specific. They do not establish present availability, distributed training, foundation-model training, or performance for another model. Serving a pretrained model is distinct from training it.

### Context, reasoning, and account routing

**Problem.** Client settings, server limits, and configuration overrides could disagree. A visible model choice did not guarantee the intended provider account or reasoning behavior.

Work traced effective configuration precedence, corrected model IDs and context metadata, preserved unrelated settings, and checked native selectors. Context tests distinguished advertised limits, accepted input length, recall, and compaction. Account tests used isolated choices and routing markers.

**Recorded result.** October 29 records reported a gateway accepting 500,037 input tokens and five account-isolation checks passing. Native reasoning checks found that several visible effort labels normalized to the same server behavior. The audit explicitly separated prompt instructions from hard reasoning-token budgets. [Source I3](#source-register)

**Limit.** Accepted input length does not prove useful reasoning over the whole context. Original-conversation recovery, automatic compaction, and broad endurance acceptance remained open. Some provider accounts were quota-limited.

## Protocols, applications, and workflows

### MCP process lifecycle and schema repair

**Problem.** A referenced Node.js cleanup timer kept disconnected stdio servers alive. A separate tool schema failed provider compatibility checks.

The lifecycle repair unreferenced the timer, checked EOF and abrupt disconnect behavior, and then adopted the upstream release. The schema repair replaced an incompatible fixed-length tuple representation with a constrained array, with backups and contract checks.

**Recorded result.** Historical Dembrandt tests covered ten EOF cycles, abrupt disconnects, extraction, and two LAN cycles exposing 21 tools with clean process exit. Original LAN verification JSON was inspected. The schema-repair summary reported 14 validation and inventory checks, plus synthetic provider requests. [Sources P1 and P2](#source-register)

**Limit.** The schema tests did not replay the original full-context conversation. The process leak contributed to resource pressure, but the audit did not establish it as the sole cause of every workstation crash.

### Queue ownership and safe workflow coordination

**Problem.** Competing queue stores and ambiguous ownership could duplicate work or mark incomplete tasks done.

The integration established one authoritative queue, added atomic claims, checked capacity and ownership, and made progress updates idempotent. A fleet sensor published capacity observations without dispatching business work. Task reconciliation preserved unrelated records and kept historical completion claims reviewable.

**Recorded result.** The October 24–25 summary reported 97 isolated queue-control tests and an idempotent repeat writeback. It also reported a 187-record reconciliation that preserved 1,924 unrelated records. Automatic coordination remained off. [Source P3](#source-register)

**Limit.** Isolated controls and observation-only telemetry did not establish fully autonomous operation. Native adoption on remote clients and acceptance of the complete work-dispatch path remained open.

### Scheduled execution and resource isolation

**Problem.** Moving automation required proof that the target scheduler ran jobs, plus controls against overlap and runaway resource use.

The migration used a serialized runner, kernel locking, bounded CPU, memory and process settings, timeouts, read-only mounts, and scoped credentials. A broader routine inventory separately tracked activation state and retained holds on unaccepted work.

**Recorded result.** The October 13 report recorded two actual scheduled successful receipts for each of 21 migrated routines. The broader October 18 summary mapped 1,139 routine identities locally and retained them on hold. [Sources F2 and P4](#source-register)

**Limit.** The 21-routine result did not certify the larger automation estate. Configured resource limits do not measure actual usage. A full bulk import into the external work tracker failed and was not claimed complete.

### Database recovery and desktop persistence

**Problem.** Corrupted local application state and component updates interrupted desktop workflows.

Recovery used SQLite salvage, integrity checks, row comparisons, reconstruction from surviving indexes, and atomic replacement. Desktop integration work preserved native component files, checked update-watch behavior, and tested create, edit, save, reload, and reopen paths.

**Recorded result.** The October 12 recovery summary reported preservation of 4,491 readable sessions and reconstruction of seven damaged headers, followed by observed UI recovery. Later desktop tests verified selected persistence paths and bounded component checks. [Source P5](#source-register)

**Limit.** Exact lost header metadata was not recovered. Synthetic workflow fixtures did not establish live model execution. Final native acceptance remained open for several integrations. A browser-control design involving Electron IPC and WebRTC was staged and blocked, not deployed.

## Knowledge systems and engineering judgment

### Separating research, configuration, and execution

**Problem.** A large collection of plans and tool catalogs can make intended architecture look like an operating system.

The audit classified each record by provenance and acceptance state. It used authenticated knowledge retrieval and focused Recall reads, retained degraded-index status, and treated architecture cards as design evidence. This prevented proposed storage, tracing, workflow, and database components from becoming deployment claims.

**Recorded result.** The October 30 research audit completed focused reads of all 18 cards returned by its final query. The broader search was still bounded and overlapping. Design notes covered memory provenance, privacy, contradiction handling, approval boundaries, and rollback. [Source K1](#source-register)

**Limit.** Search coverage did not establish a complete corpus census. Recall notes alone did not prove deployment of Temporal, n8n, Dify, LangSmith, Langfuse, Phoenix, or every proposed database. The audit found no sufficient evidence for broad Prometheus/Grafana deployment, NAS RAID administration, or a full disaster-recovery restore.

## Source register

The source IDs refer to the private audit reviewed on October 30, 2026. They are provenance labels, not public download links. The [public project receipts](../README.md#recent-receipts) support their linked repositories only.

| ID | Dated evidence family | Audit treatment |
| --- | --- | --- |
| F1 | October 24–25 storage offload and archive verification; October 23–24 external-drive diagnostics | Original reports, manifests, and selected JSON inspected. |
| F2 | October 13 container and fleet migration | Detailed operational report inspected; selected independent verification fields inspected. |
| F3 | October 24 service-domain and fleet recovery findings | Original reports inspected. |
| I1 | October 19–25 endpoint, tool, and service-recovery audits | Reports and listed machine-readable evidence informed the inference audit; no fresh fleet retest. |
| I2 | July multi-GPU certifications and parser repair; October registry reconciliation | Historical receipts and registry evidence, with stale route status retained. |
| I3 | October 29 context, reasoning, and account-route work | Dated receipts and audit summaries; native and long-context limits retained. |
| P1 | October 12 Dembrandt lifecycle and LAN verification | Original LAN JSON inspected, supplemented by historical summary. |
| P2 | October 21 MCP schema repair | Historical session summary; full-context replay absent. |
| P3 | October 24–25 queue integration and task reconciliation | Historical session summary; broader native acceptance incomplete. |
| P4 | October 18 routine inventory and import attempt | Historical session summary; remote coverage and bulk import incomplete. |
| P5 | October 12 SQLite recovery and October 28 desktop integration | Historical session summaries and candidate intake records. |
| K1 | October 30 authenticated knowledge retrieval and live Recall reads | Read-only audit, degraded full index, design evidence kept separate. |

[Return to the profile](../README.md)
