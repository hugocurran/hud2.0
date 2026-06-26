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