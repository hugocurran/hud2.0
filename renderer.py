"""
renderer.py

HUD Renderer

Responsible only for drawing.
Geometry is handled by hudgeometry.py.
"""

from __future__ import annotations

import cv2
import numpy as np

from hudstyle import HudStyle
from hudgeometry import HudGeometry, Point, Line
from aircraft import AircraftState


class Renderer:

    ALIGN_LEFT = "left"
    ALIGN_RIGHT = "right" 

    def __init__(self):

        self.geometry = None

        self.frame_counter = 0


    # ---------------------------------------------------------

    def process(
            self,
            frame: np.ndarray,
            state: AircraftState,
            ) -> np.ndarray:

        self.frame_counter += 1
  
        h, w = frame.shape[:2]

        if (
            self.geometry is None
            or self.geometry.width != w
            or self.geometry.height != h
        ):
            self.geometry = HudGeometry(w, h)

        #
        # Draw HUD
        #

        self.draw_horizon(frame, state)

        self.draw_pitch_ladder(frame, state)

        self.draw_roll_scale(frame, state)

        self.draw_roll_pointer(frame)

        self.draw_aircraft_symbol(frame)

        self.draw_status(frame, state)

        self.draw_frame_counter(frame)

        return frame

    # ---------------------------------------------------------

    def draw_horizon(self, frame, state: AircraftState):

        horizon = self.geometry.horizon(
            state.roll,
            state.pitch,
        )

        self.draw_line(
            frame,
            horizon.line,
        )


    # ---------------------------------------------------------

    def draw_pitch_ladder(self, frame, state: AircraftState):

        
        aircraft_pitch_px = (
            state.pitch * HudStyle.PITCH_SCALE
        )

        for mark in range(-30, 35, 5):

            if mark == 0:
                continue

            major = abs(mark) % 10 == 0

            ladder = self.geometry.ladder_mark(
                mark,
                state.roll,
                aircraft_pitch_px,
                major,
            )

            self.draw_line(
                frame,
                ladder.centre_line,
            )

            if ladder.left_cap is not None:
                self.draw_line(
                    frame,
                    ladder.left_cap,
            )

            if ladder.right_cap is not None:
                self.draw_line(
                    frame,
                    ladder.right_cap,
                )

            if major:

                self.draw_label(
                    frame,
                    ladder.label,
                    ladder.left_label,
                    align=self.ALIGN_RIGHT,
                )

                self.draw_label(
                    frame,
                    ladder.label,
                    ladder.right_label,
                    align=self.ALIGN_LEFT,
                )

    # ---------------------------------------------------------

    def draw_aircraft_symbol(self, frame):

        h, w = frame.shape[:2]

        cx = w // 2
        cy = h // 2

        gap = 12
        wing = 32
        stem = 14

        #
        # left wing
        #

        cv2.line(
            frame,
            (cx - gap - wing, cy),
            (cx - gap, cy),
            HudStyle.COLOUR,
            HudStyle.LINE_WIDTH,
        )

        # 
        # right wing
        #

        cv2.line(
            frame,
            (cx + gap, cy),
            (cx + gap + wing, cy),
            HudStyle.COLOUR,
            HudStyle.LINE_WIDTH,
        )

        #
        # centre post
        #

        cv2.line(
            frame,
            (cx, cy - stem),
            (cx, cy + stem),
            HudStyle.COLOUR,
            HudStyle.LINE_WIDTH,
        )

    # ---------------------------------------------------------

    def draw_status(self, frame, state: AircraftState):

        x = 20
        y = 40

        lines = [

            f"Roll     {state.roll:6.1f}",

            f"Pitch    {state.pitch:6.1f}",

            f"Heading  {state.heading:6.1f}",

            f"Altitude {state.altitude:7.1f} m",

            (
                f"Battery {state.battery_remaining:3d} %"
                if state.battery_remaining is not None
                else "Battery --- %"
            ),
        ]

        for text in lines:

            cv2.putText(
                frame,
                text,
                (x, y),
                HudStyle.FONT,
                HudStyle.FONT_SCALE,
                HudStyle.COLOUR,
                HudStyle.LINE_WIDTH,
                cv2.LINE_AA,
            )

            y += 26

    # ---------------------------------------------------------
    # ---------------------------------------------------------

    def draw_line(self, frame, line: Line) -> None:

        cv2.line(
            frame,
            (line.start.x, line.start.y),
            (line.end.x, line.end.y),
            HudStyle.COLOUR,
            HudStyle.LINE_WIDTH,
            cv2.LINE_AA,
        )

    def draw_label(
        self,
        frame,
        text: str,
        position: Point,
        align: str = "left",
    ) -> None:
        
        (text_width, text_height), _ = cv2.getTextSize(
            text,
            HudStyle.FONT,
            HudStyle.PITCH_LABEL_FONT_SCALE,
            HudStyle.PITCH_LABEL_THICKNESS,
        )

        x = position.x

        if align == self.ALIGN_RIGHT:
            x -= text_width

        cv2.putText(
            frame,
            text,
            (x, position.y),
            HudStyle.FONT,
            HudStyle.PITCH_LABEL_FONT_SCALE,
            HudStyle.COLOUR,
            HudStyle.PITCH_LABEL_THICKNESS,
            cv2.LINE_AA,
        )        

    def draw_frame_counter(self, frame):

        cv2.putText(
            frame,
            f"Frame {self.frame_counter}",
            (20, frame.shape[0] - 20),
            HudStyle.FONT,
            HudStyle.FONT_SCALE,
            HudStyle.COLOUR,
            HudStyle.LINE_WIDTH,
            cv2.LINE_AA,
        )

    def draw_roll_scale(self, frame, state: AircraftState):

        horizon = self.geometry.horizon(
            state.roll,
            state.pitch,
        )

        self.draw_line(
            frame,
            horizon.line,
        )

        scale = self.geometry.roll_scale(
            horizon,
            state.roll,
        )
        for mark in scale.marks:
            self.draw_line(frame, mark.tick)

            if mark.major:
                 self.draw_label(
                    frame,
                    str(abs(mark.angle)),
                    mark.label,
                    align=self.ALIGN_LEFT,
                 )
                 cv2.putText(
                      frame,
                      str(abs(mark.angle)),
                      (mark.label.x, mark.label.y),
                      HudStyle.FONT,
                      HudStyle.ROLL_LABEL_FONT_SCALE,
                      HudStyle.COLOUR,
                      HudStyle.ROLL_LABEL_THICKNESS,
                      cv2.LINE_AA,
                 )
                

    def draw_roll_pointer(self, frame):

        points = np.array(
            self.geometry.roll_pointer(),
            dtype=np.int32,
        )

        cv2.fillConvexPoly(
            frame,
            points,
            HudStyle.COLOUR,
            cv2.LINE_AA,
        )

