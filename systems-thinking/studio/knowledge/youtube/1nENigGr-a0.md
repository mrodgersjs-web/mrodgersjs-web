---
source: https://www.youtube.com/watch?v=1nENigGr-a0
video_id: 1nENigGr-a0
channel: ByteByteGo
title: "System Design Was HARD - Until You Knew the Trade-Offs"
scraped: 2026-08-28
tags: [engineering, databases, distributed systems, scalability, data processing]
---
# System Design Was HARD - Until You Knew the Trade-Offs

The video explains that system design is fundamentally about choosing trade-offs across data storage models, database normalization, distributed consistency guarantees, and data processing paradigms to align architectural decisions with application requirements.

## Procedure / models distilled
- Use the SQL vs NoSQL decision framework: choose SQL for strong consistency, structured schemas, and complex queries; choose NoSQL for horizontal scalability and schema flexibility.
- Apply normalization to minimize redundancy and preserve data integrity when correctness and simplicity dominate.
- Apply strategic denormalization to eliminate expensive joins and accelerate reads where query performance demands it.
- Recognize that denormalization optimizes read performance at the cost of increased write complexity and potential inconsistency.
- Apply the CAP theorem during distributed system design: under network partitions, consciously choose consistency or availability based on domain requirements.
- Navigate the consistency spectrum: prefer strong consistency when immediate accuracy matters; prefer eventual consistency when speed and scale matter more than temporary staleness.
- Select batch processing for computational efficiency and simpler error handling when latency is acceptable.
- Select stream processing for real-time responsiveness, while planning for out-of-order data, variable latency, and sophisticated state management.
- Design hybrid data architectures that use streams for time-sensitive processing and batch jobs for comprehensive analysis.

## Failure modes named
- Treating SQL or NoSQL as universally superior instead of matching the database to workload needs.
- Keeping fully normalized schemas at scale while ignoring prohibitive join costs.
- Denormalizing without accounting for increased write complexity and potential data inconsistency.
- Treating consistency as a binary property rather than a spectrum from strong to eventual.
- Ignoring the CAP theorem trade-off when designing distributed systems.
- Choosing batch processing in scenarios that require real-time reaction to events.
- Adopting stream processing without handling out-of-order arrivals, variable latency, and state management.

## Studio relevance
02 frame - provides a decision matrix for selecting data architecture patterns based on workload requirements, constraints, and the maturity stage of the system.
