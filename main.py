"""
raspi-hud

Application entry point.
"""

from config import AppConfig, VERSION
from gstpipeline import GstPipeline
from util import get_logger
from config import load_config

def main() -> int:

    config = load_config()

    logger = get_logger("raspi-hud", config.logging.level)

    logger.info("raspi-hud %s", VERSION)

    pipeline = GstPipeline(config)

    pipeline.start()

    pipeline.run()

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
