"""
Renderer.

Currently draws a simple HUD using simulated telemetry.
"""

from __future__ import annotations

import cv2
import numpy as np
import math

from telemetry import Telemetry
from hudtransform import HudTransform
from hudstyle import HudStyle

class Renderer:

    def __init__(self):
        self.transform = None
        self.hud_transform = HudTransform(width=640, height=480)

        self.frame_counter = 0
        self.telemetry = Telemetry()

    def process(self, frame: np.ndarray) -> np.ndarray:

        self.frame_counter += 1

        state = self.telemetry.get()

        h, w = frame.shape[:2]

        if (
            self.transform is None
            or self.transform.width != w
            or self.transform.height != h
        ):
            self.transform = HudTransform(w, h)

        self.draw_frame_counter(frame)
        print("draw_horizon", state.roll, state.pitch)
        self.draw_horizon(frame, state)
        self.draw_crosshair(frame)
        self.draw_text(frame, state)

        return frame
    
    

    def draw_horizon(self, frame, state):

        h, w = frame.shape[:2]

        # Fixed aircraft boresight
        cx = w // 2
        cy = h // 2

        # Convert to radians
        roll = math.radians(state.roll)

        # Pitch moves the horizon vertically
        horizon_y = cy + state.pitch * HudStyle.PITCH_SCALE

        dx = math.cos(roll)
        dy = math.sin(roll)

        length = HudStyle.HORIZON_LENGTH

        # Horizon line
        x1 = int(cx - dx * length)
        y1 = int(horizon_y - dy * length)

        x2 = int(cx + dx * length)
        y2 = int(horizon_y + dy * length)

        cv2.line(
            frame,
            (x1, y1),
            (x2, y2),
            HudStyle.COLOUR,
            HudStyle.LINE_WIDTH,
            cv2.LINE_AA,
        )

        # Draw pitch ladder
        for pitch in range(-30, 35, 5):

            if pitch == 0:
                continue

            self.draw_pitch_mark(
                frame,
                roll,
                cx,
                cy,
                state,
                pitch,
            )
    


    def draw_frame_counter(self, frame):

        cv2.putText(
            frame,
            f"Frame {self.frame_counter}",
            (20, 40),
            cv2.FONT_HERSHEY_SIMPLEX,
            1.0,
            (0, 255, 0),
            2,
            cv2.LINE_AA,
        )

    def draw_crosshair(self, frame):

        h, w = frame.shape[:2]

        cx = w // 2
        cy = h // 2

        cv2.line(frame, (cx - 20, cy), (cx + 20, cy), (0, 255, 0), 2)
        cv2.line(frame, (cx, cy - 20), (cx, cy + 20), (0, 255, 0), 2)

    def draw_text(self, frame, state):

        x = 20
        y = 80

        lines = [
            f"Roll      : {state.roll:5.1f}",
            f"Pitch     : {state.pitch:5.1f}",
            f"Heading   : {state.heading:5.1f}",
            f"Altitude  : {state.altitude:6.1f} m",
            f"Battery   : {state.battery_percent:3d} %",
        ]

        for line in lines:

            cv2.putText(
                frame,
                line,
                (x, y),
                cv2.FONT_HERSHEY_SIMPLEX,
                0.7,
                (0, 255, 0),
                2,
                cv2.LINE_AA,
            )

            y += 30

    def draw_pitch_mark(
        self,
        frame,
        roll,
        cx,
        cy,
        state,
        pitch_mark,
    ):

        import math

        dx = math.cos(roll)
        dy = math.sin(roll)

        nx = -dy
        ny = dx

        offset = (pitch_mark - state.pitch) * HudStyle.PITCH_SCALE

        mx = cx + nx * offset
        my = cy + ny * offset

        half = HudStyle.LADDER_HALF_WIDTH

        x1 = int(mx - dx * half)
        y1 = int(my - dy * half)

        x2 = int(mx + dx * half)
        y2 = int(my + dy * half)

        cv2.line(
            frame,
            (x1, y1),
            (x2, y2),
            HudStyle.COLOUR,
            HudStyle.LINE_WIDTH,
            cv2.LINE_AA,
        )
