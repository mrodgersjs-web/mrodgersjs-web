---
source: https://www.youtube.com/watch?v=DuQUw3peq84
video_id: DuQUw3peq84
channel: Behind The Team
title: "BEHIND THE TEAM | Amazon's Two-Pizza Rule Explained"
scraped: 2026-08-28
tags: [organizations, teams, autonomy, dependencies, ownership]
---
# BEHIND THE TEAM | Amazon's Two-Pizza Rule Explained

Amazon's two-pizza rule is not a headcount cap but a structural design for speed: keep teams small enough to be fed by two pizzas, reduce communication links, expose work through interfaces, and assign single-threaded ownership so decisions do not stall in coordination.

## Procedure / models distilled
- Treat communication links as friction: each additional person exponentially increases coordination overhead, so shrinking the team speeds up decisions.
- Apply the two-pizza rule as a dependency audit, not just a people count: a "small" team that needs many approvals is not a two-pizza team.
- Replace approval meetings with documented handoffs or interfaces so the next team acts on a spec instead of waiting for a meeting.
- Implement the API mandate pattern: every team exposes its data and functionality through stable service interfaces and communicates with other teams only through those interfaces.
- Use single-threaded leadership: assign exactly one person who owns one initiative with no split across competing priorities.
- Run the name-one-person test: for every initiative, write down the single person who can say yes to a change without checking with anyone else.
- If two people currently share ownership, name one lead, move the other to support, and record the decision in writing before the next team meeting.
- Sort the blocker before opening a requisition: diagnose whether the blocker is a dependency problem, an ownership problem, or a genuine headcount problem.
- Pull the last three blockers that stalled the team and classify them into dependency (waiting on another team), ownership (no clear decider), or capacity (work exceeds available hands).
- Fix dependency and ownership first; open a new hire requisition only if the same blocker persists after both are cleared.
- Design the team before growing it: structure, interfaces, and ownership determine velocity more than raw headcount.

## Failure modes named
- Hiring more developers as the default response to delivery problems, assuming more people equals faster delivery.
- Treating the two-pizza rule as a headcount rule while ignoring cross-team approvals and hidden dependencies.
- Allowing split leadership or shared ownership, which forces alignment loops and slows decisions.
- Permitting informal or ad hoc inter-team communication instead of stable, documented interfaces.
- Opening requisitions to solve dependency or ownership problems that hiring cannot fix.

## Studio relevance
04 leverage - how the studio uses this card
