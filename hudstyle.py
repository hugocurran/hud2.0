"""
HUD drawing style.
"""

import cv2


class HudStyle:

    # Colours
    COLOUR = (0, 255, 0)

    # Lines
    LINE_WIDTH = 2

    # Font
    FONT = cv2.FONT_HERSHEY_SIMPLEX
    FONT_SCALE = 0.6

    # Geometry
    PITCH_SCALE = 10.0          # pixels/degree

    HORIZON_LENGTH = 3000

    PITCH_MAJOR_WIDTH = 60
    PITCH_MINOR_WIDTH = 35

    LADDER_HALF_WIDTH = 40

    LADDER_SPACING = 5       # degrees