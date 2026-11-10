---
source: https://www.youtube.com/watch?v=2C2F5USR6N4
video_id: 2C2F5USR6N4
channel: USENIX
title: "SREcon20 Americas - The Secret Lives of SREs - Controlling the Costs of Coordination across Remote"
scraped: 2026-08-28
tags: [organizations, remote work, incident response, coordination, cognitive load, site reliability engineering]
---
# SREcon20 Americas - The Secret Lives of SREs - Controlling the Costs of Coordination across Remote

SRE incident response is socio-technical work where hidden cognitive and coordinative labor must be deliberately distributed to avoid bottlenecks, especially in remote environments.

## Procedure / models distilled
- Adopt a socio-technical systems lens: treat SRE work as real-world cognitive activity that formal runbooks and tools only partially represent.
- Recognize the coordination paradox: complex failures require diverse perspectives, but bringing those perspectives together imposes its own cognitive load.
- Build and maintain common ground: shared system knowledge, recent deploys, expected loads, and known "exploding bits" reduce the effort needed to coordinate.
- Account for the remote coordination tax: distributed response costs substantially more cognition than co-located control rooms because implicit cues about event state and responder capacity are missing.
- Reject linear incident response: incidents are overlapping and concurrent; responders often must safeguard systems before they fully understand the problem.
- Use encoded utterances for implicit coordination: short statements like "checking logs" or "killing jobs" signal orientation and intended action so others can align without lengthy explanation.
- Distribute coordination like distributed computing: spread coordinative functions across responders so the team functions as one adaptive system rather than routing everything through a single node.
- Share coordinative responsibilities: information gathering, synthesis, communication, expertise recruitment, sequencing, and synchronizing should be collective work, not owned solely by the incident commander.
- Maintain continuous common ground: keep a low-level awareness of event progression so responders can challenge mismatched mental models and repair shared understanding in real time.
- Practice adaptive choreography over command-and-control: high-performing teams anticipate next steps, take initiative, and time actions without waiting for central delegation.
- Position the incident commander as a coordinator, not a bottleneck: the IC role supports distributed coordination rather than monopolizing it.
- Treat incidents as empirical learning material: study real response work to surface hidden practices and improve tooling, training, and organizational design.

## Failure modes named
- Oversimplifying SRE work as purely technical or sequential.
- Treating incident response as a clean linear flow (detect → diagnose → repair → move on).
- Centralizing all coordination in a single incident commander, creating a processing bottleneck.
- Slowing the response to the speed of the IC, adding unnecessary outage duration.
- Assuming remote and co-located coordination carry the same cognitive cost.
- Relying on formal documentation that fails to capture the full cognitive work of response.
- Allowing outsiders or newcomers to misinterpret expert-encoded communication.
- Letting common ground erode so responders act on partial or erroneous models.
- Treating incident command structure as a rigid hierarchy instead of a distributed adaptive function.

## Studio relevance
03 diagnose - how the studio uses this card to reveal hidden coordination costs, bottlenecks, and cognitive load in incident response and to redesign practices around distributed coordination and common ground.
