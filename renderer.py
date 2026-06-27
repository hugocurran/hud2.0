"""
Renderer.

Currently this is a pass-through renderer.
HUD drawing will be added later.
"""

from __future__ import annotations

import cv2
import numpy as np


class Renderer:

    def __init__(self):

        self.frame_counter = 0

    def process(self, frame: np.ndarray) -> np.ndarray:

        self.frame_counter += 1

        #
        # Temporary debugging overlay
        #

        cv2.putText(
            frame,
            f"Frame {self.frame_counter}",
            (20, 40),
            cv2.FONT_HERSHEY_SIMPLEX,
            1.0,
            (0, 255, 0),
            2,
            cv2.LINE_AA,
        )

        return frame