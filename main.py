"""
raspi-hud

Application entry point.
"""

import faulthandler
import signal
import argparse

import logmanager
from performance import PerformanceMonitor, NullPerformance
from config import load_config
from gstpipeline import GstPipeline
from renderer import Renderer
from telemetrymanager import TelemetryManager
from mavlinksource import MavlinkSource


def main():

    faulthandler.register(signal.SIGUSR1)

    args = _parse_arguments()

    config = load_config()

    #### overide deaults here
    ###

    logmanager.initialise(config.logging.level)
    logger = logmanager.get_logger("application")

    if args.performance:
        perf = PerformanceMonitor(logger)
    else:
        perf = NullPerformance()


    pipeline = GstPipeline(config)
    renderer = Renderer()
    
    source = MavlinkSource(
        config.mavlink.connection,
        config.mavlink.baudrate,
    )

    telemetry = TelemetryManager(source)
    telemetry.start()
    logger.info("Telemetry started")

    pipeline.start()
    logger.info("Pipeline started")
    
    try:
        while True:

            frame = pipeline.get_frame()

            if frame is None:
                continue

            state = telemetry.get_state()

            with perf.timer("renderer.process"):
                frame = renderer.process(frame, state)

            with perf.timer("pipeline.push"):
                pipeline.push_frame(frame)

    except KeyboardInterrupt:
        logger.info("Interrupted")

    finally:
        telemetry.stop()
        pipeline.stop()
        
        logger.info("Stopped")

def _parse_arguments():
    parser = argparse.ArgumentParser(
        description="Raspberry Pi HUD",
    )

    parser.add_argument(
        "--performance",
        action="store_true",
        help="Enable performance monitoring",
    )

    return parser.parse_args()


if __name__ == "__main__":
    main()