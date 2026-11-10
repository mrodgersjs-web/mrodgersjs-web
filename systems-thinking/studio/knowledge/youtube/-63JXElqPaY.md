---
source: https://www.youtube.com/watch?v=-63JXElqPaY
video_id: -63JXElqPaY
channel: MIT OpenCourseWare
title: "9. Verification and Validation"
scraped: 2026-08-28
tags: [engineering, systems-engineering, verification-and-validation, risk-management, system-safety]
---
# 9. Verification and Validation

This lecture distinguishes verification (did we build the system right against written requirements?) from validation (did we build the right system for stakeholder intent?), then connects testing, technical risk management, systems-theoretic safety, and the Flight Readiness Review as the final launch gate.

## Procedure / models distilled
- Use the V-model’s two closing loops: the inner verification loop checks the implemented design against requirements as written, while the outer validation loop checks the deployed system with stakeholders in a realistic environment.
- Derive every requirement from stakeholder analysis and assign target or threshold values, then verify attainment of each requirement under controlled, repeatable conditions.
- Validate the full-up system or a realistic surrogate in an actual or simulated mission environment to confirm the CONOPS and original stakeholder intent are satisfied.
- Classify any test activity by its setting: controlled lab/standardized/test-stand conditions are verification; real-world operational use with actual users is validation.
- Plan a test campaign that covers operational extremes and realistic environments rather than only ideal lab conditions, recognizing testing is costly and imperfect.
- Maintain a technical risk matrix with likelihood and severity axes, set watch/yellow and stop/red thresholds, track items above the watch line, and escalate or redesign when risks cross the red line.
- Run a recurring risk-management cycle: identify risks, place them on the matrix, quantify with available data, report, mitigate, and re-evaluate; accept only well-understood residual risk before launch.
- Apply the cost–schedule–scope–risk trade space to decide when to redesign, delay, or cancel a program rather than pursue zero risk.
- Separate component-failure accidents from component-interaction accidents, and avoid relying solely on linear chain-of-events or Swiss-cheese barrier models for complex, software- and human-rich systems.
- Model safety as a control problem using STAMP/STPA: examine sensors, controller/process model, actuators, process inputs, disturbances, and whether control constraints are violated.
- Treat safety as an emergent property that degrades over time as components drift, sensors fail, and operators bypass procedures; monitor constraints continuously.
- Hold a Flight Readiness Review (FRR) or launch-to-market review as the last formal gate before countdown to confirm all V&V is passed, waivers are granted, residual risks are accepted, and the team has a final chance to raise red flags.

## Failure modes named
- Treating verification and validation as interchangeable synonyms.
- Attempting validation at the subsystem level instead of with the full-up system or realistic surrogates.
- Designing the product to pass stylized verification tests while failing in real operation (e.g., emissions software recognizing test cycles).
- Demanding zero residual risk, which blocks any launch or market entry.
- Using only linear chain-of-events / Swiss-cheese barrier analysis and missing component-interaction accidents.
- Assuming safety established at design time will persist as the system migrates to an unsafe state through degraded components and bypassed procedures.
- Treating the FRR as a formality instead of the last real opportunity to stop the launch.

## Studio relevance
07 verify - how the studio uses this card
