---
source: https://www.youtube.com/watch?v=qjWkNZ0SXfo
video_id: qjWkNZ0SXfo
channel: Tsoding
title: "One Formula That Demystifies 3D Graphics"
scraped: 2026-08-28
tags: [engineering, 3d-graphics, rendering, mathematics, javascript]
---
# One Formula That Demystifies 3D Graphics

3D perspective projection reduces to the pinhole formula `(x', y') = (x / z, y / z)`, which the video re-creates in a minimal HTML5-Canvas JavaScript renderer from scratch.

## Procedure / models distilled
- **Pinhole projection formula**: a 3D point `P = (x, y, z)` is projected to the 2D display point `(x / z, y / z)`, derived from similar triangles between the eye, the screen plane at `z = 1`, and the point.
- **Display vs. screen coordinate model**: the formula assumes a centered display space where `(0, 0)` is the middle, `x ∈ [-1, 1]`, `y ∈ [-1, 1]`, and positive y points up.
- **Canvas coordinate mapping**: map centered display coordinates to HTML Canvas coordinates with `x_screen = (x + 1) / 2 * width` and `y_screen = (1 - (y + 1) / 2) * height` to flip the y-axis and shift the origin to top-left.
- **Vertex + face data model**: represent 3D objects as an array of vertices and an array of faces, where each face is a list of vertex indices that form a closed polygon.
- **Frame loop with delta time**: drive animation with `setTimeout` at a target FPS and multiply changes by `dt = 1 / FPS` to keep motion time-based.
- **3D translation along z**: move an object away from the eye by adding a time-varying offset to every vertex's `z` component before projection.
- **2D rotation in the xz plane**: rotate vertices around the y-axis using `x' = x*cos(θ) - z*sin(θ)` and `z' = x*sin(θ) + z*cos(θ)` before projection.
- **Polygon edge rendering**: for each face, iterate its indices and connect each vertex to the next, wrapping the last index back to the first using modular arithmetic.
- **2D line drawing primitive**: use Canvas `beginPath`, `moveTo`, `lineTo`, and `stroke` to draw the projected edges between paired vertices.
- **Wireframe composition**: omit the vertex dots and render only the face edges to produce a recognizable rotating cube wireframe.
- **Arbitrary mesh rendering**: the same projection loop generalizes to more complex models by supplying larger vertex and face arrays without needing WebGL/OpenGL.

## Failure modes named
- **Division by zero at z = 0**: a point located exactly at the eye has nowhere to project, so the scene must keep objects at a positive distance from the camera.
- **Canvas coordinate mismatch**: HTML Canvas puts the origin at the top-left with positive y downward, so naive use of the formula places objects in the wrong location or orientation.
- **Black-on-black rendering**: default Canvas stroke color is black, so lines against a black background are invisible until stroke style is set explicitly.
- **Face index buffer overrun**: when connecting polygon vertices in a loop, the last vertex must wrap back to index 0 to close the shape.
- **Incorrect vertex ordering**: connecting cube vertices in the wrong order produces distorted or non-cube shapes until the index list matches the spatial layout.

## Studio relevance
05 ground - reconnects complex 3D graphics APIs to the simple pinhole-camera math and a minimal CPU renderer underneath them.
