"""
GStreamer pipeline.

Camera -> OpenCV -> H264 -> MPEGTS -> SRT
"""

from __future__ import annotations

import cv2
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

        self.pipeline = Gst.Pipeline.new("raspi-hud")

        self.frame_count = 0

        self.running = False

        self.logger.info("Creating GStreamer pipeline...")

        self._build_pipeline()

        self._connect_bus()

        self.frame_queue = queue.Queue(maxsize=1)

    def set_frame_callback(self, callback):

        self.frame_callback = callback


    def start(self):

        self.logger.info("Starting pipeline...")

        self.pipeline.set_state(Gst.State.PLAYING)

        self.running = True


    def stop(self):

        self.logger.info("Stopping pipeline...")

        self.running = False



        print("before null")
        state_change, current, pending = self.pipeline.get_state(0)

        print(
            f"Current={current.value_nick} "
            f"Pending={pending.value_nick}"
        )
        self.pipeline.set_state(Gst.State.NULL)
        print("after null")
        cv2.destroyAllWindows()


    def get_frame(self):

        try:
            return self.frame_queue.get_nowait()
        except queue.Empty:
            return None

    def _build_pipeline(self):

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

        self.logger.info("Pipeline:")

        self.logger.info(pipeline)

        self.pipeline = Gst.parse_launch(pipeline)

        self.appsink = self.pipeline.get_by_name("sink")

        self.appsink.connect(
            "new-sample",
            self._on_new_sample,
        )

    def _on_new_sample(self, sink):

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
                self.frame_queue.put_nowait(frame)
            except queue.Full:
            # Drop the oldest frame and replace it
                try:
                    self.frame_queue.get_nowait()
                except queue.Empty:
                    pass

                self.frame_queue.put_nowait(frame)

        finally:

            buf.unmap(mapinfo)

        return Gst.FlowReturn.OK
    
    def _connect_bus(self):

        bus = self.pipeline.get_bus()

        bus.add_signal_watch()

        bus.connect("message", self._on_bus_message)


    def _on_bus_message(self, _bus, message):

        t = message.type

        if t == Gst.MessageType.ERROR:

            err, dbg = message.parse_error()

            self.logger.error(err)

            if dbg:

                self.logger.error(dbg)

        elif t == Gst.MessageType.EOS:

            self.logger.info("End of stream")

                           