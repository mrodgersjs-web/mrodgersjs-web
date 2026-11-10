---
source: https://www.youtube.com/watch?v=Fd3985TqCgA
video_id: Fd3985TqCgA
channel: InfoQ
title: "How Many Is Too Much? Exploring Costs of Coordination During Outages"
scraped: 2026-08-28
tags: [organizations, incident-response, coordination, cognitive-load, software-engineering]
---
# How Many Is Too Much? Exploring Costs of Coordination During Outages

This talk reframes incident response as a dual cognitive-and-coordination workload, arguing that rigid command-and-control models and coordination tools often increase attentional costs, while adaptive, anticipation-based coordination built on shared common ground resolves incidents more effectively.

## Procedure / models distilled
- Map the dual workload during incidents: cognitive work (perceive, remember, reason, focus, act) plus coordinative work (find experts, brief them, allocate tasks, estimate time, manage deferrals).
- Recognize software-specific coordination demands: continual environmental change requires ongoing learning; interactive complexity requires multiple experts; speed and scale require coordinating diverse perspectives in real time.
- Track the incident lifecycle as an expansion-contraction pattern: uncertainty expands the responder set, which raises coordination costs that must then be actively managed.
- Treat coordination as a resource trade-off: more responders provide more partial models and expertise, but each adds attentional cost; the goal is joint benefit without coordination overload.
- Replace the traffic-light model of incident command with an adaptive choreography model: responders anticipate each other's next moves like drivers negotiating an uncontrolled intersection.
- Build common ground before incidents: shared knowledge, beliefs, and assumptions enable terse, high-density communication during response.
- Match coordination strategy to incident type: the same control structure is not optimal for every incident; adaptive strategies reduce coordination costs.
- Audit tooling for hidden coordination costs: tools intended to reduce coordination may add new attentional burdens by fragmenting context or introducing extra signaling steps.
- Bring authority figures into the incident loop rather than allowing them to redirect from outside, so trade-offs and competing priorities become visible to the response team.
- Invest in learning after incidents by examining patterns that made the problem harder or easier and how the team's responses helped or hindered, rather than stopping at root cause.

## Failure modes named
- Incident commander bottleneck: a single commander centralizing decisions can slow resolution when incidents require fast, distributed adaptation.
- Tooling-induced coordination debt: collaboration tools add extra communication and context-switching overhead despite being designed to reduce it.
- Distributed-equals-co-located fantasy: assuming geographically distributed teams can coordinate with the same bandwidth and subtlety as co-located teams.
- Standing-waiting-for-the-coach: responders passively awaiting direction instead of staying poised to adapt.
- Low-common-ground communication bloat: lack of shared mental models forces lengthy explanations during time-pressured incidents.
- Authority redirect without context: executives or other stakeholders jumping in to redirect work without being embedded in the response.
- Root-cause-only review: post-incident analysis focuses narrowly on technical cause and misses patterns of coordination that amplified or reduced harm.

## Studio relevance
03 diagnose - the studio uses this card to map how coordination structures, role designs, and tools shape the attentional load on responders during incidents.
