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

# @dataclass
# class PitchMark:

#     p1: tuple[int, int]
#     p2: tuple[int, int]

#     left_cap: tuple[int, int]
#     right_cap: tuple[int, int]

#     left_text: tuple[int, int]
#     right_text: tuple[int, int]

#     value: int

@dataclass
class LadderMark:
    """
    Geometry for a single pitch ladder mark.

    All coordinates are already transformed into screen coordinates.
    """

    centre_line: Line | None

    left_cap: Line | None

    right_cap: Line | None

    left_label: tuple[int, int] | None = None

    right_label: tuple[int, int] | None = None

    label: str | None = None


@dataclass
class LadderRung:
    pitch: int
    width: int   

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

        pitch_px = pitch_deg * HudStyle.PITCH_SCALE
        L = HudStyle.HORIZON_LENGTH

        p1 = self._aircraft_to_screen(
            -L,
            0,
            roll_deg,
            pitch_px,
        )

        p2 = self._aircraft_to_screen(
            L,
            0,
            roll_deg,
            pitch_px,
        )

        return Line(p1, p2)

    # def horizon(self, roll_deg: float, pitch_deg: float) -> Line:
    #     """
    #     Return the current horizon line.
    #     """
    #     dx, dy = self._rotation(roll_deg)

    #     y = self.cy + pitch_deg * HudStyle.PITCH_SCALE

    #     L = HudStyle.HORIZON_LENGTH

    #     x1 = int(self.cx - dx * L)
    #     y1 = int(y - dy * L)

    #     x2 = int(self.cx + dx * L)
    #     y2 = int(y + dy * L)

    #     return Line(
    #         (x1, y1),
    #         (x2, y2),
    #     )

    # def pitch_mark(
    #     self,
    #     roll_deg: float,
    #     aircraft_pitch: float,
    #     mark_pitch: float,
    # ) -> Line:
    #     """
    #     Return one pitch ladder mark.
    #     """

    #     dx, dy = self._rotation(roll_deg)

    #     nx, ny = self._normal(dx, dy)

    #     offset = (
    #         mark_pitch - aircraft_pitch
    #     ) * HudStyle.PITCH_SCALE

    #     mx = self.cx + nx * offset
    #     my = self.cy + ny * offset

    #     half = (
    #         HudStyle.PITCH_MAJOR_WIDTH
    #         if mark_pitch % 10 == 0
    #         else HudStyle.PITCH_MINOR_WIDTH
    #     )

    #     cap = HudStyle.PITCH_CAP_LENGTH

    #     x1 = int(mx - dx * half)
    #     y1 = int(my - dy * half)

    #     x2 = int(mx + dx * half)
    #     y2 = int(my + dy * half)

    #     cap = HudStyle.PITCH_CAP_LENGTH

    #     left_cap = (
    #         int(x1 + nx * cap),
    #         int(y1 + ny * cap),
    #     )

    #     right_cap = (
    #         int(x2 + nx * cap),
    #         int(y2 + ny * cap),
    #     )

    #     offset = HudStyle.PITCH_LABEL_OFFSET

    #     left_text = (
    #         int(x1 - dx * offset),
    #         int(y1 - dy * offset),
    #     )

    #     right_text = (
    #         int(x2 + dx * offset),
    #         int(y2 + dy * offset),
    #     )

    #     return PitchMark(
    #         (x1, y1),
    #         (x2, y2),
    #         left_cap,
    #         right_cap, 
    #         left_text,
    #         right_text,
    #         mark_pitch,
    #     )

    def ladder_mark(
        self,
        pitch: int,
        roll_deg: float,
        aircraft_pitch_px: float,
        major: bool,
    ) -> LadderMark:

        width = (
            HudStyle.PITCH_MAJOR_WIDTH
            if major
            else HudStyle.PITCH_MINOR_WIDTH
        )

        mark_y = pitch * HudStyle.PITCH_SCALE
        cap = HudStyle.PITCH_CAP_LENGTH / 2

        centre_line = self._aircraft_line(
            -width,
            mark_y,
            width,
            mark_y,
            roll_deg,
            aircraft_pitch_px,
        )

        left_cap = self._aircraft_line(
            -width,
            mark_y + cap,
            -width,
            mark_y - cap,
            roll_deg,
            aircraft_pitch_px,
        )

        right_cap = self._aircraft_line(
            width,
            mark_y + cap,
            width,
            mark_y - cap,
            roll_deg,
            aircraft_pitch_px,
        )

        left_label = self._aircraft_to_screen(
            -width - HudStyle.PITCH_LABEL_OFFSET,
            mark_y,
            roll_deg,
            aircraft_pitch_px,
        )

        right_label = self._aircraft_to_screen(
            width + HudStyle.PITCH_LABEL_OFFSET,
            mark_y,
            roll_deg,
            aircraft_pitch_px,
        )

        return LadderMark(
            centre_line=centre_line,
            left_cap=left_cap,
            right_cap=right_cap,
            left_label=left_label,
            right_label=right_label,
            label=str(abs(pitch)),
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

    def _aircraft_to_screen(
        self,
        x: float,
        y: float,
        roll_deg: float,
        aircraft_pitch_px: float,
    ) -> tuple[int, int]:
        """
        Convert a point from aircraft coordinates to screen coordinates.

        Aircraft coordinates:
            +X = right wing
            +Y = above the aircraft

        Screen coordinates:
            Origin at screen centre.
            +X = right
            +Y = down

        The point is rotated by the aircraft roll and translated by the
        current pitch before being converted to screen coordinates.
        """
        roll = math.radians(roll_deg)

        c = math.cos(roll)
        s = math.sin(roll)

        xr = x * c - y * s
        yr = x * s + y * c

        return (
            int(self.cx + xr),
            int(self.cy + aircraft_pitch_px - yr),
        ) 
    
    def _aircraft_line(
        self,
        x1: float,
        y1: float,
        x2: float,
        y2: float,
        roll_deg: float,
        aircraft_pitch_px: float,
        ) -> Line:
            p1 = self._aircraft_to_screen(x1, y1, roll_deg, aircraft_pitch_px)
            p2 = self._aircraft_to_screen(x2, y2, roll_deg, aircraft_pitch_px)
            return Line(p1, p2)
        
        
    def _rotation(self, roll_deg: float):

        roll = math.radians(roll_deg)
        # Convert from mathematical coordinates (Y increasing upwards)
        # to OpenCV image coordinates (Y increasing downwards).
        return (
            math.cos(roll),
            -math.sin(roll),
        )
    
    def _normal(self, dx: float, dy: float) -> tuple[float, float]:
        return -dy, dx
    