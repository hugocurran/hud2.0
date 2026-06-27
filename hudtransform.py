"""
HUD coordinate transforms.
"""

from __future__ import annotations

import math


class HudTransform:

    def __init__(self, width: int, height: int):

        self.width = width
        self.height = height

        self.cx = width / 2
        self.cy = height / 2

        # pixels per degree of pitch
        self.pitch_scale = 10.0

    def horizon(self, roll_deg: float, pitch_deg: float):

        roll = math.radians(roll_deg)

        dx = math.cos(roll)
        dy = math.sin(roll)

        # unit normal

        nx = -dy
        ny = dx

        offset = pitch_deg * self.pitch_scale

        cx = self.cx + nx * offset
        cy = self.cy + ny * offset

        length = max(self.width, self.height) * 2

        x1 = int(cx - dx * length)
        y1 = int(cy - dy * length)

        x2 = int(cx + dx * length)
        y2 = int(cy + dy * length)

        return (x1, y1), (x2, y2)
    