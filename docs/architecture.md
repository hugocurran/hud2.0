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

                       