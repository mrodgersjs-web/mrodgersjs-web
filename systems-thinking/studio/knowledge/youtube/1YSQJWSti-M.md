---
source: https://www.youtube.com/watch?v=1YSQJWSti-M
video_id: 1YSQJWSti-M
channel: LeadDev
title: "Scaling engineering teams with an architecture North Star | Hanjie Ji | #LeadDevAustin"
scraped: 2026-08-28
tags: [product-growth, engineering-management, architecture, agile, scaling-teams]
---
# Scaling engineering teams with an architecture North Star | Hanjie Ji | #LeadDevAustin

How to keep autonomous agile teams aligned on architecture direction as they scale by creating a lightweight, shared, forward-looking architecture North Star grounded in domain-driven design.

## Procedure / models distilled
- Define an architecture North Star as a coherent, forward-looking architecture built on shared understanding of requirements and constraints so teams can orient and navigate without giving up autonomy.
- Introduce a North Star once agile teams have run long enough to validate hypotheses and assumptions, not on day one before requirements and constraints are known.
- Use domain-driven design as the framework to map complexity, outputting a context map, domain owners, principles, and anti-patterns rather than exhaustive system diagrams.
- Build a context map showing key domains and their boundaries so engineers and product can see where strategic decisions must be made and where teams can remain autonomous.
- Involve stakeholders, customers, and product managers in the North Star exercise; engineers know technical limitations but do not own future business requirements.
- Prioritize architecture-significant requirements—the ones that would fundamentally disrupt architecture if ignored—and validate that they are real before designing around them.
- Scope the North Star practically to roughly six months out and at most one year out, focusing on core domains that differentiate the business and have heavy cross-cutting concerns.
- Identify core domains by asking: is this build vs. buy? is it fundamental to competitive advantage? does it have many cross-cutting dependencies?
- Define domain boundaries carefully so teams have freedom inside a boundary and explicit, lightweight interaction rules across boundaries.
- Keep the North Star lightweight and iterate; it should provide just enough architecture for fast, decisive daily decisions and be easy to update when business fundamentals change.
- Make the North Star highly visible to engineering, product, and business so everyone speaks the same language and uses it as a base for future requirement discussions.
- Let autonomous agile teams continue iterative delivery in small chunks while feeding learnings back into the North Star, preserving self-organization while reducing coordination overhead.

## Failure modes named
- Piecemeal architecture emerging when many autonomous teams optimize locally and the overall architecture becomes incoherent.
- "Bumper cars" effect where agile teams rely on reaction and experience to navigate because no holistic architectural view exists.
- Divergent architectural directions as teams with different contexts and business goals make siloed, just-in-time design decisions.
- Repurposing a service built for X to do Y, making it hard to extend capabilities and creating hidden coupling.
- Similar but different services doing overlapping things, leading to duplication and confusion.
- Wrong abstractions and poor integration caused by siloed knowledge and teams seeing only their piece of the puzzle.
- Haphazardly structured, duct-taped code created with good intentions but without guidance on where the architecture is heading.
- Overcorrecting by reducing team autonomy through scrum-of-scrums, architecture committees, embedded architects, or returning to waterfall big design up front.
- Building a North Star too early when requirements and assumptions are still unvalidated.
- Designing the North Star for a far-reaching future or making it too big, which makes it hard to update and harder for teams to use.

## Studio relevance
04 leverage - apply the architecture North Star exercise to re-align autonomous agile teams around a shared architecture direction while preserving their autonomy and avoiding coordination-heavy anti-patterns.
