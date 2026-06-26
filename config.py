"""
raspi-hud configuration
"""

from dataclasses import dataclass


VERSION = "0.1.0-dev"


@dataclass(frozen=True)
class CameraConfig:

    width: int = 1280
    height: int = 720
    fps: int = 30


@dataclass(frozen=True)
class StreamConfig:

    port: int = 9000

    bitrate: int = 2000

    keyframe_interval: int = 30


@dataclass(frozen=True)
class AppConfig:

    camera: CameraConfig = CameraConfig()

    stream: StreamConfig = StreamConfig()

    log_level: str = "INFO"


CONFIG = AppConfig()

