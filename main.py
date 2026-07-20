"""
raspi-hud

Application entry point.
"""

import faulthandler
import signal

from config import load_config
from gstpipeline import GstPipeline
from renderer import Renderer
from telemetrymanager import TelemetryManager
from logmanager import get_logger
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

            # frame = pipeline.get_frame()

            # if frame is None:
            #     continue

###
            item = pipeline.get_frame()

            if item is None:
                continue

            frame, arrival = item
###


            state = telemetry.get_state()
          
# ##
#             t0 = time.monotonic()
# ##

            frame = renderer.process(frame, state)
# ##
#             print(
#                 f"Render {(time.monotonic() -t0) * 1000:.1f} ms"
#             )
# ##

###
#            age_ms = (time.monotonic() - arrival) * 1000

#            print(f"Frame age before push = {age_ms:.1f} ms")
###
            pipeline.push_frame(frame)

    except KeyboardInterrupt:
        logger.info("Interrupted")

    finally:
        telemetry.stop()
        pipeline.stop()
        logger.info("Stopped")


if __name__ == "__main__":
    main()