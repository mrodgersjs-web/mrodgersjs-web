---
source: https://www.youtube.com/watch?v=4-A_PIEJ3JE
video_id: 4-A_PIEJ3JE
channel: Woven by Toyota
title: "Kenshiki Deep Dive by James Kuffner (English Subtitles)"
scraped: 2026-08-28
tags: [history-cases, automated-driving, toyota-production-system, digital-twins, woven-city]
---
# Kenshiki Deep Dive by James Kuffner (English Subtitles)

James Kuffner explains how Woven by Toyota combines human-centered purpose, a perception-prediction-planning autonomy stack, TPS-inspired software tooling, and digital-twin simulation to develop safe automated mobility and build the Woven City living laboratory.

## Procedure / models distilled
- Anchor every technology effort in amplifying human potential, not technology for its own sake
- Run a continuous three-P autonomy loop: perception → prediction → planning
- Fuse radar, camera, and lidar streams into a 360° real-time model of the traffic environment
- Overlay live sensor data on high-resolution semantic maps for automated driving context
- Feed every test drive's sensor data back into machine-learning training to improve the system over time
- Treat training-data quality and diversity as equally important as quantity
- Validate software changes through cloud-based simulation of thousands of traffic scenarios in parallel, including corner cases
- Apply Toyota Production System (TPS) principles to software development to achieve safe, high-quality, scalable code
- Recognize that roughly 90% of automotive software is off-board tooling for data, ML, builds, tests, OTA updates, and maps
- Build high-quality onboard software by first building excellent off-board tooling
- Segment mobility by speed into vehicular, intermediate (bikes/personal mobility), and pedestrian-only woven pathways
- Use Woven City as a real-world, renewable-energy-powered living lab and test course
- Create a digital twin of the physical city to iterate mobility services and answer capacity/latency questions before deployment
- Practice "digital TPS" by using simulation to explore many design possibilities in parallel at scale

## Failure modes named
- Technology-first thinking: becoming so excited about technology that the purpose of helping people is forgotten
- Attempting to physically test every traffic scenario with real cars, which is impractical or impossible
- Believing that sheer quantity of training data alone produces good machine-learning performance
- Underinvesting in off-board software and tooling while focusing only on onboard vehicle software

## Studio relevance
04 leverage - using the three-P autonomy loop, TPS-for-software, and digital-twin simulation as leverage points when designing human-centered mobility systems.
