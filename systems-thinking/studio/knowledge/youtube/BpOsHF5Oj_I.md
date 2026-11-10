---
source: https://www.youtube.com/watch?v=BpOsHF5Oj_I
video_id: BpOsHF5Oj_I
channel: Riley Brown
title: "The Ultimate Beginner’s Guide to AI Coding"
scraped: 2026-08-28
tags: [engineering, vibe-coding, ai-agents, no-code]
---
# The Ultimate Beginner’s Guide to AI Coding

A beginner’s walkthrough of using OpenAI Codex and GPT-5.5 to build, iterate, save, and cross-compile a web app into desktop (Electron) and iOS (Swift) apps sharing one backend.

## Procedure / models distilled
- Install the Codex desktop app from openai.com/codex and create a new project inside a local folder.
- Treat an app as a folder of code files that become software once the AI agent generates and runs them.
- Write a plain-language prompt describing the app you want; the agent uses GPT-5.5 to create, edit, and delete files in the project folder.
- Preview the app locally with Codex’s built-in runner / preview panel, then toggle the preview on and off as needed.
- Iterate through the “prompt → agent edits files → run locally → test → prompt again” loop until the app behaves as desired.
- Create a private GitHub repository and paste its link into Codex to upload or “push” the code; this acts like cloud storage for the project.
- Say “commit the changes to GitHub” after edits so the saved version on GitHub stays in sync with the local folder.
- Use Firebase as the default backend for authentication, database, and storage; Superbase or Neon are named alternatives.
- Convert a working web app into a desktop app by asking Codex to use Electron, a wrapper that packages a web app as a native desktop app.
- Convert the same web app into an iOS app by asking Codex to use Swift and the Xcode project structure.
- Before large conversions, ask Codex to produce a markdown plan that maps out how web, desktop, and iOS apps will share one backend and storage layer.
- Keep web, desktop, and iOS apps inside one parent project folder with subfolders for each platform so the agent retains full context.
- Debug runtime errors by pasting error text or screenshots into Codex and asking it to fix the issue.
- Test iOS builds using Apple’s Xcode and iPhone Simulator, which run the app on your Mac without needing a physical device.

## Failure modes named
- Believing GitHub is too intimidating for non-coders to set up manually.
- Building the desktop app without verifying basic window controls, resulting in a non-movable window.
- Pop-up blockers interrupting Google sign-in flows inside the Electron app.
- iOS keychain errors blocking sign-in inside the simulator.
- Mobile UI elements with placeholder text too long for the screen, causing truncation.
- Overloading mobile detail views with too many components, making the interface clunky.
- Unclear identity/ownership when an agent adds data on behalf of the user.

## Studio relevance
04 leverage - how the studio uses this card
