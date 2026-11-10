---
source: https://www.youtube.com/watch?v=4_5I9uysrRY
video_id: 4_5I9uysrRY
channel: JAX London
title: "Beyond the Spotify Model: using Team Topologies for fast Flow and Organisation Evolution"
scraped: 2026-08-28
tags: [organizations, team-topologies, cognitive-load, conways-law, software-delivery]
---
# Beyond the Spotify Model: using Team Topologies for fast Flow and Organisation Evolution

The talk argues that the 2012 Spotify model is a snapshot, not a blueprint, and introduces Team Topologies as a way to design team types, interaction modes, and platforms around cognitive load and Conway's law to achieve fast, sustainable flow.

## Procedure / models distilled
- Map the Spotify model's four constructs: a squad is a cross-functional team aligned to one business domain slice; a tribe is a family of related squads; a chapter is same-skill people within a tribe; a guild is a loose, interest-based community across the organization.
- Use cross-functional, domain-aligned squads to increase the flow of change by giving a single team end-to-end ownership of a feature or workflow.
- Clarify responsibilities by assigning ownership of specific domain slices to specific squads, reducing the ambiguity that often slows software delivery.
- Plan and budget for cross-team enablement deliberately via guilds, internal conferences, and tech talks rather than assuming collaboration will happen organically.
- Treat the Spotify model as a time-bound snapshot, not a fixed template; Spotify itself later said "there is no Spotify model," so copy the principles, not the labels.
- Size teams by managing cognitive load: minimize the mental effort spent on deployment rituals, environment setup, and unrelated knowledge so teams can focus on business problems.
- Apply Conway's law as a strategic constraint: the communication paths in the organization strongly shape the architecture you can build, so design org structure to match the desired software structure.
- Use reverse or inverse Conway maneuvers: change the organization's layout and team relationships to make a target architecture feasible.
- Choose from only three core team interaction modes: collaboration for time-bounded discovery, X-as-a-service for ongoing consumption with strong provider-side developer experience, and facilitating for building another team's capabilities.
- Make every interaction temporary and purposeful; switch from collaboration to X-as-a-service once APIs and ownership are clear, because permanent collaboration signals missing boundaries or capabilities.
- Listen to interaction quality as an organizational signal: awkward or excessive communication between teams usually means the software boundaries are wrong or a capability is missing.
- Build a thinnest viable platform that is just big enough to help consuming teams succeed, including documentation, onboarding, examples, mocks, stubs, and test harnesses, rather than large, forced platforms.
- Evolve team topology continuously by detecting triggers such as rising cognitive load, communication overload across boundaries, or strategic shifts in architecture.

## Failure modes named
- Adopting the 2012 Spotify model as a complete, permanent solution to software delivery problems.
- Ignoring the blog post disclaimer that the model was already a snapshot in progress.
- Overlooking cognitive load, leading to teams overwhelmed by unrelated tools, deployment complexity, and knowledge.
- Ignoring Conway's law and letting the existing org structure constrain the architecture to designs the organization can easily produce.
- Treating team interactions as permanent rather than situational, forcing collaboration where X-as-a-service or facilitation would be better.
- Building large, monolithic platforms that are hard to use and slow teams down instead of starting with the thinnest viable platform.
- Failing to listen for signals that current team boundaries or capabilities are wrong, such as excessive cross-team communication.
- Allowing ambiguity over who owns what domain slice, which produces coordination waste and slows delivery.

## Studio relevance
03 diagnose - use this card to map current team boundaries, interaction modes, cognitive load, and Conway's-law constraints against the flow the organization is trying to achieve.
