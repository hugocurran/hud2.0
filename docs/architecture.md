libcamerasrc
      │
      ▼
 appsink  ---> OpenCV callback ---> appsrc
                                 │
                                 ▼
                             x264enc
                                 │
                                 ▼
                              MPEG-TS
                                 │
                                 ▼
                          SRT listener



main.py
      │
      ▼
Application
      │
      ▼
Pipeline Manager
      │
      ├── Camera
      ├── Encoder
      ├── Network
      └── Telemetry
             │
             ▼
         HUD Renderer                   

                   main.py
                     │
     +---------------+---------------+
     |                               |
     |                               |
 Renderer                    GstPipeline
     |                               |
     |                       appsink callback
     |                               |
     |                       Queue(maxsize=1)
     |                               |
     +---------- get_frame() <--------+           



Version 0.2

raspi-hud/
│
├── main.py
├── config.py
├── config.yaml
├── gstpipeline.py
├── renderer.py
├── utils.py
├── requirements.txt
│
├── telemetry.py      # placeholder
├── hud.py            # placeholder
├── streamer.py       # placeholder
│
└── README.md

Responsibilities

main.py

Owns the application
Starts/stops components
Main processing loop
Keyboard handling

gstpipeline.py

Camera capture only
libcamerasrc
appsink
Queue latest frame
No GUI
No HUD
No streaming

renderer.py

Draws on frames
Initially just a frame counter
Later: artificial horizon, altitude, battery, compass, etc.

config.py

Reads YAML
Returns a strongly typed configuration object

HUD Design

          World

            ^
            |
------------+------------ Horizon
            |
            |

             |
             | rotate (roll)
             |
             V

        Screen Space

        +----------------------+
        |                      |
        |         +            |
        |                      |
        +----------------------+




                            Main Thread
                    ===========
Camera --> GstPipeline --> Renderer
                           ▲
                           │
                    get_state()
                           │
                    TelemetryManager
                     (owns state)
                           ▲
                           │ Lock
                           ▼
                 Telemetry Worker Thread
                           │
                    update_state()
                           │
                    MavlinkSource
                           │
                       Pixhawk




"stuff built on an angle uses polar coordinates, stuff that is basically straight lines uses cartesian."

Aircraft geometry

Cartesian
----------
Point
Line

Polar
-----
Arc point
Arc line (perhaps)
                       



HUD Architecture
================

The HUD consists of two independent visual frames.

Static Frame

The static frame is fixed relative to the display.

It contains:

aircraft symbol
wings
roll pointer

These never move.

Attitude Frame

The attitude frame represents the outside world.

It contains:

horizon
pitch ladder
roll scale

These elements are rigidly related and move as a single geometric object.

Aircraft roll rotates the entire frame.

Aircraft pitch translates the entire frame vertically.

The renderer is responsible only for clipping and presentation. The geometry of the attitude frame is calculated by HudGeometry.
                 HUD

          +----------------+

          Static Frame

          ▲
     -----+-----
          |

============================   Horizon
  10                 10
============================   Pitch Ladder

      Roll Scale Arc

          Attitude Frame

          +----------------+
