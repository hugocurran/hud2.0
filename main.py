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
from telemetry import Telemetry

logger = get_logger(__name__)


def main():

    config = load_config()

    pipeline = GstPipeline(config)
    renderer = Renderer()
    telemetry = Telemetry()

    pipeline.start()

    logger.info("Pipeline started")
    
    #if config.mavlink.source == "simulator":
    #    telemetry = SimulatorSource()
    #
    #elif config.mavlink.source == "pymavlink":
    #    telemetry = MavlinkSource(
    #       config.mavlink.connection,
    #       config.mavlink.baudrate,
    #   )

    try:
        while True:

            frame = pipeline.get_frame()

            if frame is None:
                continue

            state = telemetry.get()

            frame = renderer.process(frame, state)

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