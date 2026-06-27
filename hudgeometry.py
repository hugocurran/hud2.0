"""
hudgeometry.py

Geometry helper functions for the Raspberry Pi HUD.

These functions perform coordinate transforms and generate HUD geometry.
They do not perform any drawing.
"""

import math


# ----------------------------------------------------------------------
# Basic geometry
# ----------------------------------------------------------------------

def rotate_point(x, y, angle_deg):
    """
    Rotate a point around the origin.

    Parameters
    ----------
    x, y : float
        Point coordinates.

    angle_deg : float
        Rotation angle in degrees.
        Positive = clockwise (screen coordinates).

    Returns
    -------
    (xr, yr)
    """

    angle = math.radians(angle_deg)

    c = math.cos(angle)
    s = math.sin(angle)

    xr = x * c + y * s
    yr = -x * s + y * c

    return xr, yr


def translate_point(x, y, dx, dy):
    """
    Translate a point.
    """
    return x + dx, y + dy


def rotate_translate_point(x, y, angle_deg, dx, dy):
    """
    Rotate around origin then translate.
    """
    xr, yr = rotate_point(x, y, angle_deg)
    return xr + dx, yr + dy


# ----------------------------------------------------------------------
# HUD helpers
# ----------------------------------------------------------------------

def pitch_to_pixels(pitch_deg, pixels_per_degree):
    """
    Convert pitch angle into screen offset.
    Positive pitch moves the horizon downward.
    """
    return pitch_deg * pixels_per_degree


def horizon_endpoints(width, cx, cy, roll_deg, horizon_length):
    """
    Generate horizon line endpoints.

    Returns:
        (x1, y1), (x2, y2)
    """

    half = horizon_length / 2

    left = (-half, 0)
    right = (half, 0)

    x1, y1 = rotate_translate_point(
        left[0],
        left[1],
        roll_deg,
        cx,
        cy,
    )

    x2, y2 = rotate_translate_point(
        right[0],
        right[1],
        roll_deg,
        cx,
        cy,
    )

    return (
        int(x1),
        int(y1),
    ), (
        int(x2),
        int(y2),
    )


# ----------------------------------------------------------------------
# Pitch ladder
# ----------------------------------------------------------------------

def pitch_mark(
    pitch_deg,
    aircraft_pitch_deg,
    pixels_per_degree,
):
    """
    Calculate vertical offset of one pitch mark.

    Returns pixel offset relative to screen centre.
    """

    return (
        pitch_deg - aircraft_pitch_deg
    ) * pixels_per_degree


# ----------------------------------------------------------------------
# Roll scale
# ----------------------------------------------------------------------

def polar_to_cartesian(radius, angle_deg):
    """
    Convert polar coordinates into screen coordinates.

    0° = up
    Positive clockwise.
    """

    angle = math.radians(angle_deg)

    x = radius * math.sin(angle)
    y = -radius * math.cos(angle)

    return x, y


def roll_tick(cx, cy, radius, angle_deg, tick_length):
    """
    Generate one roll tick.

    Returns:
        ((x1,y1), (x2,y2))
    """

    ox, oy = polar_to_cartesian(radius, angle_deg)
    ix, iy = polar_to_cartesian(radius - tick_length, angle_deg)

    return (
        int(cx + ox),
        int(cy + oy),
    ), (
        int(cx + ix),
        int(cy + iy),
    )


def roll_pointer(cx, cy, radius, height):
    """
    Fixed triangle pointer at top of roll scale.

           ▲
    """

    top = (
        cx,
        cy - radius - height,
    )

    left = (
        cx - height,
        cy - radius,
    )

    right = (
        cx + height,
        cy - radius,
    )

    return top, left, right


# ----------------------------------------------------------------------
# Utility
# ----------------------------------------------------------------------

def screen_center(width, height):
    """
    Return integer screen centre.
    """

    return width // 2, height // 2