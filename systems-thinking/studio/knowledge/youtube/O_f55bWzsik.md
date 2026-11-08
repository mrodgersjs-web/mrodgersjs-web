---
source: https://www.youtube.com/watch?v=O_f55bWzsik
video_id: O_f55bWzsik
channel: TubeGuruji
title: "Build Full stack AI Influencer Generator & Post Scheduler Using NextJs, React, Luma AI, Zernio"
scraped: 2026-08-28
tags: [tools, nextjs, saas, ai-influencer, social-media-scheduling]
---
# Build Full stack AI Influencer Generator & Post Scheduler Using NextJs, React, Luma AI, Zernio

A hands-on tutorial for building a Next.js SaaS where users create AI influencer profiles, generate portrait and full-body visuals with Luma AI UniOne, craft campaign posts, and schedule or publish them across social platforms via the Zeno API, backed by Supabase auth/data and Stripe subscriptions.

## Procedure / models distilled
- Scaffold a Next.js/React project and set up Supabase for authentication (email/password plus social providers) and as the application database.
- Build a landing page and an authenticated dashboard with sidebar navigation covering dashboard, model/studio, create post, calendar, account, and settings.
- Create an AI influencer model workflow that collects name, gender, body type, skin tone, age range, hairstyle, vibe, and an optional custom prompt, then generates both a portrait and a full-body image via Luma AI UniOne.
- Save generated models to a studio gallery and deduct credits each time a model is created.
- Build a post-creation flow: select an existing model, choose connected social accounts, pick a post format (square/landscape), and fill campaign details such as product, goal, scene location, outfit, lighting, prop, brand style, and primary CTA.
- Generate post variants with Luma UniOne using up to three reference images and extra instructions, then preview the resulting images and pick a version.
- Schedule posts for a specific date/time or publish immediately, storing scheduled posts in a calendar view and recent activity feed.
- Connect social accounts (Instagram, TikTok, Facebook, YouTube, X/Twitter, etc.) through the Zeno API so only connected platforms appear during post creation.
- Publish or schedule across selected platforms through a single Zeno API endpoint that includes the media file, caption/description, and target platform(s).
- Implement a credit system with free, standard, and pro tiers: define costs for model creation and post generation, enforce account-connection limits, and cap scheduled posts per tier.
- Integrate Stripe for subscriptions: define plan prices in code rather than pre-creating products/plans in Stripe, create a checkout session, and add credits to the user account after a successful payment/webhook event.
- Add Stripe keys (secret, publishable, webhook secret) to environment variables and run the required Supabase SQL migrations to support profiles, credits, and subscription state.

## Failure modes named
- Social platforms enforce different media upload limits (e.g., Twitter max 4 images, Instagram max 10), so the upload logic must respect the target platform.
- Stripe webhooks require a publicly reachable endpoint; localhost will not receive webhooks unless you route through ngrok or another tunnel.
- Missing Stripe secret, publishable, or webhook keys in environment variables will block checkout and post-payment credit top-ups.
- Pre-creating subscription plans inside Stripe makes later pricing changes harder; it is safer to pass the subscription amount from the application’s pricing model.
- If credit-deduction logic is not implemented on model and post creation flows, users can generate content without spending credits.
- A scheduled post that appears in-app should also be confirmed in the Zeno dashboard, since the UI alone does not prove the platform accepted the schedule.
- Treating the project as a simple demo instead of wiring auth, credits, scheduling, and payments will prevent it from becoming a usable SaaS.

## Studio relevance
04 leverage - the studio uses this card as a reference architecture and anti-pattern checklist when assembling AI model generation, social scheduling, and payment services into a coherent SaaS product.
