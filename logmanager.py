"""
Application logging manager.

This module provides centralised configuration of the Python logging
framework together with helper functions for obtaining subsystem loggers.

Logging is configured once during application start-up and all subsystem
loggers inherit the root configuration.
"""

import logging
import sys

LOGGER_ROOT = "hud"
LOG_FORMAT = "%(asctime)s %(levelname)-8s %(name)-20s %(message)s"

_initialised = False

def initialise(level: str) -> None:
    """Initialise the HUD logging system."""

    global _initialised
   
    if _initialised:
        return
    
    root = logging.getLogger(LOGGER_ROOT)

    # Quick sanity check to make sure logger level is recognised
    loglevel = getattr(logging, level.upper(), None)
    if not isinstance(loglevel, int):
        raise ValueError(loglevel)

    root.setLevel(loglevel)

    root.propagate = False

    formatter = logging.Formatter(LOG_FORMAT)

    handler = logging.StreamHandler(sys.stdout)

    handler.setFormatter(formatter)

    root.addHandler(handler)

    _initialised = True


def get_logger(subsystem: str) -> logging.Logger:
    """Return a logger for a HUD subsystem."""
   
    return logging.getLogger(f"{LOGGER_ROOT}.{subsystem}")




# def get_logger(name: str, level: str = "INFO") -> logging.Logger:

#     logger = logging.getLogger(name)

#     if logger.handlers:
#         return logger

#     logger.setLevel(level)

#     formatter = logging.Formatter(
#         "%(asctime)s %(levelname)-8s %(message)s"
#     )

#     handler = logging.StreamHandler(sys.stdout)

#     handler.setFormatter(formatter)

#     logger.addHandler(handler)

#     return logger

