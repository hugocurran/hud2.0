"""
HUD coordinate transforms.
"""

from __future__ import annotations

import math

from hudtypes import Point, Line, Triangle

class HudTransform:

    def __init__(self, width: int, height: int):

        self.width = width
        self.height = height

        self.cx = width / 2
        self.cy = height / 2

        # pixels per degree of pitch
        self.pitch_scale = 10.0

    def aircraft_to_screen(
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
    
    def aircraft_line(
        self,
        x1: float,
        y1: float,
        x2: float,
        y2: float,
        roll_deg: float,
        aircraft_pitch_px: float,
        ) -> Line:
            p1 = self.aircraft_to_screen(x1, y1, roll_deg, aircraft_pitch_px)
            p2 = self.aircraft_to_screen(x2, y2, roll_deg, aircraft_pitch_px)
            return Line(p1, p2)
    
    def polar_point(
        self,
        origin: Point,
        angle_deg: float,
        radius: float,
    ) -> Point:   
        
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
    
    def rotation(self, roll_deg: float):

        roll = math.radians(roll_deg)
        # Convert from mathematical coordinates (Y increasing upwards)
        # to OpenCV image coordinates (Y increasing downwards).
        return (
            math.cos(roll),
            -math.sin(roll),
        )
    
    def normal(self, dx: float, dy: float) -> tuple[float, float]:
        return -dy, dx
    











    # def horizon(self, roll_deg: float, pitch_deg: float):

    #     roll = math.radians(roll_deg)

    #     dx = math.cos(roll)
    #     dy = math.sin(roll)

    #     # unit normal

    #     nx = -dy
    #     ny = dx

    #     offset = pitch_deg * self.pitch_scale

    #     cx = self.cx + nx * offset
    #     cy = self.cy + ny * offset

    #     length = max(self.width, self.height) * 2

    #     x1 = int(cx - dx * length)
    #     y1 = int(cy - dy * length)

    #     x2 = int(cx + dx * length)
    #     y2 = int(cy + dy * length)

    #     return (x1, y1), (x2, y2)
    