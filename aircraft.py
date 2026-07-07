
from __future__ import annotations

from dataclasses import dataclass



@dataclass
class AircraftState:
    # --------------------------
    # Attitude
    # --------------------------

    roll: float = 0.0          # degrees
    pitch: float = 0.0         # degrees
    heading: float = 0.0       # degrees (0-360)

    # --------------------------
    # Flight
    # --------------------------

    altitude: float = 0.0      # metres MSL
    relative_altitude: float | None = None  # metres AGL
    airspeed: float | None = None      # m/s
    groundspeed: float | None = None   # m/s
    vertical_speed: float | None = None  # m/s

    # --------------------------
    # GPS
    # --------------------------

    latitude: float | None = None
    longitude: float | None = None

    satellites_visible: int | None = None
    gps_fix_type: int | None = None
    gps_altitude: float | None = None

    hdop: float | None = None
    vdop: float | None = None

    # --------------------------
    # Battery
    # --------------------------

    battery_voltage: float | None = None   # volts
    battery_current: float | None = None   # amps
    battery_remaining: int | None = None   # percent

    # --------------------------
    # Vehicle
    # --------------------------

    armed: bool = False
    flight_mode: str = ""

    #----------------------------
    # Mission
    #-----------------------------
    target_bearing: float | None = None
    target_distance: float | None = None 
    cross_track_error: float | None = None
    seq: int | None = None  #current waypoint sequence number


