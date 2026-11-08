---
source: https://www.youtube.com/watch?v=986hztrfaSQ
video_id: 986hztrfaSQ
channel: unknown
title: "Build and Deploy a Full Stack Next.js Application | React, Next JS, TypeScript, Tailwind CSS"
scraped: 2026-08-28
tags: [engineering, nextjs, fullstack, graphql, deployment]
---
# Build and Deploy a Full Stack Next.js Application | React, Next JS, TypeScript, Tailwind CSS

A step-by-step build and deploy of a Dribbble-style developer portfolio app using Next.js 13 App Router, TypeScript, Tailwind CSS, GraphBase, NextAuth, and Cloudinary.

## Procedure / models distilled
- Initialize a Next.js 13 project with TypeScript, Tailwind CSS, ESLint disabled, no `src` directory, and the App Router enabled using `npx create-next-app@latest`.
- Install the dependency stack: `@headlessui/react` for accessible UI primitives, `cloudinary` for image hosting, `jsonwebtoken` and `@types/jsonwebtoken` for auth tokens, `graphql-request` for GraphQL calls, `next-auth` for authentication, and `@grafbase/sdk` as a dev dependency.
- Scaffold the project structure: `app/` for pages and API routes, `components/` for reusable UI, `public/` for static assets, `common.types.ts` for shared TypeScript interfaces, and updated `globals.css` and `tailwind.config.js`.
- Define GraphBase schemas for `Project` and `User` with relations, then run CRUD operations against the serverless GraphQL API.
- Configure NextAuth with Google Provider and a custom JWT/credentials flow, storing the session token and passing it to GraphBase for authorized requests.
- Compose the homepage as a server-rendered section containing categories, posts, and load-more pagination handled server-side.
- Create API routes for token generation and GraphQL proxy actions so client components can authenticate without exposing secrets.
- Implement a Cloudinary image upload flow that takes a device image, uploads it to the cloud, and stores the returned URL with the project record.
- Build create/edit/delete project pages and a profile page using dynamic routes, reusing components across list, detail, and profile views.
- Deploy the app to Vercel, import the GitHub repository, populate environment variables, and update Google Cloud OAuth callback URIs to match the production domain.
- Debug production issues by inspecting Vercel deployment logs, verifying environment variables across Vercel and GraphBase, and redeploying after any env change.

## Failure modes named
- Deploying without redeploying after environment variable changes leaves the running build stale.
- Missing `NEXT_PUBLIC_SERVER_URL` causes client-side API requests to hit `undefined` and fail in production.
- GraphBase returning 403 API auth errors when `NEXTAUTH_SECRET` or related auth env vars are not synced to GraphBase.
- Newly created posts not appearing immediately after creation due to Next.js 13 server-side rendering caching behavior.
- TypeScript build errors blocking deployment unless resolved or safely bypassed before push.

## Studio relevance
07 verify - how the studio uses this card
