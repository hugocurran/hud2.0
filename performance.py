"""
performance.py

Lightweight performance monitoring.

When enabled, timing statistics are accumulated and reported
periodically via the logging system.

When disabled, a NullPerformance object provides the same API
with negligible overhead.
"""

from __future__ import annotations

from dataclasses import dataclass
import time


# ----------------------------------------------------------------------
# Statistics
# ----------------------------------------------------------------------

@dataclass
class TimerStats:

    count: int = 0
    total: float = 0.0
    minimum: float | None = None
    maximum: float | None = None

    def __post_init__(self):
        self._clear()

    def update(self, elapsed: float):

        self.count += 1
        self.total += elapsed
        
        if self.minimum is None:
            self.minimum = elapsed
            self.maximum = elapsed
        else:
            self.minimum = min(self.minimum, elapsed)
            self.maximum = max(self.maximum, elapsed)

    @property
    def average(self):

        if self.count == 0:
            return 0.0

        return self.total / self.count

    @property
    def average_ms(self):
        return self.average * 1000.0

    @property
    def minimum_ms(self):
        return self.minimum * 1000.0
    
    @property
    def maximum_ms(self):
        return self.maximum * 1000.0
    
    def reset(self):
        self._clear()

    def _clear(self):
        self.count = 0
        self.total = 0.0
        self.minimum = None
        self.maximum = None


# ----------------------------------------------------------------------
# Timer context manager
# ----------------------------------------------------------------------

class PerformanceTimer:

    def __init__(self, monitor, name):

        self.monitor = monitor
        self.name = name
        self.start = 0.0

    def __enter__(self):

        self.start = time.perf_counter()
        return self

    def __exit__(self, exc_type, exc_value, traceback):

        elapsed = time.perf_counter() - self.start
        self.monitor.record(self.name, elapsed)

        return False


# ----------------------------------------------------------------------
# Null timer
# ----------------------------------------------------------------------

class NullTimer:

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_value, traceback):
        return False


# ----------------------------------------------------------------------
# Enabled monitor
# ----------------------------------------------------------------------

class PerformanceMonitor:

    def __init__(
        self,
        logger,
        report_interval=10.0,
    ):

        self.logger = logger
        self.report_interval = report_interval

        self.statistics = {}

        self.next_report = (
            time.monotonic()
            + report_interval
        )

    def timer(self, name):

        return PerformanceTimer(
            self,
            name,
        )

    def record(
        self,
        name,
        elapsed,
    ):

        stats = self.statistics.setdefault(
            name,
            TimerStats(),
        )

        stats.update(elapsed)

        if time.monotonic() >= self.next_report:

            self.report()

            self.next_report = (
                time.monotonic()
                + self.report_interval
            )

    def report(self):

        #
        # Implement later.
        #
        pass


# ----------------------------------------------------------------------
# Disabled monitor
# ----------------------------------------------------------------------

class NullPerformance:

    def timer(self, name):

        return NullTimer()

    def report(self):

        pass