---
source: https://www.youtube.com/watch?v=Ug4F01ghcrQ
video_id: Ug4F01ghcrQ
channel: Database Podcasts
title: "Episode 11 – Organizational Design & Conway’s Law 🏢➡️💻 | @DatabasePodcasts"
scraped: 2026-08-28
tags: [organizations, conways-law, software-architecture, team-design, communication]
---
# Episode 11 – Organizational Design & Conway’s Law 🏢➡️💻 | @DatabasePodcasts

Conway’s Law states that a system’s architecture mirrors its organization’s communication structure, making team design a first-class architectural decision.

## Procedure / models distilled
- **Apply Conway’s Law as a diagnostic lens:** treat the current software architecture as a fossil record of how teams actually communicate and where information flows or stalls.
- **Map org-chart shapes to architectural outcomes:** rigid hierarchical structures tend to produce tightly coupled monoliths; networks of autonomous teams tend to produce modular, service-oriented systems.
- **Model communication cost combinatorially:** recognize that communication channels grow as n(n-1)/2, so a 3-person team has 3 channels, a 5-person team has 10, and an 8-person team has 28.
- **Use the two-pizza team rule:** keep teams small enough that two pizzas can feed them, deliberately constraining communication overhead.
- **Execute the reverse Conway maneuver:** first define the target system architecture, then restructure teams to mirror that architecture.
- **Form teams around business capabilities, not technology layers:** assign each team ownership of a clear business domain rather than a horizontal function like front-end or database.
- **Empower teams with end-to-end ownership:** give each team the authority and skills to make decisions without constant permission-seeking.
- **Build cross-functional teams:** include product, design, coding, and operations skills inside the same team so it can fully own its service.
- **Adopt a “you build it, you run it” philosophy:** make each team responsible for both building and operating its service.
- **Treat org-chart lines as architectural lines:** consider team boundaries, reporting lines, and communication pathways to be as consequential as code boundaries and interfaces.
- **Audit current team structure before designing systems:** examine team size, communication patterns, and bottlenecks to predict what architecture they will naturally produce.

## Failure modes named
- **Assuming architecture is independent of organization:** treating org design as “soft stuff” while assuming technical design can be optimized in isolation.
- **Throwing people at a deadline:** adding members to a team under the belief it will speed delivery while ignoring the combinatorial explosion of coordination overhead.
- **Allowing monolithic org structures to persist while targeting microservices:** hoping for modularity in code while teams remain siloed and hierarchically coupled.
- **Oversized teams:** creating teams too large to feed with two pizzas, increasing alignment cost and reducing time spent producing value.
- **Horizontal, technology-layer teams:** organizing by function rather than business capability, which fragments ownership and produces integration bottlenecks.
- **Disempowered teams without full skill coverage:** expecting teams to own services when they lack decision rights or the product/design/ops skills needed to run them.
- **Ignoring communication bottlenecks:** failing to see stalled or forced information flows as early warnings of future architectural coupling.

## Studio relevance
02 frame - how the studio uses this card
