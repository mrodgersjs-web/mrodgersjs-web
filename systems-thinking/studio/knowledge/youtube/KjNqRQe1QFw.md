---
source: https://www.youtube.com/watch?v=KjNqRQe1QFw
video_id: KjNqRQe1QFw
channel: Dylan Beattie
title: "Moore's Law, Amdahl's Law, Conway's Law - and why we need to stop having meetings`"
scraped: 2026-08-28
tags: [organizations, scaling, distributed-systems, communication, software-architecture]
---
# Moore's Law, Amdahl's Law, Conway's Law - and why we need to stop having meetings`

The convergence of Moore's Law, Amdahl's Law, and Conway's Law implies that scalable software requires organizations to remove serial communication bottlenecks—especially meetings—from both their teams and their systems.

## Procedure / models distilled
- Moore's Law: transistor count per integrated circuit roughly doubles every two years, driving exponential growth in compute capacity.
- The multicore divergence: around 2005 the industry hit physical limits on single-core clock speed (~4 GHz), so total CPU transistors kept growing by adding cores rather than making one core faster.
- Scaling up vs. scaling out: modern computing shifted from buying bigger mainframes to running many small backend instances that can be added on demand.
- Parallelization as a design requirement: software must split work into small, autonomous units that can be distributed across cores/instances and have their outputs combined.
- Amdahl's Law: the theoretical speedup from parallelization is capped by the fraction of the workload that cannot run in parallel.
- The "roast turkey" analogy: some tasks have a fixed minimum duration no matter how many cooks or ovens you add.
- The "Christmas burrito" analogy: workloads that are fully parallelizable can scale quickly by adding resources, like spinning up cloud instances.
- Eliminate the "turkeys" in a system: remove serial, non-parallelizable tasks if you want to realize the benefits of distributed computing.
- Conway's Law: organizations design systems whose structure mirrors their own communication structure.
- The bank call-transfer example: when two departments don't communicate, the systems they build don't communicate either.
- Face-to-face conversation trade-offs: it is high-bandwidth and good for problem-solving but poor at preserving information for people outside the conversation.
- Optimize distributed communication for discoverability: trade a little short-term velocity for long-term efficiency by capturing decisions in durable, discoverable formats.
- Resilient distributed-system patterns: autonomous microservices and command-query separation work because components operate without constantly checking back with a central authority.
- Infrastructure-as-code parallel: Terraform/Pulumi/Bicep make scaling scripted, documented, and repeatable—qualities teams should emulate.
- Meetings don't scale: organizations that rely heavily on synchronous meetings tend to produce systems with matching serial bottlenecks.

## Failure modes named
- Hitting the single-core physical limit while assuming raw clock speed will keep growing.
- Adding resources to a system that contains unavoidable serial work and being surprised by limited speedup.
- Siloed departments building incompatible systems because their teams do not communicate.
- Holding long status meetings to relay information that could have been an email, ticket, or wiki entry.
- Blocking work while waiting for someone to reply with missing requirements or data sources.
- Treating "most efficient method of conveying information is face-to-face conversation" as a license to default to meetings rather than durable artifacts.
- Failing to capture solutions discussed in conversation, leaving others unaware of decisions.
- Requiring daily physical commutes that consume time without improving system design.
- Building non-parallelizable communication structures into teams and then replicating them as non-parallelizable system architectures.

## Studio relevance
03 diagnose - use this card to surface whether a client's scaling problems are rooted in serial team-communication bottlenecks that have been copied into their system architecture.
