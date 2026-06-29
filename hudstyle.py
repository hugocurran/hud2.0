"""
HUD drawing style.
"""

import cv2


class HudStyle:

    # ------------------------------------------------------------
    # Colours
    # ------------------------------------------------------------

    COLOUR = (0, 255, 0)

    # ------------------------------------------------------------
    # Drawing
    # ------------------------------------------------------------

    LINE_WIDTH = 2

    FONT = cv2.FONT_HERSHEY_SIMPLEX
    FONT_SCALE = 0.6

    # ------------------------------------------------------------
    # Horizon
    # ------------------------------------------------------------

    PITCH_SCALE = 10.0          # pixels per degree
    HORIZON_LENGTH = 3000

    # ------------------------------------------------------------
    # Pitch ladder
    # ------------------------------------------------------------

    PITCH_MAJOR_WIDTH = 40
    PITCH_MINOR_WIDTH = 20

    LADDER_SPACING = 5

    PITCH_LABEL_OFFSET = 15
    PITCH_LABEL_FONT_SCALE = 0.5
    PITCH_LABEL_THICKNESS = 1
    PITCH_CAP_LENGTH = 8

    # ------------------------------------------------------------
    # Aircraft Symbol
    # ------------------------------------------------------------

    AIRCRAFT_GAP = 12
    AIRCRAFT_WING = 32
    AIRCRAFT_STEM = 14

    # ------------------------------------------------------------
    # Roll Scale
    # ------------------------------------------------------------

    ROLL_RADIUS = 220

    ROLL_MAJOR_TICK = 18
    ROLL_MINOR_TICK = 10

    ROLL_POINTER_SIZE = 14
    ROLL_POINTER_OFFSET = 8

    ROLL_LABEL_FONT_SCALE = 0.5
    ROLL_LABEL_THICKNESS = 1 
    ROLL_LABEL_OFFSET = 20

    # ------------------------------------------------------------
    # Status Overlay
    # ------------------------------------------------------------

    STATUS_X = 20
    STATUS_Y = 40
    STATUS_LINE_SPACING = 26