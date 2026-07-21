"""
MAVLink telemetry source.

Currently receives attitude information only.
"""
import math
import time

from pymavlink import mavutil
from telemetrysource import TelemetrySource
from collections.abc import Callable
from logmanager import get_logger
from config import load_config
from aircraft import AircraftState


class MavlinkSource(TelemetrySource):

    

    def __init__(self, connection: str, baudrate: int):
        config = load_config()

        #self.aircraft_state = AircraftState()

        self.logger = get_logger("telemetry")

        self.logger.info(f"Connecting to MAVLink {connection}...")

        self.master = mavutil.mavlink_connection(
            connection,
            baud=baudrate,
        )

        print("Waiting for heartbeat...")

        self.master.wait_heartbeat()
        self.master.mav.request_data_stream_send(
            self.master.target_system,
            self.master.target_component,
            mavutil.mavlink.MAV_DATA_STREAM_EXTRA1,
            20,     # Hz
            1,      # start
        )


        self.logger.info(
            f"Heartbeat received "
            f"(system={self.master.target_system}, "
            f"component={self.master.target_component})"
        )

        # Despatch table for MAVLink message types to handler functions
        self._handlers: dict[
            str,
            Callable[[object, AircraftState], None],
        ] = {
            "ATTITUDE": self._handle_attitude,
            "HEARTBEAT": self._handle_heartbeat,
            "VFR_HUD": self._handle_vfr_hud,
            "SYS_STATUS": self._handle_sys_status,
            "GLOBAL_POSITION_INT": self._handle_global_position_int,
            "GPS_RAW_INT": self._handle_gps_raw_int,
            "MISSION_CURRENT": self._handle_mission_current,
        }

    def update_state(
        self,
        state: AircraftState,
    ) -> None:

        while True:

            msg = self.master.recv_match(blocking=False)

            if msg is None:
                return  

            msg_type = msg.get_type()

            handler = self._handlers.get(msg_type)

            if handler is None:
                # if msg_type not in self._unknown_messages:
                #     self.logger.info(
                #         f"No handler for {msg_type}"
                #     )
                #     self._unknown_messages.add(msg_type)
                
                continue

            handler(msg, state)
            
    def _handle_attitude(
        self,
        msg,
        state: AircraftState,
    ) -> None:
        """
        Decode ATTITUDE.

        Updates:
            roll
            pitch
            heading
        """
       
        state.roll = math.degrees(msg.roll)
        state.pitch = math.degrees(msg.pitch)
        state.heading = (
            math.degrees(msg.yaw) + 360
        ) % 360

        state.last_update = time.monotonic()
 
    def _handle_heartbeat(
        self,
        msg,
        state: AircraftState,
    ) -> None:
        """
        Decode HEARTBEAT.

        Updates:
            armed
            flight_mode
        """
        state.armed = bool(
            msg.base_mode &
            mavutil.mavlink.MAV_MODE_FLAG_SAFETY_ARMED
        )

        state.flight_mode = mavutil.mode_string_v10(msg)

    def _handle_vfr_hud(
        self,
        msg,
        state: AircraftState,
    ) -> None:
        """
        Decode VFR_HUD.

        Updates:
        airspeed
        groundspeed
        altitude
        climb_rate
        """

        state.airspeed = msg.airspeed
        state.groundspeed = msg.groundspeed
        state.altitude = msg.alt
        state.climb_rate = msg.climb

        state.last_update = time.monotonic()

    def _handle_sys_status(        
            self,
            msg,
            state: AircraftState,
        ) -> None:

        state.battery_voltage = (
            msg.voltage_battery / 1000.0
        )

        state.battery_current = (
            msg.current_battery / 100.0
            if msg.current_battery >= 0
            else None
        )

        state.battery_remaining = (
            msg.battery_remaining
            if msg.battery_remaining >= 0
            else None
        )

        state.last_update = time.monotonic()

    def _handle_global_position_int(
        self,
        msg,
        state: AircraftState,
    ) -> None:

        state.latitude = msg.lat / 1e7
        state.longitude = msg.lon / 1e7
        state.altitude = msg.alt / 1000.0
        state.relative_altitude = msg.relative_alt / 1000.0

        state.last_update = time.monotonic()

    def _handle_gps_raw_int(
        self,
        msg,
        state: AircraftState,
    ) -> None:

        state.gps_altitude = msg.alt / 1000.0
        state.satellites_visible = msg.satellites_visible
        state.gps_fix_type = msg.fix_type
        state.hdop = msg.eph / 100.0 if msg.eph >= 0 else None
        state.vdop = msg.epv / 100.0 if msg.epv >= 0 else None

        state.last_update = time.monotonic()

    def _handle_mission_current(
        self,
        msg,
        state: AircraftState,
    ) -> None:

        state.seq = msg.seq

        state.last_update = time.monotonic()

        