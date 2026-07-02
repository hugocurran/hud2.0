"""
MAVLink telemetry source.

Currently receives attitude information only.
"""
import math
import time

from pymavlink import mavutil
from telemetrysource import TelemetrySource
from telemetry import TelemetryState
from collections import Counter
from collections.abc import Callable


class MavlinkSource(TelemetrySource):

    def __init__(self, connection: str, baudrate: int):

        self.stats = Counter()  

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

        self._handlers: dict[
            str,
            Callable[[object, TelemetryState], None],
        ] = {
            "ATTITUDE": self._handle_attitude,
        }

    def update_state(
        self,
        state: TelemetryState,
    ) -> None:

        while True:

            msg = self.master.recv_match(blocking=False)

            if msg is None:
                break

            if msg.get_type() == "BAD_DATA":
                continue

            handler = self._handlers.get(msg.get_type())

            if handler is not None:
                handler(msg, state)
            
    def _handle_attitude(
        self,
        msg,
        state: TelemetryState,
    ) -> None:

        state.roll = math.degrees(msg.roll)
        state.pitch = math.degrees(msg.pitch)
        state.heading = (
            math.degrees(msg.yaw) + 360
        ) % 360

        state.last_update = time.monotonic()

        