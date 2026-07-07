"""
Telemetry manager.

Owns the current telemetry state and updates it using the
configured telemetry source.
"""

from __future__ import annotations

import threading
import time


from aircraft import AircraftState
from telemetrysource import TelemetrySource
from dataclasses import replace


class TelemetryManager:

    def __init__(self, source: TelemetrySource):

        self._source = source
        self._state = AircraftState()
        self._lock = threading.Lock()
        self._running = False
        self._thread: threading.Thread | None = None

    def start(self) -> None:

        self._running = True

        self._thread = threading.Thread(
            target=self._worker,
            daemon=True,
        )

        self._thread.start()

    def stop(self) -> None:
        self._running = False

        if self._thread is not None:
            self._thread.join()

        self._source.stop()

    def get_state(self) -> AircraftState:
        with self._lock:
            return replace(self._state)
    
    def _worker(self) -> None:

        while self._running:

            with self._lock:
                self._source.update_state(self._state)

            time.sleep(0.01)
    