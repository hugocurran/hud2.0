Experiment	Change	Result
R1	autovideosink sync=false	Significant reduction in latency. Buffering warnings disappeared.

Rx pipeline:
build_pipeline()
{
    cat <<EOF
srtsrc uri=srt://${PI_HOST}:${SRT_PORT}
    latency=50
! queue
    max-size-buffers=1
    leaky=downstream
! tsdemux
! h264parse
! avdec_h264
! autovideosink sync=false
EOF
}
Does not work. Removing the queue fixes it.

On the sender side, using a leaky queue before the encoder makes perfect sense because dropping an occasional frame is preferable to increasing latency. On the receiver side, once the stream has been packetised into MPEG-TS, the integrity of the packet sequence matters much more than keeping latency low by discarding data. In other words, the sender should be free to drop frames, but the receiver should never drop transport packets.


