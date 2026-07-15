Logging Version 1.0 15/07/2026
==============================

Purpose
=======

The purpose of the logging system is to provide a single consistent location for creating log entries that is accessible from anywhere in the package. The objective is to create a traceable record of relevant events to verify correct operation of the system and allow diagnosis of problems/issues. The logging system supports different levels of information (warning, error, etc - see below) and this is largely intended to allow easy filtering of output.

Note that debugging using print() statements is useful to support debugging, this is not the same as logging which provides a centralised record. Conversely, vast quantities of low-level debugging output does not belong in a log and should be avoided.

Design Principles
=================

The key goals of the logging system are:
    - It should be consistent across all modules
    - It should have zero impact on performance
    - It should have configurable verbosity
    - It should be suitable for unattended aircraft operation
    - It should be available and useful for post-flight diagnosis

Log Levels
==========
Level	    Use
-----       ---
DEBUG	    Internal state and development diagnostics
INFO	    Normal application startup and shutdown
WARNING	    Recoverable issues
ERROR	    Failure of a subsystem
CRITICAL	Application cannot continue

Log levels follow the standard UNIX conventions - once a Log Level is set by the user (in config.yaml) the system will only record logs at that level or a higher level of criticality: Criticality levels are in the order shown above ordered from lowest to highest, with INFO being the default.

Logger Hierarchy
================
To facilitate easy searching/filtering each module is expected to tag its log entries with the module function (note that functions may span multiple modules). The hierarchy is:
hud

    application

    renderer

    hudgeometry

    telemetry

    camera

    gst

    network

    config

This is achieved by specifying the module function in the call to get_logger() - e.g. get_logger(renderer).

Output Destinations
===================
All logs are output to stdout.

Note that the HUD is managed as a systemd service - i.e. it is started and stopped by systemd(1) during system boot. The exact configuration of the service is defined in the file /lib/systemd/system/hud-generator.service - basically it is started after the mavproxy.service is stable. So far as logging is concerned, systemd will forward all output (stdout, stderr) to the operating system log, where it can be accessed using journalctl(1).

Coding Standards
================
Access to the logging system is initialised by each module calling the function get_logger() (located in utils.py) and specifying the module function - e.g. get_logger(renderer). This provides the module with a reference to the logging system.

General rules:
    - Log significant events, not every function call
    - Log context rather than stack traces where possible
    - Never log inside high-frequency rendering loops unless DEBUG is enabled (in config.logging) 

Future Enhancements
===================

None planned

Related Documents
=================

See BZ25-Setup documentation


