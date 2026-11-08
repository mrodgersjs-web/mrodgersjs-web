---
source: https://www.youtube.com/watch?v=AW1yfBKRMKc
video_id: AW1yfBKRMKc
channel: JavaScript Mastery
title: "Master Web Animations in 2 Hours | Build an Awwwards-Level Website"
scraped: 2026-08-28
tags: [engineering, gsap, web-animation, react, front-end]
---
# Master Web Animations in 2 Hours | Build an Awwwards-Level Website

A hands-on crash course that teaches core GSAP animation primitives in React, then applies them to build a scroll-driven, emotionally purposeful cocktail landing page.

## Procedure / models distilled
- Use the `useGSAP(callback, deps)` hook as a React-style effect to run GSAP animations on mount and re-run them when dependencies change.
- Animate from an element’s current state to a new state with `gsap.to(target, { x, rotation, duration, ease, repeat, yoyo })`.
- Create entrance animations with `gsap.from(target, { ... })`, which animates from a defined starting state back to the element’s current rendered state.
- Define explicit start and end states with `gsap.fromTo(target, fromVars, toVars)` for fully predictable bidirectional motion.
- Sequence and orchestrate multiple tweens with `gsap.timeline()`, chaining `.to()`, `.from()`, or `.fromTo()` and using relative offsets like `<` to overlap motion.
- Bind tweens to scroll progress with `ScrollTrigger` by configuring `trigger`, `start`, `end`, `scrub`, and `pin` to build scroll-driven reveals and parallax.
- Create cascading entrance effects by adding a `stagger` value to a tween or timeline so related elements animate in rhythm instead of simultaneously.
- Split text into animatable words with `SplitText.create(selector, { type: 'words' })`, then target the generated words for staggered reveals.
- Tie animations to React state by including state variables such as `currentIndex` in `useGSAP`’s dependency array so the animation re-runs when the state changes.
- Build scroll-linked parallax by translating foreground and background layers at different rates as the user scrolls.
- Pair `gsap.timeline()` with `ScrollTrigger` so a footer or contact section animates in as it enters the viewport.
- Design animations with emotional intent: each motion should advance a narrative or feeling, such as a drink sliding toward the user, rather than existing only to look cool.

## Failure modes named
- Animating purely for visual effect instead of serving an emotional or narrative purpose.
- Passing `type: 'word'` to `SplitText.create` instead of `type: 'words'`, which silently produces no animatable targets.
- Misspelling an image filename or element ID so the element never renders and the GSAP selector returns nothing.
- Omitting a dependency from `useGSAP` and expecting the animation to re-run when React state like a slide index changes.

## Studio relevance
04 leverage - use this card to build cinematic, scroll-driven, emotion-led interfaces with GSAP in React.
