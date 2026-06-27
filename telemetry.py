"""
Telemetry model.

Currently generates simulated telemetry.
Later this class will be fed by pymavlink.
"""

from __future__ import annotations

from dataclasses import dataclass
import math
import time


@dataclass(slots=True)
class TelemetryState:
    roll: float = 0.0
    pitch: float = 0.0
    heading: float = 0.0
    altitude: float = 0.0
    battery_percent: int = 100


class Telemetry:

    def __init__(self):

        self.state = TelemetryState()

    def update(self):

        t = time.time()

        self.state.roll = 30.0 * math.sin(t * 0.5)
        self.state.pitch = 15.0 * math.sin(t * 0.35)
        self.state.heading = (t * 10.0) % 360.0
        self.state.altitude = 123.4
        self.state.battery_percent = 87

    def get(self) -> TelemetryState:

        self.update()
        return self.state