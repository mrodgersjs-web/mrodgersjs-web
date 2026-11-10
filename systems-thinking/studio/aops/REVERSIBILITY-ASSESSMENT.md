# A_ops Cap + Chargeback — Reversibility Assessment

**Requested by:** Council run `20260828-200112` (unanimous DEFER, Munger DEALBREAKER).
**Unlocked by:** Mike Rodgers, operator authority, 2026-08-28 ("unlock it and go").
**BMS band:** D (outward effect on fleet behavior) — human approval granted, recorded here.

## What is being installed

1. **Measurement only, first**: an A_ops ledger (attention-minutes charged to causing
   agent/system), a scoreboard, and a gate command (`aops gate "<new thing>"`) that
   records the B4 justification for any new spawn/cron/node.
2. **No hard enforcement yet**: nothing is auto-killed, blocked, or refused in this
   install. The cap is *published*, not *enforced*. Enforcement (B3 overflow refusal)
   is a SECOND, separately-gated change that requires the OpenBot control plane.

## Reversibility analysis

| Component | Reversible? | How to undo | Cost of undo |
|---|---|---|---|
| Ledger + scoreboard (`aops` CLI) | Fully | `rm -rf ~/.rig/aops` + unlink wrapper | < 1 min, zero side effects — it only reads/writes its own files |
| Cap publication (config value) | Fully | `aops cap set unlimited` or delete config | < 1 min |
| Gate command on new spawns | Policy, not code | Stop calling `aops gate` | 0 min — it is advisory until B3 |
| B4 debit rule (documentation) | Fully | Remove from lattice/router docs | 0 min |
| B3 enforcement (NOT in this install) | Partially | Requires control-plane change | Would need its own assessment |

**Conclusion: the measurement layer is cleanly reversible** (its only effects are its
own files and published numbers). The council's concern attaches to B3 ENFORCEMENT,
which is explicitly deferred to the OpenBot control plane with its own gate.
The "this week" deadline concern is addressed by scoping this install to
measurement-only — nothing one-way ships this week.

## Kill criteria (per council)

If by **2026-09-04** the ledger shows attention-metering itself consuming >15
operator-minutes/day, or the numbers are too noisy to act on, uninstall
(reversible, above) and the DEFER verdict stands vindicated.
