"""
raspi-hud

Application entry point.
"""

from config import CONFIG, VERSION
from util import get_logger


def main() -> int:
    """Application entry point."""

    logger = get_logger("raspi-hud", CONFIG.log_level)

    logger.info("----------------------------------------")
    logger.info("raspi-hud %s", VERSION)
    logger.info("Initialising...")
    logger.info("Camera : %dx%d @ %d FPS",
                CONFIG.camera.width,
                CONFIG.camera.height,
                CONFIG.camera.fps)
    logger.info("SRT Port : %d", CONFIG.stream.port)
    logger.info("Ready.")
    logger.info("----------------------------------------")

    return 0


if __name__ == "__main__":
    raise SystemExit(main())