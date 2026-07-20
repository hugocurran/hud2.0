# Logging Version 1.0 15/07/2026

## Purpose

The purpose of the logging system is to provide a single consistent logging interface for creating log entries that is accessible from anywhere in the packapplication. The objective is to create a traceable record of relevant events to verify correct operation of the system and allow diagnosis of problems/issues. The logging system supports different levels of information (warning, error, etc - see below) and this is largely intended to allow easy filtering of output.

Note that print() statements are a temporary debugging aid and should normally be removed before code is committed. Logging provides the permanent diagnostic record of system operation. Conversely, vast quantities of low-level debugging output does not belong in a log and should be avoided.

## Design Principles

The key goals of the logging system are:

    - It should be consistent across all modules

    - It should have negligible impact on performance

    - It should have configurable verbosity

    - It should be suitable for unattended aircraft operation

    - It should be available and useful for post-flight diagnosis

### Log Levels

Level	    Use
-----       ---
DEBUG	    Internal state and development diagnostics
INFO	    Normal application startup and shutdown
WARNING	    Recoverable issues
ERROR	    Failure of a subsystem
CRITICAL	Application cannot continue

Log levels follow the standard UNIX conventions - once a Log Level is set by the user (in config.yaml) the system will only record logs at that level or a higher level of criticality: Criticality levels are in the order shown above ordered from lowest to highest, with INFO being the default.

### Logger Hierarchy

The logging system uses a hierarchical namespace to organise log messages by subsystem. The root logger (hud) represents the application as a whole, while child loggers represent the major functional subsystems (for example hud.render, hud.video and hud.telemetry).

Child loggers inherit the configuration of their parent logger, allowing the application to configure logging behaviour once while retaining the ability to identify and filter messages by subsystem. This approach follows the standard Python logging model and provides a scalable architecture as additional subsystems are added.

Each subsystem shall obtain a logger corresponding to its functional role. This hierarchy facilitates filtering and searching of log output. The hierarchy is:

hud
    hud.application
    hud.video
    hud.render
    hud.telemetry
    hud.network
    hud.config
    hud.system

This is achieved by specifying the module function in the call to get_logger() - e.g. get_logger("render").

### Log Entry Format

Every log entry shall contain:

    - Timestamp

    - Severity

    - Subsystem

    - Message


## Current Implementation

Each module obtains a logger by calling the helper function get_logger() in utils.py. The helper constructs the fully-qualified logger name (for example hud.render) and returns the corresponding Python Logger object.

By centralising logger creation within a helper function, the remainder of the application is isolated from the implementation details of the logging framework and the root logger namespace.

All logs are output to stdout.

Note that the HUD is managed as a systemd service - i.e. it is started and stopped by systemd(1) during system boot. The exact configuration of the service is defined in the file /lib/systemd/system/hud-generator.service - basically it is started after the mavproxy.service is stable. So far as logging is concerned, systemd will forward all output (stdout, stderr) to the operating system log, where it can be accessed using journalctl(1).

### Coding Standards

Access to the logging system is initialised by each module calling the function get_logger() (located in utils.py) and specifying the module function - e.g. get_logger("hud.renderer"). This provides the module with a reference to the logging system.

General rules:

    - Log significant events, not every function call

    - Log context rather than stack traces where possible

    - Never log inside high-frequency rendering loops unless DEBUG is enabled (in config.logging)

    - Avoid logging the same condition repeatedly

    - Log the cause of an event rather than simply its consequence. (E.g. 'Configuration file 'config.yaml' not found; using defaults.' rather than 'Configuration failed.')

### Message Style

Provide context to the message following the general style <thing> <state/status>. E.g. 'Camera initialised' rather than 'Got Camera', or 'Video output stream started' rather than 'Video running'. If messages follow the same style the logs are easier to read.

## Future Enhancements

Potential future enhancements include:

    - Session identifiers
    
    - Rotating log files

    - Flight log correlation

    - Remote logging

    - Structured (JSON) logging

## Related Documents

See BZ25-Setup documentation


