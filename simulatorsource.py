"""
Simulated telemetry source.
"""

from __future__ import annotations

import math
import time

from telemetry import TelemetryState
from telemetrysource import TelemetrySource


class SimulatorSource(TelemetrySource):

    def update_state(
        self,
        state: TelemetryState,
    ) -> None:

        t = time.time()

        state.roll = 30.0 * math.sin(t * 0.5)
        state.pitch = 15.0 * math.sin(t * 0.35)
        state.heading = (t * 10.0) % 360.0
        state.altitude = 123.4
        state.battery_percent = 87
        
    