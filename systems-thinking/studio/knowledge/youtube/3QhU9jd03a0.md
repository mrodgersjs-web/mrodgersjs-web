---
source: https://www.youtube.com/watch?v=3QhU9jd03a0
video_id: 3QhU9jd03a0
channel: CrashCourse
title: "Computer Networks: Crash Course Computer Science #28"
scraped: 2026-08-28
tags: [physics, networking, internet, protocols, distributed-systems]
---
# Computer Networks: Crash Course Computer Science #28

An overview of how computer networks evolved from isolated machines into the global internet through shared media, addressing, collision management, switching, and packet routing.

## Procedure / models distilled
- Use Local Area Networks (LANs) to let nearby computers share data and physical resources such as printers and storage drives instead of physically moving media.
- Assign every network device a unique Media Access Control (MAC) address so it can recognize traffic intended for it on a shared carrier.
- Apply Carrier Sense Multiple Access (CSMA) by having devices listen to the shared medium and transmit only when it appears silent.
- Detect collisions on shared media and use Exponential Backoff: wait a random interval that doubles after each successive collision to reduce repeated contention.
- Shrink collision domains by segmenting networks with switches, which maintain tables of MAC addresses and forward traffic only when destinations lie on different segments.
- Build large internets by interconnecting smaller networks, allowing inter-network communication and multiple paths between endpoints.
- Use Circuit Switching to reserve dedicated communication lines when guaranteed, exclusive capacity is required, accepting higher cost and less flexibility.
- Use Message Switching to relay whole messages hop-by-hop through intermediate nodes, enabling alternate routes and fault tolerance.
- Track hop count and enforce a Hop Limit to detect and prevent infinite routing loops between nodes.
- Use Packet Switching to chop data into small, independently routed packets that can take different paths and avoid tying up entire links.
- Assign IP addresses to networked devices and use Internet Protocol (IP) headers so routers know where to forward packets.
- Balance load dynamically across available paths with congestion control and router-to-router protocols such as ICMP and BGP.
- Run higher-level protocols such as TCP/IP on top of IP to handle out-of-order packet arrival and reliable delivery.

## Failure modes named
- Collisions on shared carriers when two devices transmit simultaneously, garbling the combined signal.
- Repeated collisions when multiple devices use the same fixed retransmission delay after an initial collision.
- Cascading congestion and transmission backlogs when collisions multiply under heavy network load.
- Infinite routing loops where intermediate nodes pass a message back and forth, causing wasted bandwidth and undelivered messages.
- Bottlenecks and link starvation when a whole large message must traverse each hop before the next message can use that link.
- Out-of-order packet arrival when packets from the same message take different routes through a network.

## Studio relevance
02 frame - the studio uses this card to map network architecture, protocols, and failure modes when framing distributed communication systems.
