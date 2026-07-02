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


class MavlinkSource(TelemetrySource):

    def __init__(self, connection: str, baudrate: int):

        self.state = TelemetryState()
        self.last_update = time.monotonic()
        self.badcount =0
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


    def get_state(self) -> TelemetryState:

        while True:

            msg = self.master.recv_match(blocking=False)

            if msg is None:
                break

            if msg.get_type() == "BAD_DATA":
                continue

            if msg.get_type() == "ATTITUDE":
                self.state.roll = math.degrees(msg.roll)
                self.state.pitch = math.degrees(msg.pitch)
                self.state.heading = (
                    math.degrees(msg.yaw) + 360.0
                ) % 360.0
            
        return self.state

        