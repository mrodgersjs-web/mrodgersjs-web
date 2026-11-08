---
source: https://www.youtube.com/watch?v=DJMsXSr1jec
video_id: DJMsXSr1jec
channel: Shreyas Raj
title: "Build $10,000 AI 3D Websites in 10 Minutes (Google Anti-Gravity Full Tutorial)"
scraped: 2026-08-28
tags: [engineering, ai, 3d-web, web-development]
---
# Build $10,000 AI 3D Websites in 10 Minutes (Google Anti-Gravity Full Tutorial)

A walkthrough of using Google's Whisk, Flow, and Anti-Gravity IDE to generate product visuals, animate an exploded-view video, convert it to scroll-synced frames, and deploy a premium 3D website locally.

## Procedure / models distilled
- Start with a high-quality product image; the demo uses a Sony WH-1000XM6 headphone as the subject.
- Use Google Whisk's image-generation workspace to generate a premium horizontal hero product shot with a universal prompt.
- Generate a separate exploded-view product shot in Whisk by swapping the universal prompt for an explosion prompt.
- Select start and end frames carefully because the final animation quality depends on them matching your intent.
- Use Google Flow's "frames to video" feature to animate a smooth transition from the assembled product to the exploded view.
- Write the video prompt explicitly as a "slow-motion professional internal tech showcase" rather than relying on the word "explosion," which AI interprets poorly.
- Convert the generated video into JPG frames at 30 FPS using EaseGIFs' video-to-image converter.
- Download the extracted frames as a zip and unzip them into a dedicated project folder.
- Install the Google Anti-Gravity IDE and Node.js as the runtime stack.
- Create a new project folder inside Anti-Gravity and paste the unzipped frames folder into it.
- Paste the provided build prompt into Anti-Gravity's chat panel and select Gemini 3 Pro High for the best output.
- Run the terminal commands (cd project, npm install, npm run dev) to spin up a local development server.
- Open the localhost URL to view and scroll through the finished 3D exploded-view website.

## Failure modes named
- AI image generators tend to misinterpret the word "explosion," producing overly massive or distorted disintegrations instead of a clean exploded-view technical render.
- Using a vertical or poorly oriented hero shot breaks the horizontal layout expected for a hero section.
- Starting and ending frames that do not match the desired product state degrade the final scroll animation.
- Generating only one video variation reduces the chance of landing a clean, premium output.
- Treating the provided prompt as one-shot and skipping manual tweaking can leave the website unfinished or off-brand.

## Studio relevance
06 synthesize - reference as a multi-tool workflow for producing scroll-driven 3D product experiences from image generation through local deployment.
