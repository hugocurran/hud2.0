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

    # # --------------------------
    # # Attitude
    # # --------------------------

    # roll: float = 0.0          # degrees
    # pitch: float = 0.0         # degrees
    # heading: float = 0.0       # degrees (0-360)

    # # --------------------------
    # # Flight
    # # --------------------------

    # altitude: float = 0.0      # metres MSL
    # airspeed: float | None = None      # m/s
    # groundspeed: float | None = None   # m/s
    # vertical_speed: float | None = None  # m/s

    # # --------------------------
    # # GPS
    # # --------------------------

    # latitude: float | None = None
    # longitude: float | None = None

    # satellites: int | None = None

    # hdop: float | None = None
    # vdop: float | None = None

    # # --------------------------
    # # Battery
    # # --------------------------

    # battery_voltage: float | None = None   # volts
    # battery_current: float | None = None   # amps
    # battery_remaining: int | None = None   # percent

    # # --------------------------
    # # Vehicle
    # # --------------------------

    # armed: bool = False
    # flight_mode: str = ""

    # --------------------------
    # Timing
    # --------------------------

    last_update: float = 0.0


