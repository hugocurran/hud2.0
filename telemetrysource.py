"""
Telemetry source interface.

All telemetry providers implement this interface.
"""

from __future__ import annotations

from abc import ABC, abstractmethod


class TelemetrySource(ABC):

    @abstractmethod
    def get(self):
        """
        Return the latest telemetry state.
        """
        raise NotImplementedError
    