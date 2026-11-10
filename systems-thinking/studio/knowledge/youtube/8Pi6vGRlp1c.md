---
source: https://www.youtube.com/watch?v=8Pi6vGRlp1c
video_id: 8Pi6vGRlp1c
channel: ArjanCodes
title: "The Right Way to Use AI for Writing Maintainable Code"
scraped: 2026-08-28
tags: [engineering, ai-coding-assistants, software-design, maintainability, refactoring]
---
# The Right Way to Use AI for Writing Maintainable Code

The video demonstrates how to iteratively guide an AI coding assistant toward maintainable code by applying software design principles rather than accepting the first working draft.

## Procedure / models distilled
- Treat software design as the primary tool for managing complexity so AI prompts become simpler and generated code remains maintainable.
- Start from an AI-generated example, then immediately critique structure and responsibilities, not just whether it runs.
- Replace sprawling conditional logic in runner methods with a protocol or command object for each action.
- Eliminate circular dependencies by making step classes depend on lower-level concepts like shape and color instead of the orchestrator.
- Align code structure with domain concepts, for example making an animation play on a shape rather than having the animation create its own animator.
- Push duration into each animation step so the animator only tracks time and dispatches to steps.
- Consolidate near-duplicate low-level operations into a single responsibility, such as one render method instead of separate draw and update methods.
- Separate high-level shape abstractions from low-level rendering with dependency injection to keep each layer simple.
- Demote a class to a plain function when it ends up holding only a single responsibility.
- Store animation duration at the animation level, not inside every step, so steps stay reusable and composable.
- Ask the AI design questions instead of handing it solutions, then iterate on the result using design principles.
- Verify generated behavior empirically and fix algorithmic bugs such as cumulative transformations applied each frame.
- Manage ground-truth state by storing original shape state as a baseline for animation math, then applying the final transformed state.
- Split the code into focused files by responsibility, such as graphics, animation, and main orchestration.

## Failure modes named
- Accepting the first working draft and building on top of it, which accumulates long-term technical debt.
- Letting the AI place unrelated responsibilities in one class, such as canvas setup, shape drawing, fading, and timekeeping in the animator.
- Circular dependencies between orchestrators and the steps they run.
- Large if-statement run methods that grow with every new action.
- Monkey-patching helper methods onto a class instead of giving them a proper home.
- Duplicated low-level logic split across draw and update paths.
- Outdated style choices such as uppercase `List`, `Dict`, and `Tuple` imports.
- AI agreeing with the user even when the proposed direction is wrong, leading to overcomplicated or misguided fixes.
- Getting sidetracked into complex pipeline changes when a simple value or hardcoded-parameter adjustment is sufficient.
- Cumulative application of transformations that ignores the correct baseline state.
- Treating AI as a feature generator rather than a collaborator that needs design direction.

## Studio relevance
04 leverage - how the studio uses this card
