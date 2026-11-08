---
source: https://www.youtube.com/watch?v=BYIIyjlKed0
video_id: BYIIyjlKed0
channel: Professor Messer
title: "Redundancy, Fault Tolerance, and High Availability - CompTIA Security+ SY0-301: 2.7"
scraped: 2026-08-28
tags: [engineering, redundancy, fault-tolerance, high-availability, infrastructure]
---
# Redundancy, Fault Tolerance, and High Availability - CompTIA Security+ SY0-301: 2.7

This video explains how organizations maintain uptime by layering redundant hardware, disk arrays, power protection, server clusters, load balancing, and standby spares so that component failures do not interrupt service.

## Procedure / models distilled
- Distinguish redundancy from high availability: redundancy means spare components exist to take over, but failover may require manual intervention, whereas high availability means systems are continuously online and automatically absorb a failure without user-visible interruption.
- Deploy redundant hardware at multiple layers, including duplicate servers, power supplies, motherboards, routers, firewalls, and wide-area network links, so any single failure has a backup path.
- Pair monitoring software with clustered applications so that if one software instance fails, another instance on the network can detect the outage and pick up the workload.
- Protect against power loss with uninterruptible power supplies (UPS) that use batteries to keep systems running when utility power becomes unstable or drops.
- Implement RAID inside servers to survive disk failures: RAID 0 stripes data across disks for performance but offers no fault tolerance; RAID 1 mirrors identical copies across disks; RAID 5 stripes data and adds parity so the array survives the loss of any single drive with better storage efficiency than mirroring.
- Combine RAID levels, such as RAID 0+1 or RAID 5+1, to blend striping, parity, and mirroring depending on the required balance of performance, capacity, and fault tolerance.
- Build server clusters with shared backend storage and continuous inter-node communication so that remaining nodes can detect an outage and take over resources automatically.
- Use active-active clusters where every node simultaneously serves users and balances load; if one node fails, the remaining active nodes continue handling traffic without a manual switch.
- Use active-passive clusters where one node actively serves users while an identical node stays on standby; the passive node promotes itself automatically when it detects the active node has disappeared.
- Balance load across multiple active systems so that surviving systems already carry part of the traffic and can absorb the failed node’s share without requiring a separate power-up step.
- Maintain spare servers at graduated readiness levels: cold spares are stored unconfigured, warm spares are racked and periodically updated but manually activated, and hot spares are always on and often configured for automatic takeover.

## Failure modes named
- Hardware failures: loss of a server, router, power supply, motherboard, or disk.
- Software failures in standalone or clustered applications.
- Power outages and unstable utility power, such as frequent thunderstorms causing intermittent electricity.
- Misconception that having redundant components automatically equals high availability.
- RAID 0 array unavailability: losing any one striped disk without parity destroys the entire logical volume.
- Active node failure in a server cluster.
- Manual failover delays when redundant systems are not designed to switch over automatically.

## Studio relevance
04 leverage - the studio uses this card to design resilient systems that keep services continuously available by selecting the right mix of redundancy, RAID, clustering, load balancing, and spare strategies for each anticipated failure mode.
