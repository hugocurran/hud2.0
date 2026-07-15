Purpose
=======

The objective of HUD 2.0 is to create a flexible framework for generating a Heads-Up Display (HUD) on the aircraft that is overlaid onto the the current camera output, before transmitting to a ground station via a video streaming protocol. The advantage of this approach, compared to the traditional approach of creating a HUD on a ground station, is that the information is always 'fresh' and there is no possibility of drift between the video feed and telemetry feed.

Scope
=====

HUD 2.0 is a single Python3 package that has a number of external dependancies (which are installed via a setup.sh script). It is capable of direct interaction with a flight controller that generates MAVLink 2 messages, however is is normally connected to the flight controller via mavproxy. The configuration of the flight controller and mavproxy are outside the project scope. 

Design Principles
=================

HUD 2.0 makes full use of Python3 (version 3.13) to create a coherent model that follows classical Object Oriented Programming (OOP) principles. Classes have a single responsibility, ownership of data is strictly managed and types are enforced.

Current Implementation
======================

The code is divided into several modules:

- main.py
  - orchestrates startup
  - creates `GstPipeline`, `Renderer`, `TelemetryManager`, `MavlinkSource`

- config.py
  - defines `Config` and nested config dataclasses

- gstpipeline.py
  - camera input + output pipeline
  - manages frames and GStreamer appsrc/appsink

- renderer.py
  - draws HUD overlays using `HudGeometry` and `HudStyle`

- telemetrymanager.py
  - owns aircraft state and refresh loop
  - delegates updates to `TelemetrySource`

- telemetrysource.py
  - abstract telemetry provider interface
  - implemented by mavlinksource.py and simulatorsource.py

- hudgeometry.py
  - generates HUD geometry data from aircraft attitude

- hudtransform.py
  - converts aircraft-space coordinates into screen-space

- hudtypes.py
  - basic primitive types: `Point`, `Line`, `Triangle`

Future Enhancements
===================
1. Expand the model to allow the user (via config.yaml) to specify the platform in use
    - Allow platform-specific requirements to be managed in one place
    - Move the system from a Raspi-focused implementation to a more generic basis that supports other platforms
    - Support a more varied list of cameras

2. Allow the use of alternative libraries for interaction with MAVLink. Currently the system is tied to pymavlink, but in the future MAVROS may be used.

3. Integrate the use of a simulated camera to support the use of HUD 2.0 as a training aid.

Related Documents
=================

```mermaid
classDiagram
    class Main {
    }
    class Config {
    }
    class CameraConfig {
    }
    class DisplayConfig {
    }
    class LoggingConfig {
    }
    class MavlinkConfig {
    }
    class GstPipeline {
    }
    class Renderer {
    }
    class TelemetryManager {
    }
    class TelemetrySource {
    }
    class MavlinkSource {
    }
    class SimulatorSource {
    }
    class HudGeometry {
    }
    class HudTransform {
    }
    class HudStyle {
    }
    class Point {
    }
    class Line {
    }
    class Triangle {
    }
    class AircraftState {
    }

    Main --> GstPipeline : uses
    Main --> Renderer : uses
    Main --> TelemetryManager : uses
    Main --> MavlinkSource : uses
    Main --> Config : loads

    Config o-- CameraConfig
    Config o-- DisplayConfig
    Config o-- LoggingConfig
    Config o-- MavlinkConfig

    GstPipeline --> Config : config

    Renderer --> HudGeometry : owns
    Renderer --> HudStyle : uses
    Renderer --> AircraftState : draws from

    HudGeometry --> HudTransform : uses
    HudGeometry --> HudStyle : uses
    HudGeometry --> Point : creates
    HudGeometry --> Line : creates
    HudGeometry --> Triangle : creates

    HudTransform --> Point : returns
    HudTransform --> Line : returns
    HudTransform --> Triangle : returns

    TelemetryManager --> TelemetrySource : depends
    TelemetryManager --> AircraftState : owns state

    TelemetrySource <|-- MavlinkSource
    TelemetrySource <|-- SimulatorSource

    MavlinkSource --> AircraftState : updates
    SimulatorSource --> AircraftState : updates
```
