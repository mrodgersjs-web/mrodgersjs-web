## Sourced mechanism library (Systems Thinking Studio, v3)

> Curated structural/direct transfers only. Domain-specific prescriptions were excluded.
> Authority remains STAGED_NOT_PROMOTED; each rule activates only through its gate.

### causal-intervention-loop

- **Transfer:** `direct`
- **Rule:** Every claimed causal improvement must name an intervention, an observable outcome, a rival explanation, and a refutation condition.
- **Studio change:** Add causal-hypothesis and counterfactual fields to every intervention packet; do not turn correlation into a systems claim.
- **Prove/refute:** Plant an intervention whose observed outcome disagrees with the hypothesis; packet must turn RED rather than preserve the claim.
- **Card proof:** `8fd15ec6bed186705e13583131916d7bd98a7646e238a737f741303e5ff3be29`

### wip-before-throughput

- **Transfer:** `structural`
- **Rule:** When queue age rises, cap work-in-progress at the narrowest verified constraint before adding parallel agents or schedules.
- **Studio change:** Every campaign, swarm, and scheduled workflow declares WIP cap, queue-age signal, and drain condition.
- **Prove/refute:** Inject more queued units than the cap; system must defer excess work and report queue age instead of silently growing backlog.
- **Card proof:** `fc10837b4cf1fbba8caaf3b553064f63bcdcf233fc16347b33307ea9dd4bdd5d`

### requisite-observability

- **Transfer:** `structural`
- **Rule:** A controller may act only on state it can observe at the relevant delay; unknown state routes to bounded observation, never adaptive guessing.
- **Studio change:** System maps specify observed state, observer, sampling delay, allowed controller action, and unknown-state escalation.
- **Prove/refute:** Remove the required signal; controller must emit UNKNOWN/BLOCKED and avoid corrective action.
- **Card proof:** `48975423815d27770d2f304a48708213ac50df0fd44867514579a12fc5638b25`

### situation-coverage-not-checklist-coverage

- **Transfer:** `direct`
- **Rule:** A gate covers combinations of state, boundary, and failure mode—not merely a list of functions called.
- **Studio change:** Every high-stakes verification matrix includes situation dimensions and at least one planted-failure case per guarded boundary.
- **Prove/refute:** Plant a failure in an uncovered situation; coverage report must show a missing cell, then turn green only after a new regression case exists.
- **Card proof:** `b095632668580dcf7044cde1ab01a389c3c00ea7d46424c150bf46d0c9947fef`

### approval-boundary-map

- **Transfer:** `direct`
- **Rule:** High-impact actions cross a typed human approval boundary with a named approver, scope, expiry, and audit row.
- **Studio change:** Extend Gate-D packets with approval owner, action class, scope, expiry, and denied-path receipt; approval routing is a system boundary, not a chat convention.
- **Prove/refute:** Submit an action with a wrong/expired approver; it must fail before external execution and retain a denial receipt.
- **Card proof:** `49b95e878d8ed038eb674aea7ff0422cc77f8f4676fa6a91716786fdb8f7d49c`

### telemetry-diagnosis-loop

- **Transfer:** `direct`
- **Rule:** Every unattended loop needs telemetry sufficient for the next operator to distinguish a failed dependency, an unknown state, and a completed action.
- **Studio change:** Require health signal, last-success timestamp, last-failure evidence, queue/WIP age, and causal correlation ID in studio run packets.
- **Prove/refute:** Suppress a required signal; diagnostic output must name the missing signal and degrade rather than report healthy.
- **Card proof:** `48bdfb023209c4c8a67e1758e61995d7455effe8460754000943a9064d186a75`

### intent-traceability

- **Transfer:** `structural`
- **Rule:** Intent, boundary, test, artifact, and acceptance evidence stay traceably linked across the system boundary.
- **Studio change:** DoneContracts become traceability records: mission intent → hypothesis → intervention → gate → evidence → decision.
- **Prove/refute:** Delete one link in the chain; verifier must reject the done claim as untraceable.
- **Card proof:** `a3e9ed0180b2afb5c23dd19dc3cc134ef1dbde2da22ac4b69e812af49998cf9c`

### visible-degradation-and-recovery

- **Transfer:** `structural`
- **Rule:** Recovery is valid only when degraded state is visible, fallback activation is proven, and restoration is verified against the original contract.
- **Studio change:** Replace binary healthy/dead reports with PASS, DEGRADED, REPAIR_ATTEMPTED, and BLOCKED; pair every fallback with a restore drill.
- **Prove/refute:** Break the primary path; fallback must surface DEGRADED, preserve the evidence, and pass a restore check after recovery.
- **Card proof:** `2bdb3fbd4bfa05e98a47a261f50013c1330032a2933146d11c5c9b067f51a59c`

### shadow-before-intervention

- **Transfer:** `direct`
- **Rule:** For reversible but high-cost interventions, run a shadow model against live observations before changing the live controller.
- **Studio change:** Add shadow-mode stage to systems changes: baseline → shadow prediction → divergence threshold → human decision → live rollout.
- **Prove/refute:** Force shadow/live divergence beyond threshold; rollout must block and attach the divergence evidence.
- **Card proof:** `7af76d7b00a8fd678c0296da0c669c83a8dc29a7772a2e1ddf4ec25db8b6672e`

### sociotechnical-boundary-review

- **Transfer:** `direct`
- **Rule:** Automation changes are assessed against incentives, human override, ownership, and technical boundary behavior together.
- **Studio change:** Every systems intervention packet names affected human roles, incentives changed, override route, and social failure signal.
- **Prove/refute:** Remove the human owner or override route; approval must fail as incomplete boundary design.
- **Card proof:** `a3ec50c4fed58876e951c90f050c774b08e3e69bac6621034a79f7f64a75dea8`

### archetype-before-remedy

- **Transfer:** `structural`
- **Rule:** Classify the recurring behavior (constraint, shifting burden, limits-to-growth, feedback delay) before selecting a remedy.
- **Studio change:** Gap reports include archetype hypothesis, evidence, expected recurrence, leverage point, and a counter-archetype test.
- **Prove/refute:** Present a remedy without an archetype/evidence row; studio verifier returns NOT_READY.
- **Card proof:** `7e8a934e40c05921eceb5afc3f67a711c4a09c375802bb6a8f8c13bf291483e0`
