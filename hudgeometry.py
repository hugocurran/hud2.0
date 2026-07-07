"""
HUD geometry calculations.

Contains no OpenCV drawing code.
"""

from __future__ import annotations

from dataclasses import dataclass
import math

from hudstyle import HudStyle

""" A point on the screen """
@dataclass(frozen=True)
class Point:
    x: int
    y: int

""" A line segment on the screen """
@dataclass
class Line:
    start: Point
    end: Point


@dataclass
class Horizon:

    line: Line

    centre: Point

@dataclass
class LadderMark:
    """
    Geometry for a single pitch ladder mark.

    All coordinates are already transformed into screen coordinates.
    """

    centre_line: Line | None

    left_cap: Line | None

    right_cap: Line | None

    left_label: Point | None = None

    right_label: Point | None = None

    label: str | None = None

@dataclass
class AttitudeFrame:

    horizon: Line

    ladder: list[LadderMark]

    roll_scale: RollScale


@dataclass
class RollScale:

    marks: list[RollMark]

@dataclass
class RollMark:

    tick: Line

    label: Point

    angle: int

    major: bool

class HudGeometry:

    def __init__(self, width: int, height: int):

        self.width = width
        self.height = height

        self.cx = width // 2
        self.cy = height // 2

    def horizon(self, roll_deg: float, pitch_deg: float,) -> Horizon:

            pitch_px = pitch_deg * HudStyle.PITCH_SCALE
            L = HudStyle.HORIZON_LENGTH

            centre = self._aircraft_to_screen(
                0,
                0,
                roll_deg,
                pitch_px,
            )

            left = self._aircraft_to_screen(
                -L,
                0,
                roll_deg,
                pitch_px,
            )

            right = self._aircraft_to_screen(
                L,
                0,
                roll_deg,
                pitch_px,
            )

            return Horizon(
                line=Line(left, right),
                centre=centre,
            )

    
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
    
    def roll_scale(
        self,
        horizon: Horizon,
        roll_deg: float,
    ) -> RollScale:

        origin = horizon.centre

        marks = []

        label_radius = (
            HudStyle.ROLL_RADIUS
            + HudStyle.ROLL_LABEL_OFFSET
        )

        for angle in (-60, -45, -30, -20, -10, 10, 20, 30, 45, 60):

            major = angle in (-60, -30, 30, 60)

            length = (
                HudStyle.ROLL_MAJOR_TICK
                if major
                else HudStyle.ROLL_MINOR_TICK
            )

            outer = self._polar_point(
                origin,
                #angle,
               angle - roll_deg,
                HudStyle.ROLL_RADIUS,
            )

            inner = self._polar_point(
                origin, 
                angle - roll_deg,
                #angle,
                HudStyle.ROLL_RADIUS - length,
            )

            label = self._polar_point(
                origin,
                angle - roll_deg,
                #angle,
                label_radius,
            )

            tick = Line(
                outer,
                inner,  
            )

            marks.append(
                RollMark(
                    tick = tick,
                    label = label,
                    angle = angle,
                    major = major,
            )
        )

        return RollScale(
            marks=marks,
        )
    
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
    ) -> Point:
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

        return Point(
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

    def _polar_point(
        self,
        origin: Point,
        angle_deg: float,
        radius: float,
    ) -> Point:   
        
        #angle = math.radians(angle_deg)
        angle = math.radians(angle_deg)

        sx = math.sin(angle)
        cy = math.cos(angle)

        # return Point(
        #     int(self.cx + sx * radius),
        #     int(self.cy - cy * radius),
        # )
        return Point (
              int(origin.x + sx * radius),
              int(origin.y - cy * radius)   ,
        )
        
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
    