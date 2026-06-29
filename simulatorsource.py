"""
Simulated telemetry source.
"""

from telemetry import Telemetry
from telemetrysource import TelemetrySource


class SimulatorSource(TelemetrySource):

    def __init__(self):
        self.telemetry = Telemetry()

    def get(self):
        return self.telemetry.get()
    