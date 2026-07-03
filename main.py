"""
raspi-hud

Application entry point.
"""

import cv2
import faulthandler
import signal
import sys

from config import load_config
from gstpipeline import GstPipeline
from renderer import Renderer
from telemetrymanager import TelemetryManager
from util import get_logger
from mavlinksource import MavlinkSource


logger = get_logger(__name__)


def main():

    faulthandler.register(signal.SIGUSR1)

    config = load_config()

    pipeline = GstPipeline(config)
    renderer = Renderer()
    
    source = MavlinkSource(
        config.mavlink.connection,
        config.mavlink.baudrate,
    )

    telemetry = TelemetryManager(source)
    telemetry.start()
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
        telemetry.stop()
        pipeline.stop()
        cv2.destroyAllWindows()
        logger.info("Stopped")


if __name__ == "__main__":
    main()