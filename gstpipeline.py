"""
GStreamer pipeline.

Camera -> OpenCV -> H264 -> MPEGTS -> SRT
"""

from __future__ import annotations
import time

#import cv2
import numpy as np

import gi
import queue

gi.require_version("Gst", "1.0")
gi.require_version("GLib", "2.0")

from gi.repository import Gst, GLib

from config import Config
from util import get_logger


Gst.init(None)


class GstPipeline:

    def __init__(self, config: Config):

        self.config = config

        self.logger = get_logger("pipeline", config.logging.level)

        self.frame_count = 0

        self.running = False

        self.logger.info("Creating GStreamer pipelines...")

        self.frame_duration = Gst.util_uint64_scale_int(
            1,
            Gst.SECOND,
            self.config.camera.fps,
        )

        self.timestamp = 0

        self.input_pipeline = Gst.Pipeline.new("raspi-hud")
        self._build_input_pipeline()
        self._connect_input_bus()

        self.output_pipeline = Gst.Pipeline.new("hud-output")    
        self._build_output_pipeline()
        self._connect_output_bus()

        self.frame_queue = queue.Queue(maxsize=1)

    def set_frame_callback(self, callback):

        self.frame_callback = callback


    def start(self):

        self.logger.info("Starting pipelines...")

        self.timestamp = 0

        self.input_pipeline.set_state(Gst.State.PLAYING)

        self.output_pipeline.set_state(Gst.State.PLAYING)

        self.running = True


    def stop(self):

        self.logger.info("Stopping pipelines...")

        self.running = False

        self.output_pipeline.set_state(Gst.State.NULL)
        self.input_pipeline.set_state(Gst.State.NULL)

    def get_frame(self):

        try:
            return self.frame_queue.get_nowait()
        except queue.Empty:
            return None
        
    def push_frame(self, frame):

        data = frame.tobytes()

        buffer = Gst.Buffer.new_allocate(
            None,
            len(data),
            None,
        )

        buffer.fill(0, data)

        buffer.pts = self.timestamp
        buffer.dts = self.timestamp
        buffer.duration = self.frame_duration

        self.timestamp += self.frame_duration

        self.appsrc.emit(
            "push-buffer",
            buffer,
        )    

    def _build_input_pipeline(self):

        width = self.config.camera.width
        height = self.config.camera.height
        fps = self.config.camera.fps

        pipeline = f"""
            libcamerasrc
            !
            video/x-raw,width={width},height={height},framerate={fps}/1
            !
            videoconvert
            !
            video/x-raw,format=BGR
            !
            appsink
                name=sink
                emit-signals=true
                sync=false
                drop=true
                max-buffers=1
        """

        self.logger.info("Input Pipeline:")

        self.logger.info(pipeline)

        self.input_pipeline = Gst.parse_launch(pipeline)

        self.appsink = self.input_pipeline.get_by_name("sink")

        self.appsink.connect(
            "new-sample",
            self._on_new_sample,
        )

    def _build_output_pipeline(self):
            """
            OpenCV renderer output.

            Receives rendered BGR frames from the application via appsrc.

            Initially terminates at autovideosink for latency testing.

            This sink will later become:

                appsrc
                -> encoder
                -> MPEG-TS
                -> SRT
            """
        
            width = self.config.camera.width
            height = self.config.camera.height
            fps = self.config.camera.fps

            self.logger.info("Building H.264 output pipeline")

            pipeline = f"""
                appsrc
                    name=source
                    is-live=true
                    do-timestamp=false
                    format=time
                    block=false
                    caps=video/x-raw,format=BGR,width={width},height={height},framerate={fps}/1
                !
                queue
                    max-size-buffers=1
                    leaky=downstream
                !
                videoconvert
                !
                video/x-raw,format=NV12
                !
                x264enc 
                    tune=zerolatency
                    speed-preset=ultrafast
                    bitrate=5000
                    key-int-max=30
                    rc-lookahead=0
                    byte-stream=true
                !
                mpegtsmux
                    alignment=7
                !
                srtsink
                    uri=srt://:9000
                    mode=listener
                    latency=50
                    wait-for-connection=true
            """
            self.logger.info("Output pipeline:")

            self.logger.info(pipeline)

            self.output_pipeline = Gst.parse_launch(pipeline)

            self.appsrc = self.output_pipeline.get_by_name("source")


    def _on_new_sample(self, sink):

        if not self.running:
            return Gst.FlowReturn.OK

        sample = sink.emit("pull-sample")

        if sample is None:
            return Gst.FlowReturn.ERROR

        buf = sample.get_buffer()

        caps = sample.get_caps()

        structure = caps.get_structure(0)

        width = structure.get_value("width")

        height = structure.get_value("height")
  
        ok, mapinfo = buf.map(Gst.MapFlags.READ)

        if not ok:
            return Gst.FlowReturn.ERROR

        try:

            frame = np.ndarray(
                (height, width, 3),
                dtype=np.uint8,
                buffer=mapinfo.data,
            ).copy()

            try:
                arrival = time.monotonic()

                self.frame_queue.put_nowait(
                    (frame, arrival)
                )

                #self.frame_queue.put_nowait(frame)
            except queue.Full:
            # Drop the oldest frame and replace it
                try:
                    self.frame_queue.get_nowait()              
                    #self.frame_queue.get_nowait()
                except queue.Empty:
                    pass
                # Replace it with the newest frame
                self.frame_queue.put_nowait(frame, arrival)

        finally:

            buf.unmap(mapinfo)

        return Gst.FlowReturn.OK
    
    def _connect_input_bus(self):

        bus = self.input_pipeline.get_bus()

        bus.add_signal_watch()

        bus.connect(
            "message",
            self._on_bus_message,
            "input",
        )

    def _connect_output_bus(self):

        bus = self.output_pipeline.get_bus()

        bus.add_signal_watch()

        bus.connect(
            "message",
            self._on_bus_message,
            "output",
        )

    def _on_bus_message(
        self,
        bus,
        message,
        name,
    ):

        t = message.type

        if t == Gst.MessageType.ERROR:

            err, dbg = message.parse_error()

            self.logger.error(
                f"{name}: {err}"
            )

            if dbg:

                self.logger.debug(
                    f"{name}: {dbg}"
                )

        elif t == Gst.MessageType.EOS:

            self.logger.info(
                    f"{name}: End of Stream"
                )
        

                           