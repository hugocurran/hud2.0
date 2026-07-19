HUD Rendering
=============

Purpose
=======
As noted in Architecture the HUD system consists of three core elements: Video Pipelines, Telemetry and HUD Rendering. This document describes how Rendering works and the underlying components that make up the rendering system.

Scope
=====
This document is focused on the process of rendering a HUD image.

The collection of a current camera image and sending the modified (with HUD) image to a viewer is orchestrated by main.py and is outside the scope of this document.

Design Principles
=================
In pursuit of the overall philosophy outlined in Architecture this sub-system is designed to provide a clear separation between the different activities. The renderer is solely responsible for actually drawing the HUD onto the frame; hudgeometry is responsible for working out what information needs to be displayed and where; hudtransform provides the integration between the two by handling the translation between the aircraft coordinate system and that use by cv2/renderer.

Renderer has access to the Aircraft object, which contains the current aircraft state - updated by the telemetry sub-system. It passes this state to HudGeometry in its request for the drawing parameters for each object in the HUD (e.g. horizon line, pitch ladder). HudGeometry provides the drawing paramaters via HudTransform, which outputs 'screen' coordinates that are compatible with the cv2 model.

Renderer has a list of objects it needs to draw - this list can be extended (or reduced) without changing the underlying structure of Renderer (open-closed). Similarly, HudGeoetry knows how to draw a specific list of objects - this list can also be extended. HudTransform knows nothing of drawing, geometry or even HUDs: it simply converts a point from aircraft to screen coordinates; other artefacts are defined as points (e.g. a line consists of begin, centre and end points) and there are helper methods to handle multi-point constructs (e.g. line).

The purpose of HudTypes is simply to provide a common description of point, line and triangle. This could be extended to include polygons or similar in the future.

Current Implementation
======================
The components are:

    - Renderer class contained in renderer.py. This class is responsible for drawing the HUD on top of the current frame received from the camera (from the input pipeline). The class only deals with the actual drawing process, which consists of using OpenCV (cv2 library) to draw lines and text. It does know what objects need to be drawn, but relies on HudGeometry to define them. It passes the current aircraft state (Aircraft object) to HudGeometry. All geomtery calculations are performed by HudGeometry with the exception of the aircraft symbol in the screen centre, which is fixed and always drawn in the same place.

    - HudGeometry class contained in hudgeometry.py. This class takes information from the Aircraft state object and works out what needs drawing and where. It does not contain any drawing code - this is exclusively the domain of the Renderer class. HudGeometry works in 'aircraft' coordinates: These needs to be translated into screen (cv2) coordinates before the renderer can draw. There are numerous dataclasses defined in hudgeometry.py that define the contents of the HUD objects (e.g. PitchLadder, RollScale) and these classes are shared with Renderer.

    - HudTransform class contained in hudtransform.py. This class provides a common set of methods that convert the aircraft coordinates produced by HudGeometry into the cv2 coordinates consumed by Renderer. (Note that the main difference is that the y axis is reversed between the two coordinate systems).

    - HudTypes class contained in hudtypes.py. This is a helper class that contains common constructs used by both Renderer and HudGeometry - basically point, line and triangle.

    - HudStyle class contained in hudstyle.py. This class contains all of the constants used by the Hud Rendering system (primarily aimed at Renderer). As all of this information is contained in one place it is relatively simple to update e.g. the line colour. The data itself is contained within the HudStyle class as a set of constants. It could readily be moved to a separate YAML file to allow the user to define these things.

This sequence diagram illustrates the relationship between the three main components:
---
references:
  - "File: /hudgeometry.py"
generationTime: 2026-07-15T17:29:33.784Z
---
sequenceDiagram
    participant Caller
    participant HudGeometry
    participant HudTransform
    participant HudStyle

    Caller->>HudGeometry: horizon(roll_deg, pitch_deg)
    activate HudGeometry
    activate HudTransform
    HudGeometry->>HudStyle: read PITCH_SCALE and HORIZON_LENGTH
    HudGeometry->>HudTransform: aircraft_to_screen(0, 0, roll_deg, pitch_px)
    HudGeometry->>HudTransform: aircraft_to_screen(-L, 0, roll_deg, pitch_px)
    HudGeometry->>HudTransform: aircraft_to_screen(L, 0, roll_deg, pitch_px)
    HudGeometry-->>Caller: Horizon(line=Line(left,right), centre)

    Caller->>HudGeometry: ladder_mark(pitch, roll_deg, aircraft_pitch_px, major)
    HudGeometry->>HudStyle: compute mark_y, cap, label offsets
    alt major pitch mark
        HudGeometry->>HudStyle: use PITCH_MAJOR_WIDTH
    else minor pitch mark
        HudGeometry->>HudStyle: use PITCH_MINOR_WIDTH
    end
    HudGeometry->>HudTransform: aircraft_line(...) for centre_line
    HudGeometry->>HudTransform: aircraft_line(...) for left_cap
    HudGeometry->>HudTransform: aircraft_line(...) for right_cap
    HudGeometry->>HudTransform: aircraft_to_screen(...) for left_label
    HudGeometry->>HudTransform: aircraft_to_screen(...) for right_label
    HudGeometry-->>Caller: LadderMark(...)

    Caller->>HudGeometry: roll_scale(horizon, roll_deg)
    HudGeometry->>HudStyle: compute label_radius and tick lengths
    loop roll tick angles
        alt major tick
            HudGeometry->>HudStyle: use ROLL_MAJOR_TICK
        else minor tick
            HudGeometry->>HudStyle: use ROLL_MINOR_TICK
        end
        HudGeometry->>HudTransform: polar_point(origin, angle - roll_deg, ROLL_RADIUS)
        HudGeometry->>HudTransform: polar_point(origin, angle - roll_deg, ROLL_RADIUS - length)
        HudGeometry->>HudTransform: polar_point(origin, angle - roll_deg, label_radius)
    end
    HudGeometry->>HudTransform: polar_point(centre, 0, ROLL_RADIUS)
    HudGeometry->>HudTransform: polar_point(centre, -2, ROLL_RADIUS - 14)
    HudGeometry->>HudTransform: polar_point(centre, 2, ROLL_RADIUS - 14)
    HudGeometry-->>Caller: RollScale(marks, pointer)
    deactivate HudTransform
    deactivate HudGeometry

Future Enhancements
===================
OpenCV is a fast (i.e. low latency) mechanism for drawing onto a frame. However, it has two main drawbacks:
    - The graphics are somewhat crude and textual data is limited to a single font
    - There is no easy way to vary transparancy of the HUD. This may prove problematic if the video source has poor contrast (e.g. generated by a thermal camera or when the aircraft is operating in low light).

An alternative is Cairo, which has very good graphics and can readily (perhaps automatically) change the transparency of the HUD image. The main drawback to Cairo is that it is relatively slow in handling frames into and out of the video pipelines. In the future it is intended to explore a hybrid approach that would use cv2 for reading/writing frames and Cairo to do the actual drawing. This should be achievable without changing HudGeometry or the interfaces to main.py (which is responsible for collecting frames, pushing them to the renderer and extracting the result).

Related Documents
=================




