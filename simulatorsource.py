"""
Simulated telemetry source.
"""

from telemetry import Telemetry, TelemetryState
from telemetrysource import TelemetrySource


class SimulatorSource(TelemetrySource):

    def __init__(self):
        self.telemetry = Telemetry()

    def get_state(self) -> TelemetryState:
        return self.telemetry.get_state()
    