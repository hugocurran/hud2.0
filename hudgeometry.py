"""
HUD geometry calculations.

Contains no OpenCV drawing code.
"""

from __future__ import annotations

from dataclasses import dataclass
import math

from hudstyle import HudStyle


@dataclass
class Line:

    p1: tuple[int, int]
    p2: tuple[int, int]

@dataclass
class RollTick:

    p1: tuple[int, int]
    p2: tuple[int, int]

    text: tuple[int, int]

    angle: int

    major: bool


class HudGeometry:

    def __init__(self, width: int, height: int):

        self.width = width
        self.height = height

        self.cx = width // 2
        self.cy = height // 2

    def horizon(self, roll_deg: float, pitch_deg: float) -> Line:
        """
        Return the current horizon line.
        """

        roll = math.radians(roll_deg)

        dx, dy = self._rotation(roll_deg)

        y = self.cy + pitch_deg * HudStyle.PITCH_SCALE

        L = HudStyle.HORIZON_LENGTH

        x1 = int(self.cx - dx * L)
        y1 = int(y - dy * L)

        x2 = int(self.cx + dx * L)
        y2 = int(y + dy * L)

        return Line(
            (x1, y1),
            (x2, y2),
        )

    def pitch_mark(
        self,
        roll_deg: float,
        aircraft_pitch: float,
        mark_pitch: float,
    ) -> Line:
        """
        Return one pitch ladder mark.
        """

        dx, dy = self._rotation(roll_deg)

        nx, ny = self._normal(dx, dy)

        offset = (
            mark_pitch - aircraft_pitch
        ) * HudStyle.PITCH_SCALE

        mx = self.cx + nx * offset
        my = self.cy + ny * offset

        half = (
            HudStyle.PITCH_MAJOR_WIDTH
            if mark_pitch % 10 == 0
            else HudStyle.PITCH_MINOR_WIDTH
        )

        x1 = int(mx - dx * half)
        y1 = int(my - dy * half)

        x2 = int(mx + dx * half)
        y2 = int(my + dy * half)

        return Line(
            (x1, y1),
            (x2, y2),
        )
    
    def roll_ticks(self, roll_deg: float) -> list[RollTick]:

        ticks = []

        for angle in (-60, -45, -30, -20, -10, 10, 20, 30, 45, 60):

            major = angle in (-60, -30, 30, 60)

            length = (
                HudStyle.ROLL_MAJOR_TICK
                if major
                else HudStyle.ROLL_MINOR_TICK
            )

            radians = math.radians(angle + roll_deg)

            sx = math.sin(radians)
            cy = math.cos(radians)

            x1 = int(self.cx + sx * HudStyle.ROLL_RADIUS)
            y1 = int(self.cy - cy * HudStyle.ROLL_RADIUS)

            x2 = int(self.cx + sx * (HudStyle.ROLL_RADIUS - length))
            y2 = int(self.cy - cy * (HudStyle.ROLL_RADIUS - length))

            label_radius = (
                HudStyle.ROLL_RADIUS 
                + HudStyle.ROLL_LABEL_OFFSET
            )

            tx = int(self.cx + sx * label_radius)
            ty = int(self.cy - cy * label_radius)

            ticks.append(
                RollTick(
                    (x1, y1),
                    (x2, y2),
                    (tx, ty),
                    angle,
                    major,
                )
            )

        return ticks
    
    def roll_pointer(self):

        size = HudStyle.ROLL_POINTER_SIZE

        base_y = (
            self.cy
            - HudStyle.ROLL_RADIUS
            + HudStyle.ROLL_POINTER_OFFSET
        )

        tip = (
            self.cx,
            base_y,
        )

        left = (
            self.cx - size,
            base_y + size,
        )

        right = (
            self.cx + size,
            base_y + size,
        )

        return (
            tip,
            left,
            right,
        )
        
    def _rotation(self, roll_deg: float):

        roll = math.radians(roll_deg)

        return (
            math.cos(roll),
            math.sin(roll),
        )
    
    def _normal(self, dx: float, dy: float) -> tuple[float, float]:
        return -dy, dx
    