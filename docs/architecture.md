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