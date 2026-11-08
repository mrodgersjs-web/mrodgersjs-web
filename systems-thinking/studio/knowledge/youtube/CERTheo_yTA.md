---
source: https://www.youtube.com/watch?v=CERTheo_yTA
video_id: CERTheo_yTA
channel: Five Minute Friday
title: "Conway's Law and the Reverse Conway Manoeuvre - Five Minute Friday"
scraped: 2026-08-28
tags: [organizations, software-architecture, systems-design, organizational-change]
---
# Conway's Law and the Reverse Conway Manoeuvre - Five Minute Friday

Conway's Law means organizations inevitably build systems that mirror their communication structures, so the Reverse Conway Manoeuvre redesigns the organization first to create a desired future system architecture.

## Procedure / models distilled
- State Conway's Law: any organization that designs a system will inevitably produce a design whose structure copies the organization's communication structure.
- Recognize that software architecture mirrors organizational structure and communication patterns.
- Map team boundaries to module boundaries: the seams between teams become the seams between systems or components.
- Use the Army/Navy joint-system example to see how separate organizational units plus a coordination layer produce matching system modules and a command module.
- Apply the Reverse Conway Manoeuvre when the goal is a new system architecture: change the organization to make the new architecture inevitable.
- Step 1: define the desired future-state system architecture.
- Step 2: determine the future-state organizational structure and communication patterns that would naturally produce that architecture.
- Step 3: begin shifting the current organization toward the future-state structure.
- To extract a capability from a monolith, carve out a dedicated team with a clear mission around that capability.
- Let the new team and the existing teams communicate in the same way the desired systems should integrate; the system boundaries will follow.
- Repeat the team-carving process to decompose an overloaded monolith into smaller, coherent chunks such as microservices.
- Treat organizational design as an integral part of system design, because Conway's Law means org design always drives system architecture.
- Note that the Reverse Conway Manoeuvre applies beyond software to any system an organization designs.

## Failure modes named
- A monolith accumulating too many unrelated responsibilities until it becomes unmanageable.
- Letting existing organizational silos unconsciously dictate system boundaries instead of deliberately designing both together.
- Trying to change system architecture without changing the organizational communication structure that produces it.
- Treating organizational design and system design as separate concerns.

## Studio relevance
04 leverage - use org design as an active lever to reshape system architecture before restructuring teams or code.
