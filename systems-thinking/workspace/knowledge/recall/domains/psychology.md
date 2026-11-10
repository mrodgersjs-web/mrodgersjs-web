> Cards tagged: 93 · Content sources: mirror 79 / API 65

# Psychology — Jake PAI knowledge pack

Operating layer for `/jake` (Prime Conductor). 93 spine cards. 79 have local mirrors; 14 have none. Most mirrors are import stubs (title + frontmatter only), so content was filled with four exhaustive Recall searches (`cognitive bias persuasion`, `habits identity motivation`, `Cialdini Kahneman`, `founder psychology`) plus `card` fetches. Cite 32 strongest cards below. Never invent cards or URLs.

## Motivation, dopamine, flow, and finishing

- Kahneman–Tversky prospect value is stored as `v(x) = x^α` for gains and `v(x) = −λ(−x)^β` for losses, with `α ≈ 0.88`, `β ≈ 0.88`, `λ ≈ 2.25` (losses hurt ~2.25× equivalent gains) and probability weighting `w(p) = p^γ / (p^γ + (1−p)^γ)^{1/γ}` with `γ ≈ 0.65` (overweight small probabilities). Overall prospect value `V = Σ w(pᵢ)·v(xᵢ)`. [Card: This Dopamine Trick Will Make You Addicted To Studying](https://www.youtube.com/watch?v=QVWINTeyUOk)

- Reactance: `R ∝ FreedomImportance × ThreatMagnitude × FrequencyOfThreat`; restricted desire `DesiredValue(restricted) = DesiredValue(free) × (1 + R)`. Above a threshold, persuasion boomerangs. Scarcity stacks: `PerceivedValue = BaseValue × (1 + R_scarcity) × (1 + R_restriction)`. Same card maps variable-ratio selection (generate 32 candidates, pick 1) as the addictive schedule. [Card: This Dopamine Trick Will Make You Addicted To Studying](https://www.youtube.com/watch?v=QVWINTeyUOk)

- Chase / gatekeeper: reactance intensity `RI = (Perceived Restriction × Freedom Threat) / Accessibility` (each 1–10). Loss-frame magnitude `LFM = |Potential Loss| × 2.25 × Certainty Weight`. Fogg trigger `B = MAP` (Motivation × Ability × Prompt) must spike at the same moment. Carpenter 2013 meta-analysis (42 studies): adding “but you are free to refuse” *increases* compliance. Four-move gatekeeper: qualify the buyer, don’t chase. Terror Management Theory (Greenberg, Pyszczynski, Solomon, 1986) sits under “why they hire you.” [Card: This ONE Psychological Trigger Gets Clients to Chase You](https://www.youtube.com/watch?v=VjyDi69NbVc)

- Implementation intentions beat goals: “If it’s Monday at 7:00 a.m., then I’m at the gym.” Goal setters failed 62% of the time; if-then planners failed 9%. [Card: How to Trick Your Brain to Crave Hard Things (It's Almost Unfair)](https://www.youtube.com/watch?v=okf8Ykmv5sk)

- Finish-line dopamine is not start-line novelty. Isolate the first 10 seconds of a 3-hour edit so the nervous system registers a completion win and rewires toward that action. [Card: The Elite System to Finish Everything You Start | How to Force Your Brain to Crave the Finish Line](https://www.youtube.com/watch?v=n4mQg6aNilg)

- Flow (Csikszentmihalyi): stay in the challenge–skill channel; below it is boredom, above it is anxiety. Visualization pre-wires patterns; pattern-match at performance time can release dopamine and drop you into flow (Bannister effect: impossible → probable once seen). Kotler: train via neurobiology (repeatable mechanism), not metaphor. [Card: The science of effortlessness: How to activate flow | Steven Kotler: Full Interview](https://www.youtube.com/watch?v=RZIn9tfeQ2I) · [Card: A Neuroscience Trick To Achieve Literally Anything](https://www.youtube.com/watch?v=7khRkfAQU7I)

- Schooling reinforces isolated-fact recall with “hundreds upon hundreds” of dopamine hits; later work demands long-term, compositional use. Retrain the reinforcement, not just the content. [Card: How to Use Neuroscience To Learn Skills Like The Top 1%](https://www.youtube.com/watch?v=xIcvQBw7ec4)

## Cognitive bias, defense, and calibrated thinking

- Availability: overweight what’s easy to retrieve. Confirmation: accept agreeing evidence, filter the rest. Defense: admit the bias is in *your* head; use RCTs and peer review as bias-reduction machinery (Crash Course / HHMI BioInteractive). [Card: Introduction to Cognitive Bias: Crash Course Scientific Thinking #1](https://www.youtube.com/watch?v=d2r7Bk1NlgU)

- Influence map from the twisted-tricks transcript: anchoring, Ben Franklin effect, cognitive dissonance, status-quo / default bias, reciprocity, reverse psychology. Dissonance: small actions shift identity then compliance (~01:02:52). Reactance: autonomy threat → pushback (~00:09:38). Repetition can make claims feel true (~02:21:03). Fear-then-relief drops resistance (~02:23:44). Belief Integrity Check: what is being repeated, who benefits, did I believe this before, what evidence exists outside the message, am I complying because fear just dropped? [Card: 3 Hours of Psychological Tricks So Twisted, They’ll Change How You Think](https://www.youtube.com/watch?v=z4fLdL9Y0_U) · [Card: iCanStudy](https://www.icanstudy.com/)

- Prospect-theory offer design (from the same iCanStudy / Kahneman notes): frame cost of inaction, risk of staying the same, downside protection, avoided loss, reduced uncertainty. Diagnose: what loss are they protecting, what is the reference point, is comfort-loss scarier than future gain? [Card: iCanStudy](https://www.icanstudy.com/)

- Thinking toolkit (from the iCanStudy notes): expected value, probabilistic thinking, checklists, framing, availability control, reversal, default effect, cognitive-load management, emotion labeling, cognitive diffusion. Pattern detector: “three times is a rule.” Fogg + COM-B as the Behavior Debugger. [Card: iCanStudy](https://www.icanstudy.com/)

- PsyShield / HumanOS stack: HumanOS (behavioral engine), PsyGraph (motives/incentives), Bias Firewall, PsyShield (manipulation defense), Reality Compass (narrative distortion), Influence Map (ethical vs manipulative), Behavior Debugger (Fogg + COM-B). Next 10× is protection against bad conclusions, not more information. [Card: PsyShield + HumanOS: Behavioral Science and Manipulation Defense Layer for REB+ and ADTB+](https://github.com/NVIDIA-NeMo/Guardrails)

- Reality Anchor claim-pressure harness flags `will / always / never / proven / guaranteed / best / only / most`; `evidence_ratio = supported_claims / claims`. Fake understanding is a gate, not a vibe. [Card: RIG Engine Recipe 02 — Reality Anchor](https://consensus.app/)

## Learning, memory, analogical intelligence, metacognition

- Analogical thinking operates on *structural* similarity, not surface. Historical transfers: Darwin ← Malthus; Rutherford atom ← solar system; Kepler light ← planetary motion; Maxwell electromagnetism ← fluids. Analogical tests are among the best single predictors of fluid intelligence (A:B :: C:D). Hold the analogy lightly; drop it when evidence says the structure is wrong. Pattern-library size is the intelligence bottleneck. [Card: The Purest Form of Intelligence: Analogical Thinking](https://www.youtube.com/watch?v=Z1uzAC4XDZA)

- “Pattern weaver” vs specialist: collect threads across domains; curiosity here is not ADHD. Integration-age advantage is the diverse toolkit, not depth-only. [Card: If You Have Too Many Interests, You Have The “Pattern Weaver” Mind](https://www.youtube.com/watch?v=M_Ym61SEM0o)

- CIA-style learning: emotion + repetition = retention; timers create controlled urgency; cover-identity (act as the competent speaker) drives behavior; review via notes + spoken summaries + simulated scenarios; intensity in short bursts, mastery as marathon. Interrogate understanding by explaining in simple words / teaching / using new terms in real sentences. [Card: Learn Like a Spy: The CIA’s Secret Method to Learn Faster (It Works Scary Fast)](https://www.youtube.com/watch?v=rOLmfGg6wX0)

- Memory selection: excitation/inhibition create narrow windows; day’s traces compete; strongest patterns (most significant events) win replay, compressed “fast-forward.” Design encoding so the pattern you want is the strongest competitor at replay. [Card: How Your Brain Chooses What to Remember](https://www.youtube.com/watch?v=ceFFEmkxTLg)

- Biological learning ≠ backprop. Credit assignment in tissue is closer to hierarchical predictive coding (each layer predicts the layer below; energy-based relaxation). Unsigned |δ| still tags memory. [Card: The Brain’s Learning Algorithm Isn’t Backpropagation](https://www.youtube.com/watch?v=l-OLgbdZ3kk)

- Metacognition: treat emotion-regulation as a think-about-thinking loop (not “feel better”). Analogical library + deliberate mismatch with the standard toolkit is the creative transfer skill. [Card: The Secrets of Metacognition](https://www.youtube.com/watch?v=p6P11e32iW4)

## Influence, negotiation, power, social intelligence

- Negotiation stack: **Anchoring** — first number becomes the reference; go first with a bold-but-believable figure. **Mirroring** — repeat last few words as a question; they explain more. **Tactical silence** — let them fill the gap. **Flinch** — authentic “that’s higher than I expected” forces justification. Good-cop/bad-cop is a two-role constraint play. [Card: Every Negotiation Tactic & How To Use Them Yourself, Explained](https://www.youtube.com/watch?v=90svIa07ilQ)

- Carnegie Principle 12: throw down a challenge. Schwab: the desire to excel, not money-getting. Herzberg: what motivated workers most was not money, perks, or praise. [Card: How to Win Friends and INFLUENCE People (Complete Animated Book Summary)](https://www.youtube.com/watch?v=rvgS9jTGbp4)

- Greene option-control: multiple paths that all terminate at your outcome; dilemma by lighting the preferred option; pressure by making alternatives worse over time (inaction as the bigger risk). Law 32 fantasies: instant change, escape, unity, reversing the unchangeable — never sell gradual hard work as the fantasy. Law 17: Nixon “Madman Theory” / 1972 bombings — unpredictability as leverage because humans crave patterns. [Card: The 48 Laws of Power by Robert Greene | Complete Animated Book Summary](https://www.youtube.com/watch?v=3Ai3WkzeZEc)

- Machiavelli modern: bait with greed/ego/fear; fight on your terrain; press the specific weakness (impatience, pride, desperation). After a win, do not let the crowd pick the next fight. Disrespect handling is non-reactive: they become predictable; you keep the option set. [Card: Machiavelli - The Art of Power in The Modern World](https://www.youtube.com/watch?v=Y7ExXLcy26s)

- Social intelligence: STOP technique + prewritten responses to hot buttons. Hierarchies now track perceived value contribution. Power channels: formal authority, expertise, social connection, charisma (Keltner, Berkeley). Roles rewrite behavior (Stanford Prison as caution; HBS: role changes decisions and personality expression). Ethical persuasion test: does it *empower* the other person’s choice? [Card: Social Intelligence: Mastering The Psychology Of Human Behavior (Audiobook)](https://www.youtube.com/watch?v=CsXKAC4iYG4)

- Dark-psychology corpus is ingested as a *defense* dataset (PsyShield), not a playbook to run on customers. [Card: PsyShield + HumanOS: Behavioral Science and Manipulation Defense Layer for REB+ and ADTB+](https://github.com/NVIDIA-NeMo/Guardrails)

## Brand, design, peak–end, and desire architecture

- Premium brands (Nike, Ralph Lauren, Lululemon): first step is psychology mapping — the customer’s exclusivity triggers — not a logo polish. Three-step process starts with research/profile, then positioning. [Card: The Psychology of Premium Branding](https://www.youtube.com/watch?v=1kcxUhjuW_0)

- Brand-love principles in the tape: delusional self-belief (Jordan using criticism as fuel); mastery as decades (Jiro Ono, 70 years); Jobs simplicity — three buttons → one → buttonless vs BlackBerry/RAZR. [Card: the psychology of building a brand everyone loves](https://www.youtube.com/watch?v=6V4y0AX69h4)

- Graphic-design psych: high-contrast geometric reduction (Apple, Squid Game guards); color salience + variable reward (red notification dots); Gestalt for clean nav; FOMO copy as explicit scarcity language. Squares/rects → order/stability for informative layouts. [Card: The ONLY Graphic Design Psychology Video You’ll Ever Need!](https://www.youtube.com/watch?v=wBaTNvs8enw)

- Peak–end (Kahneman remembering-self): `EAS = (Peak_Intensity × End_Intensity) / Emotional_Flatline_Duration` (intensities 1–10). Site/deck must contain one unmistakable peak demonstration (trailer, live proof, before–after, motion thesis, mechanism reveal) and a CTA that leaves residue. [Card: RIG Website Design Scoring Algorithm V2: Motion Thesis + Peak-End Demonstration Doctrine]()

- Voltage / selling sequence: Wound → Mirror → Autonomy → Qualification → Open Loop. Variable-ratio reveal: `P(reward on trial k) = (1−p)^{k−1} p`, `E[n] = 1/p`. Do not dump all value at once. TD error on the page: `TD_Error = reward_t + γ·Value(next) − Value(current)`. [Card: RIG OS Behavioral Voltage Doctrine: Dopamine Loading, Desire Architecture, and Product Selling Gates](https://doi.org/10.1073/pnas.1820145116)

## RIG behavioral engines (fleet-operable recipes)

Peer-reviewed mapping (Consensus, 50 included papers / 170M-paper search) is the math spine for scoring:

- **RPE:** `δₜ = rₜ + γ·V(sₜ₊₁) − V(sₜ)`. Evidence 10/10 — 2,316 participants across 102 fMRI studies (Fouragnan et al., 2018); Schultz / Eshel / Watabe-Uchida on dopamine. Unsigned |δ| encodes memory (Liu 2025; Ergo 2020; Rouhani 2024). Both +20 Detonation and −20 Erosion create trace — a one-word “Pass” can match a 500-word manifesto on |δ|. [Card: RIG Proprietary Process: Peer-Reviewed Mathematical Foundations — RPE, Bayesian Surprise, Reactance, Spacing, Entropy — Mapped to BDF30, IDP, and All Scoring Gates](https://consensus.app)

- **Bayesian surprise:** `S = D_KL(P_post || P_prior)`. Itti & Baldi 2005: 72%+ of gaze shifts to high-surprise regions; beats Shannon surprise for attention. [Card: RIG Proprietary Process: Peer-Reviewed Mathematical Foundations — RPE, Bayesian Surprise, Reactance, Spacing, Entropy — Mapped to BDF30, IDP, and All Scoring Gates](https://consensus.app)

- **Spacing / compounding:** `MemoryCompoundingScore = 0.30·DoctrineThreadContinuity + 0.25·OptimalSpacingAdherence + 0.25·CatchphraseRecurrence + 0.20·VillainClassConsistency`; gate `≥ 0.60` for series posts; ISI within 10–20% of target retention. [Card: RIG Proprietary Process: Peer-Reviewed Mathematical Foundations — RPE, Bayesian Surprise, Reactance, Spacing, Entropy — Mapped to BDF30, IDP, and All Scoring Gates](https://consensus.app)

- **Zeigarnik Residue:** productive open loops, not anxiety captivity. 10-layer: current question → useful tension → open loop → defined payoff → next step → strip clickbait → preserve autonomy → test usefulness → score → rewrite. [Card: RIG Engine Recipe 13 — Zeigarnik Residue](https://consensus.app/)

- **Social Proof Density:** reject generic phrases (`trusted by`, `loved by`, `industry-leading`, `world-class`, `thousands of customers`, `proven results`, `best-in-class`). Specificity markers: `%`, `days/weeks/months`, `before/after`, `reduced/increased`, `from/to`, `measured`, `baseline`. Coverage = fraction of claims that have a linked proof. [Card: RIG Supplemental Engine Recipe — Social Proof Density](https://consensus.app/)

- **Autonomy Calibration:** enlarge choice, surface tradeoffs, human override, exit path, no coercive dependency. “A good system makes the human more capable, not more captured.” [Card: RIG Engine Recipe 11 — Autonomy Calibration](https://consensus.app/)

- Related recipe souls (use as scoring axes, not slogans; recipes exist on the spine but were not all cited): Cognitive Sovereignty, Confidence Calibration, Hedonic Adaptation Resistance, Opponent Process (contrast pair + aftertaste), Somatic Marker, Predictive Error Calibration, Memory Residue, Voltage Reactor.

## Open gaps

- **Mirror quality:** 79/93 have `mirror_path` and all 79 files exist, but only ~9 mirrors contain real body text. Do not treat “has mirror” as “has transcript.”
- **No-mirror remainder (14)** still thin after search: Dostoevsky sleep lecture, “The World Feels Wrong…”, `awesome-persona-distill-skills`, Unified Deviation Engine V4, Schopenhauer “idiots,” “Become Dangerously Focused,” Mind-F*ck Paradoxes, Email Drafting Protocol, “Game of Life Wrong,” Communications Deviation Engine V2 (partial). Fetch `card <id>` before using them in product copy.
- **Cialdini named 7** (reciprocity, commitment/consistency, social proof, authority, liking, scarcity, unity) are *applied* across chase/reactance/social-proof cards but there is no dedicated Cialdini primary. Kahneman is present as math, not as a *Thinking, Fast and Slow* card.
- **Habits/identity:** if-then plans and Carnegie/Herzberg are here; no Clear/Duhigg atomic-habit primary, no Kegan adult-development primary, no Dweck original.
- **Empty `source_url` on several RIG ops cards** (Peak-End V2, Feynman X-Ray Raw, Presentation Doctrine, several website/email scorers). Cite by title; do not invent a DOI.
- **YouTube-summary layer** (48 Laws, Carnegie, dark psychology) is compressed and often YouTuber-framed. Prefer RIG math cards + Crash Course + Kotler + analogical-thinking when the fleet needs a source of record.
- **Founder psychology** search mostly hit adjacent GTM/brand cards, not a founder-mental-health or decision-under-uncertainty set.
