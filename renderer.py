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
from hudgeometry import HudGeometry


class Renderer:

    def __init__(self):

        self.geometry = None

        self.frame_counter = 0

    # ---------------------------------------------------------

    def process(
            self,
            frame: np.ndarray,
            state,
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

    def draw_horizon(self, frame, state):

        line = self.geometry.horizon(
            state.roll,
            state.pitch,
        )

        self.draw_line(frame, line)


    # ---------------------------------------------------------

    def draw_pitch_ladder(self, frame, state):

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

    # def draw_pitch_ladder(self, frame, state):

    #     aircraft_pitch_px = (
    #         state.pitch * HudStyle.PITCH_SCALE
    #     )

    #     for mark in range(-30, 35, 5):

    #         if mark == 0:
    #             continue

    #         major = abs(mark) % 10 == 0

    #         # pitch = self.geometry.pitch_mark(
    #         #     state.roll,
    #         #     state.pitch,
    #         #     mark,
    #         # )
            
    #         ladder = self.geometry.ladder_mark(
    #             mark,
    #             state.roll,
    #             aircraft_pitch_px,
    #             major,
    #         )

    #         # print (line)
    #         self.draw_line(frame, pitch)

    #         # End caps
    #         cv2.line(
    #             frame,
    #             pitch.p1,
    #             pitch.left_cap,
    #             HudStyle.COLOUR,
    #             HudStyle.LINE_WIDTH,
    #             cv2.LINE_AA,
    #         )

    #         cv2.line(
    #             frame,
    #             pitch.p2,
    #             pitch.right_cap,
    #             HudStyle.COLOUR,
    #             HudStyle.LINE_WIDTH,
    #             cv2.LINE_AA,
    #         )

    #         if mark % 10 == 0:

    #             text = str(abs(mark))

    #             (text_width, text_height), _ = cv2.getTextSize(
    #                 text,
    #                 HudStyle.FONT,
    #                 HudStyle.PITCH_LABEL_FONT_SCALE,
    #                 HudStyle.PITCH_LABEL_THICKNESS,
    #         )               

    #             left_pos = (
    #                 pitch.left_text[0] - text_width,
    #                 pitch.left_text[1],
    #             )

    #             right_pos = pitch.right_text

    #             cv2.putText(
    #                 frame,
    #                 text,
    #                 left_pos,
    #                 HudStyle.FONT,
    #                 HudStyle.PITCH_LABEL_FONT_SCALE,
    #                 HudStyle.COLOUR,
    #                 HudStyle.PITCH_LABEL_THICKNESS,
    #             cv2.LINE_AA,
    #             )

    #             cv2.putText(
    #                 frame,
    #                 text,
    #                 right_pos,
    #                 HudStyle.FONT,
    #                 HudStyle.PITCH_LABEL_FONT_SCALE,
    #                 HudStyle.COLOUR,
    #                 HudStyle.PITCH_LABEL_THICKNESS,
    #                 cv2.LINE_AA,
    #             )

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

    def draw_status(self, frame, state):

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

    def draw_line(self, frame, line):

        cv2.line(
            frame,
            line.p1,
            line.p2,
            HudStyle.COLOUR,
            HudStyle.LINE_WIDTH,
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

    def draw_roll_scale(self, frame, state):

        for tick in self.geometry.roll_ticks(state.roll):

            self.draw_line(frame, tick)

            if tick.major:

                 cv2.putText(
                      frame,
                      str(abs(tick.angle)),
                      tick.text,
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

