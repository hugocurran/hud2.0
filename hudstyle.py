"""
HUD drawing style.
"""

import cv2


class HudStyle:

    COLOUR = (0, 255, 0)

    LINE_WIDTH = 2

    FONT = cv2.FONT_HERSHEY_SIMPLEX

    FONT_SCALE = 0.6

    PITCH_SCALE = 10.0      # pixels per degree

    HORIZON_LENGTH = 3000

    LADDER_HALF_WIDTH = 40

    LADDER_SPACING = 5       # degrees