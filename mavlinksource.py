"""
MAVLink telemetry source.

Currently receives attitude information only.
"""
import math
import time

from pymavlink import mavutil
from telemetrysource import TelemetrySource
from telemetry import TelemetryState
from collections.abc import Callable
from util import get_logger
from config import load_config


class MavlinkSource(TelemetrySource):

    

    def __init__(self, connection: str, baudrate: int):
        config = load_config()

        self.logger = get_logger(
            "mavlink",
            config.logging.level,
        )

        print(f"Connecting to {connection}...")

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


        print(
            f"Heartbeat received "
            f"(system={self.master.target_system}, "
            f"component={self.master.target_component})"
        )

        # Despatch table for MAVLink message types to handler functions
        self._handlers: dict[
            str,
            Callable[[object, TelemetryState], None],
        ] = {
            "ATTITUDE": self._handle_attitude,
            "HEARTBEAT": self._handle_heartbeat,
        }

    def update_state(
        self,
        state: TelemetryState,
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
        state: TelemetryState,
    ) -> None:
        """
        Decode ATTITUDE.

        Updates:
            roll
            pitch
            heading
        """
        state.roll = -math.degrees(msg.roll)
        state.pitch = math.degrees(msg.pitch)
        state.heading = (
            math.degrees(msg.yaw) + 360
        ) % 360

        state.last_update = time.monotonic()
 
    def _handle_heartbeat(
        self,
        msg,
        state: TelemetryState,
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

        