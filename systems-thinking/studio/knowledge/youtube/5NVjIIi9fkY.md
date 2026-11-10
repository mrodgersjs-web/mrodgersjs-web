---
source: https://www.youtube.com/watch?v=5NVjIIi9fkY
video_id: 5NVjIIi9fkY
channel: MATLAB
title: "Feedback Control Systems | Understanding Control Systems, Part 2"
scraped: 2026-08-28
tags: [engineering, feedback control, control systems, dynamic systems]
---
# Feedback Control Systems | Understanding Control Systems, Part 2

The video explains feedback control by showing how continuous measurement of an output, comparison to a desired value, and action driven by the resulting error let a system reach and maintain its goal despite variations and disturbances.

## Procedure / models distilled
- Define a desired output, or setpoint, such as a target toast color or water temperature.
- Measure the actual output continuously with a sensor, which can be human sight, skin, or a thermocouple.
- Compute the error as the difference between the desired output and the measured output.
- Use a nonzero error to decide whether to keep the actuator running; if the error is not zero, continue applying control action.
- Turn off or reduce the actuator once the measured output matches the setpoint and the error reaches zero.
- View the overall process as a closed loop: setpoint, comparator, controller, actuator, process, and sensor feeding back to the comparator.
- Treat the comparator as the mental step that subtracts “what you see” from “what you want” to produce the error signal.
- Handle system variations without a precise prior model by relying on measured output rather than a fixed input schedule.
- Reject unexpected disturbances by sensing the resulting change in output and adjusting the actuator to drive the error back to zero.
- Automate the human role with physical components: a sensor measures the process variable and a controller manipulates the actuator based on the error.
- Make smaller adjustments as the error shrinks, so control effort tapers as the system approaches the setpoint.

## Failure modes named
- Open-loop timer-based toasting fails when the user has no prior knowledge of the correct toasting duration.
- A fixed shower-handle position calibrated by trial and error fails when an unmeasured disturbance such as a dishwasher diverts hot water.
- Using the same preset input for different loads produces different outputs, as with a slice of bread versus a frozen bagel.
- Calibrating an input once and then ignoring feedback leaves the system unable to compensate for new or unexpected variations.

## Studio relevance
02 frame - map any goal-seeking system onto the feedback-loop template of setpoint, sensor, error, controller, actuator, and disturbance.
