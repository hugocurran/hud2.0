"""
raspi-hud

Application entry point.
"""

import signal
import sys
import cv2
import time

from config import load_config
from gstpipeline import GstPipeline
from renderer import Renderer
from util import get_logger
from telemetry import Telemetry
from simulatorsource import SimulatorSource
from mavlinksource import MavlinkSource


logger = get_logger(__name__)


def main():

    config = load_config()

    pipeline = GstPipeline(config)
    renderer = Renderer()
    telemetry = MavlinkSource(
        config.mavlink.connection,
        config.mavlink.baudrate,
    )

    pipeline.start()

    logger.info("Pipeline started")
    
    try:
        while True:

            frame = pipeline.get_frame()

            if frame is None:
                continue

            state = telemetry.get_state()
          
            frame = renderer.process(frame, state)

            cv2.imshow("raspi-hud", frame)
            
            if cv2.waitKey(1) == 27:      # ESC
                break

    except KeyboardInterrupt:
        logger.info("Interrupted")

    finally:
        pipeline.stop()
        cv2.destroyAllWindows()
        logger.info("Stopped")


if __name__ == "__main__":
    main()