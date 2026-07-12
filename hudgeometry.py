"""
HUD geometry calculations.

Contains no OpenCV drawing code.
"""

from __future__ import annotations

from dataclasses import dataclass

from hudstyle import HudStyle
from hudtypes import Point, Line, Triangle
from hudtransform import HudTransform

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

    pointer: Triangle

@dataclass
class RollMark:

    tick: Line

    label: Point

    angle: int

    major: bool

class HudGeometry:

    def __init__(self, width: int, height: int):

        self.transform = HudTransform(width, height)

        self.width = width
        self.height = height

        self.cx = width // 2
        self.cy = height // 2

        

    def horizon(self, roll_deg: float, pitch_deg: float,) -> Horizon:

            pitch_px = pitch_deg * HudStyle.PITCH_SCALE
            L = HudStyle.HORIZON_LENGTH

            centre = self.transform.aircraft_to_screen(
                0,
                0,
                roll_deg,
                pitch_px,
            )

            left = self.transform.aircraft_to_screen(
                -L,
                0,
                roll_deg,
                pitch_px,
            )

            right = self.transform.aircraft_to_screen(
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

        centre_line = self.transform.aircraft_line(
            -width,
            mark_y,
            width,
            mark_y,
            roll_deg,
            aircraft_pitch_px,
        )

        left_cap = self.transform.aircraft_line(
            -width,
            mark_y + cap,
            -width,
            mark_y - cap,
            roll_deg,
            aircraft_pitch_px,
        )

        right_cap = self.transform.aircraft_line(
            width,
            mark_y + cap,
            width,
            mark_y - cap,
            roll_deg,
            aircraft_pitch_px,
        )

        left_label = self.transform.aircraft_to_screen(
            -width - HudStyle.PITCH_LABEL_OFFSET,
            mark_y,
            roll_deg,
            aircraft_pitch_px,
        )

        right_label = self.transform.aircraft_to_screen(
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

            outer = self.transform.polar_point(
                origin,
                #angle,
               angle - roll_deg,
                HudStyle.ROLL_RADIUS,
            )

            inner = self.transform.polar_point(
                origin, 
                angle - roll_deg,
                #angle,
                HudStyle.ROLL_RADIUS - length,
            )

            label = self.transform.polar_point(
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
        
        # Roll_scale pointer (a triangle)
            
        centre = horizon.centre
        #radius = HudStyle.ROLL_RADIUS

        tip = self.transform.polar_point(
            centre,
            0,
            HudStyle.ROLL_RADIUS,
        )

        left = self.transform.polar_point(
            centre,
            -2,
            HudStyle.ROLL_RADIUS - 14,
        )

        right = self.transform.polar_point(
            centre,
            2,
            HudStyle.ROLL_RADIUS - 14,
        )

        triangle = Triangle(
            tip,
            left,
            right,
        )

        return RollScale(
            marks=marks,
            index=triangle,
        )
    
    # def roll_pointer(self):

    #     size = HudStyle.ROLL_POINTER_SIZE

    #     base_y = (
    #         self.cy
    #         - HudStyle.ROLL_RADIUS
    #         + HudStyle.ROLL_POINTER_OFFSET
    #     )

    #     tip = (
    #         self.cx,
    #         base_y,
    #     )

    #     left = (
    #         self.cx - size,
    #         base_y + size,
    #     )

    #     right = (
    #         self.cx + size,
    #         base_y + size,
    #     )

    #     return (
    #         tip,
    #         left,
    #         right,
    #     )
