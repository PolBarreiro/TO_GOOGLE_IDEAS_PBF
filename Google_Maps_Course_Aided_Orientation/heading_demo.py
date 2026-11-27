"""Illustrative GPS-course + device-heading fusion; not production navigation software.

Concept by Pol Barreiro Font; sample code prepared with AI assistance.
Requires Python 3 and uses only the standard library.
"""
from __future__ import annotations

from dataclasses import dataclass
from math import atan2, cos, radians, sin, sqrt
from typing import Iterable


@dataclass(frozen=True)
class Fix:
    """A GPS fix; heading_deg is optional fused device heading, clockwise from true north."""
    latitude: float
    longitude: float
    time_s: float
    accuracy_m: float
    heading_deg: float | None = None


def bearing_deg(a: Fix, b: Fix) -> float:
    """Initial great-circle bearing from fix a to fix b, clockwise from true north."""
    lat1, lat2 = radians(a.latitude), radians(b.latitude)
    dlon = radians(b.longitude - a.longitude)
    y = sin(dlon) * cos(lat2)
    x = cos(lat1) * sin(lat2) - sin(lat1) * cos(lat2) * cos(dlon)
    return (atan2(y, x) * 180.0 / 3.141592653589793 + 360.0) % 360.0


def distance_m(a: Fix, b: Fix) -> float:
    """Haversine distance in metres."""
    earth_radius_m = 6_371_000.0
    lat1, lat2 = radians(a.latitude), radians(b.latitude)
    dlat = lat2 - lat1
    dlon = radians(b.longitude - a.longitude)
    h = sin(dlat / 2) ** 2 + cos(lat1) * cos(lat2) * sin(dlon / 2) ** 2
    return 2 * earth_radius_m * atan2(sqrt(h), sqrt(1 - h))


def circular_blend_deg(
    first_deg: float, first_weight: float, second_deg: float, second_weight: float
) -> float:
    """Blend compass angles without the 359°/0° wraparound error."""
    x = first_weight * cos(radians(first_deg)) + second_weight * cos(radians(second_deg))
    y = first_weight * sin(radians(first_deg)) + second_weight * sin(radians(second_deg))
    return (atan2(y, x) * 180.0 / 3.141592653589793 + 360.0) % 360.0


def estimate_heading(fixes: Iterable[Fix]) -> dict[str, float | str | None]:
    """Estimate forward direction from recent GPS course and optional device heading.

    Demo policy: reject poor/short GPS baselines; weight usable course by speed and
    fix quality. Real systems should use platform sensor-fusion and calibrated
    uncertainty, not these illustrative thresholds.
    """
    points = sorted(fixes, key=lambda fix: fix.time_s)
    if len(points) < 2:
        return {"heading_deg": None, "gps_course_deg": None, "speed_mps": 0.0,
                "status": "Need at least two GPS fixes"}

    start, end = points[0], points[-1]
    elapsed = end.time_s - start.time_s
    travelled = distance_m(start, end)
    speed = travelled / elapsed if elapsed > 0 else 0.0

    if elapsed <= 0 or travelled < 4.0:
        return {"heading_deg": end.heading_deg, "gps_course_deg": None,
                "speed_mps": speed, "status": "GPS course unavailable; use device heading"}

    course = bearing_deg(start, end)
    gps_quality = max(0.0, min(1.0, 1.0 - max(start.accuracy_m, end.accuracy_m) / 25.0))
    motion_quality = max(0.0, min(1.0, (speed - 0.5) / 2.0))
    course_weight = gps_quality * motion_quality

    if course_weight < 0.15:
        return {"heading_deg": end.heading_deg, "gps_course_deg": course,
                "speed_mps": speed, "status": "GPS course too uncertain; use device heading"}

    if end.heading_deg is None:
        return {"heading_deg": course, "gps_course_deg": course, "speed_mps": speed,
                "status": "Using GPS course"}

    # Illustrative fixed sensor weight. A real app should derive both weights from
    # timestamped sensor uncertainties and account for magnetic declination.
    fused = circular_blend_deg(course, course_weight, end.heading_deg, 0.6)
    return {"heading_deg": fused, "gps_course_deg": course, "speed_mps": speed,
            "status": "Blending GPS course with device heading"}


if __name__ == "__main__":
    # A short north-east walk. Real applications would receive timestamped live fixes.
    sample = [
        Fix(35.68110, 139.76710, 0.0, 8.0, 42.0),
        Fix(35.68118, 139.76720, 5.0, 7.0, 48.0),
        Fix(35.68127, 139.76731, 10.0, 6.0, 50.0),
    ]
    result = estimate_heading(sample)
    print(f"Estimated forward heading: {result['heading_deg']:.1f}°" if result["heading_deg"] is not None
          else f"Estimated forward heading: unavailable ({result['status']})")
    print(f"GPS course: {result['gps_course_deg']!s}° | "
          f"speed: {result['speed_mps']:.2f} m/s | {result['status']}")
