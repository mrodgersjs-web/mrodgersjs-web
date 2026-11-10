---
source: https://www.youtube.com/watch?v=CtHrHII3AOk
video_id: CtHrHII3AOk
channel: Nicholas Andre
title: "Lecture - Topologies"
scraped: 2026-08-28
tags: [organizations, networking, topologies, osi-model]
---
# Lecture - Topologies

A lecture on the data link layer that uses highway traffic analogies to distinguish logical and physical topologies, and explains how collision-control mechanisms shape network performance.

## Procedure / models distilled
- Treat the OSI model as a responsibility map: changes at one layer (e.g., IPv4 to IPv6) do not force changes below it as long as the interface to the next lower layer is preserved.
- Divide the data link layer (Layer 2) into two sublayers: Logical Link Control (LLC) and Media Access Control (MAC).
- Distinguish logical topology (the rules/behavior of data transmission) from physical topology (the actual arrangement of devices and cables).
- Use a shared-highway analogy to reason about half-duplex media: only one direction of traffic at a time, so simultaneous movement causes collisions.
- Apply the collision-probability model: more nodes on a shared medium raise collision probability; collisions cause retransmissions, which raise collision probability again and degrade performance.
- Classify bus, star-over-hub, and hub-centered layouts as multi-access topologies because multiple nodes share the same medium.
- Add collision control to multi-access networks via CSMA/CD (Carrier Sense Multiple Access with Collision Detection) to sense and recover from collisions.
- Implement ring / token-ring topologies as deterministic systems: a token grants transmission rights, so only one device sends at a time and collisions are eliminated.
- Read each frame's destination 48-bit MAC address at every ring node; if the address does not match, forward the frame to the next node.
- Size ring payloads larger than shared-bus payloads because collision-detection overhead is minimal, improving bandwidth efficiency.
- Manage ring latency as a scaling cost: each added node increases the time a token takes to circulate.
- Scope networks geographically into LAN (local), MAN (metropolitan), and WAN (wide) based on where data originates and how far it must travel.
- Match fiber optics to one-way ring topologies: laser light travels one direction, very fast, over long distances, supporting deterministic traffic flow.

## Failure modes named
- Collisions on shared media when two signals travel the same pathway simultaneously.
- Exponential performance collapse from retransmissions increasing future collision probability.
- High and growing latency in ring topologies as more nodes join the circle.
- Token monopolization in a ring when implementation fails to enforce fair turn-taking between two heavy talkers.
- Mistaking a star-shaped physical layout for a true star topology when a hub creates a shared multi-access medium at the logical layer.

## Studio relevance
02 frame - Use to map the structural layout and flow rules of a system before diagnosing bottlenecks or designing interventions.
