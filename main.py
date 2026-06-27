"""
raspi-hud

Application entry point.
"""

import signal
import sys
import cv2

from config import load_config
from gstpipeline import GstPipeline
from renderer import Renderer
from util import get_logger

logger = get_logger(__name__)


def main():

    config = load_config()

    pipeline = GstPipeline(config)
    renderer = Renderer()

    pipeline.start()

    logger.info("Pipeline started")

    try:
        while True:

            frame = pipeline.get_frame()

            if frame is None:
                continue

            frame = renderer.process(frame)

            cv2.imshow("raspi-hud", frame)

            key = cv2.waitKey(1)

            if key == 27:      # ESC
                break

    except KeyboardInterrupt:
        logger.info("Interrupted")

    finally:
        pipeline.stop()
        cv2.destroyAllWindows()
        logger.info("Stopped")


if __name__ == "__main__":
    main()