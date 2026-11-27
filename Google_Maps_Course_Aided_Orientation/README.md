# Course-Aided Map Orientation

**Concept by Pol Barreiro Font.** This small Python demonstration was prepared with AI assistance to make the concept concrete; it is not production navigation software.

## The idea

A map app's blue location dot can show the user's position while its blue cone indicates the direction the phone is facing. On some devices, that direction can be unstable while the user is moving. This proposal adds a second directional cue: the recent direction of travel derived from successive GPS fixes.

Under the explicit assumption that the user holds the phone upright and points its top edge forward, recent GPS course can help estimate the phone's forward direction. A production implementation could combine this course with the phone's fused orientation sensors (gyroscope, accelerometer and magnetometer), GPS course and their confidence/accuracy values. The map's orientation indicator could then stabilize sooner, especially when magnetic heading is noisy.

This is an **orientation aid**, not a GPS-position accuracy improvement. GPS course becomes unreliable when stationary, moving slowly, turning sharply, or when fixes are noisy. The estimator should fade or reject the course cue in those cases and fall back to the device's normal orientation estimate. If the phone is sideways, in a pocket, or pointed away from the direction of travel, the assumption does not hold.

## Python concept demo

`heading_demo.py` is a dependency-free illustration. It calculates a bearing and speed from a short sequence of GPS fixes, then blends that course with an optional device heading using circular angle math. It is not connected to Google Maps, Android sensors, or a live GPS receiver. A real implementation needs platform-specific sensor fusion, uncertainty calibration, user testing, and safeguards for walking, cycling, driving, and device posture.

Run it with Python 3:

```sh
python heading_demo.py
```

## What to evaluate

- Compare the map's displayed forward direction with and without course assistance.
- Measure heading error and time to a stable heading across phone models and movement speeds.
- Test stops, turns, low-quality GPS, indoor/urban canyon conditions, and phones not held forward.
- Use confidence-weighted fusion and fall back whenever course is unreliable.
- Keep location and sensor processing on-device where practical, and document battery/privacy impact.

## Licensing and commercial proposal

The original text and code in this directory are offered under **CC BY-NC-ND 4.0 International** for non-commercial sharing with attribution and without distributing adaptations. This public license does not grant commercial-use or derivative-work rights. A separate written commercial license or buyout may be negotiated directly with the author:

**Pol Barreiro Font** — contact via GitHub: [@PolBarreiro](https://github.com/PolBarreiro)

The author is open to an economical agreement; price and scope are negotiable. No price or purchase commitment is implied by this proposal. If Google is interested in a commercial implementation, please contact the author before using this material under a separate agreement.

This is a proposal and prototype, not a patent claim or a guarantee of novelty. Public disclosure may affect the ability to protect an invention; seek qualified IP advice before relying on exclusivity. Submitting the same idea through a product feedback channel may be governed by separate terms and may not create any payment obligation.

## AI assistance

The Python sample was generated with AI assistance from the author's concept. The central concept and the forward-facing-phone assumption are attributed to Pol Barreiro Font.
