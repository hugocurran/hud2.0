"""
Configuration management for raspi-hud.
"""

from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path

import yaml

VERSION = "0.2.0-dev"


# ----------------------------------------------------------------------
# Camera
# ----------------------------------------------------------------------

@dataclass(frozen=True)
class CameraConfig:
    width: int
    height: int
    fps: int


# ----------------------------------------------------------------------
# Streaming
# ----------------------------------------------------------------------

@dataclass(frozen=True)
class StreamConfig:
    host: str
    port: int
    bitrate: int
    keyframe_interval: int
    latency: int


# ----------------------------------------------------------------------
# MAVLink
# ----------------------------------------------------------------------

@dataclass(frozen=True)
class MavlinkConfig:
    connection: str


# ----------------------------------------------------------------------
# Logging
# ----------------------------------------------------------------------

@dataclass(frozen=True)
class LoggingConfig:
    level: str


# ----------------------------------------------------------------------
# Root configuration
# ----------------------------------------------------------------------

@dataclass(frozen=True)
class AppConfig:
    camera: CameraConfig
    stream: StreamConfig
    mavlink: MavlinkConfig
    logging: LoggingConfig


# ----------------------------------------------------------------------
# Loader
# ----------------------------------------------------------------------

def load_config(filename: str = "config.yaml") -> AppConfig:
    """
    Load application configuration from YAML.
    """

    path = Path(filename)

    if not path.exists():
        raise FileNotFoundError(path)

    with path.open("r", encoding="utf-8") as f:
        data = yaml.safe_load(f)

    return AppConfig(
        camera=CameraConfig(**data["camera"]),
        stream=StreamConfig(**data["stream"]),
        mavlink=MavlinkConfig(**data["mavlink"]),
        logging=LoggingConfig(**data["logging"]),
    )
