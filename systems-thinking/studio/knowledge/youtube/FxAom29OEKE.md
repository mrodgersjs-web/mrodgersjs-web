---
source: https://www.youtube.com/watch?v=FxAom29OEKE
video_id: FxAom29OEKE
channel: Kiki's Bytes
title: "I ACED my Technical Interviews knowing these System Design Basics"
scraped: 2026-08-28
tags: [engineering, system-design, distributed-systems, databases, interviews]
---
# I ACED my Technical Interviews knowing these System Design Basics

The video introduces core system-design fundamentals—scalability, reliability, availability, efficiency, CAP theorem, load balancing, caching, SQL vs NoSQL, indexing, and partitioning—using a social-media-platform example to illustrate how to evolve a single-server design into a distributed architecture.

## Procedure / models distilled
- Start with a minimal single web server and one database, then evolve toward a distributed system as load grows.
- Scale horizontally by adding more servers, or vertically by upgrading existing hardware, depending on demand.
- Evaluate distributed systems through four characteristics: scalability, reliability, availability, and efficiency, balancing their inherent trade-offs.
- Apply the CAP theorem: during network partitions, guarantee only two of consistency, availability, or partition tolerance.
- Insert load balancers between users/web servers, web/app servers, and app/databases; distribute traffic with least-connections, round-robin, or IP-hash algorithms.
- Deploy a standby load balancer to prevent the load balancer itself from becoming a single point of failure.
- Add application caches and CDNs for static media, exploiting temporal locality to reduce latency, then manage consistency against the source of truth.
- Select cache write and eviction policies to match consistency, latency, and capacity needs: write-through, write-around, write-back, LRU, FIFO, and LFU.
- Choose SQL when strong ACID compliance and stable schemas matter; choose NoSQL for flexible schemas, unstructured data, and horizontal scalability.
- Use primary, secondary, and composite indexes to accelerate reads, while accepting slower writes due to index-maintenance overhead.
- Partition data horizontally, vertically, or via directory-based lookup when vertical scaling is exhausted; use key/hash, list, round-robin, or composite partitioning schemes.
- Apply consistent hashing across a hash ring so adding or removing servers minimizes the amount of data that must be remapped.
- Monitor the trade-offs introduced by each technique: caching versus consistency, indexing reads versus write speed, and partitioning scale versus join/rebalance complexity.

## Failure modes named
- A single-server, single-database design cannot scale as user demand grows.
- One server receiving disproportionate traffic can become overwhelmed without a load balancer.
- A load balancer itself can become a single point of failure if it lacks a standby.
- Serving stale data from cache if it is not kept in sync with the source of truth.
- Data loss risk with write-back caching if the system fails before flushing to storage.
- Cache flooding if writes frequently populate the cache unnecessarily.
- Unintended index bloat slowing down writes because every insert/update/delete must update indexes.
- Attempting to scale a database vertically forever until hardware limits are hit.
- Cross-partition joins and data rebalancing become difficult after partitioning.

## Studio relevance
02 frame - provides a shared vocabulary of scalable-architecture primitives and trade-offs for framing system-design decisions.
