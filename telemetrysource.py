"""
Telemetry source interface.

All telemetry providers implement this interface.
"""

from __future__ import annotations

from abc import ABC, abstractmethod

from aircraft import AircraftState


class TelemetrySource(ABC):
    """Abstract base class for telemetry providers."""

    def start(self) -> None:
        """Start the telemetry source."""

    def stop(self) -> None:
        """Stop the telemetry source."""

    @abstractmethod
    def update_state(
        self,
        state: AircraftState,
    ) -> None:
        """
        Update the supplied telemetry state.
        """
        raise NotImplementedError
    