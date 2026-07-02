"""
Telemetry source interface.

All telemetry providers implement this interface.
"""

from __future__ import annotations

from abc import ABC, abstractmethod

from telemetry import TelemetryState


class TelemetrySource(ABC):
    """Abstract base class for telemetry providers."""

    def start(self) -> None:
        """
        Start the telemetry source.

        Override if the source requires a worker thread
        or other background resources.
        """

    def stop(self) -> None:
        """
        Stop the telemetry source.

        Override if cleanup is required.
        """

    @abstractmethod
    def get_state(self) -> TelemetryState:
        """
        Return the latest telemetry state.
        """
        raise NotImplementedError
    