"""
Configuration loading.

Loads config.yaml into strongly typed dataclasses.
"""

from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path

import yaml


# ---------------------------------------------------------------------
# Camera
# ---------------------------------------------------------------------


@dataclass(slots=True)
class CameraConfig:
    width: int
    height: int
    fps: int


# ---------------------------------------------------------------------
# Display
# ---------------------------------------------------------------------


@dataclass(slots=True)
class DisplayConfig:
    enabled: bool
    window_name: str


# ---------------------------------------------------------------------
# Logging
# ---------------------------------------------------------------------


@dataclass(slots=True)
class LoggingConfig:
    level: str


# ---------------------------------------------------------------------
# Root configuration
# ---------------------------------------------------------------------


@dataclass(slots=True)
class Config:
    camera: CameraConfig
    display: DisplayConfig
    logging: LoggingConfig
    mavlink: MavlinkConfig


@dataclass(slots=True)
class MavlinkConfig:
    connection: str
    baudrate: int
    source: str

# ---------------------------------------------------------------------
# Loader
# ---------------------------------------------------------------------


def load_config(filename: str = "config.yaml") -> Config:

    path = Path(filename)

    with path.open("r") as f:
        data = yaml.safe_load(f)

    return Config(
        camera=CameraConfig(**data["camera"]),
        display=DisplayConfig(**data["display"]),
        logging=LoggingConfig(**data["logging"]),
        mavlink=MavlinkConfig(**data["mavlink"]),
    )
