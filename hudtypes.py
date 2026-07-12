""" Declaration of primitive types used in HudTransform and HudGeometry
"""

from dataclasses import dataclass

@dataclass(frozen=True)
class Point:
    # A point on the screen
    x: int
    y: int

@dataclass(frozen=True)
class Line:
    # A line on the screen
    start: Point
    end: Point

@dataclass(frozen=True)
class Triangle:
    a: Point
    b: Point
    c: Point