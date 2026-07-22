#!/bin/bash

# libcamera
#  ↓
# queue
#  ↓
# videoconvert
#  ↓
# x264enc
#  ↓
# mpegtsmux
#  ↓
# srtsink


set -e
trap 'echo; echo "Transmitter stopped"; exit 0' INT

source env-common.sh
source env-pi.sh

build_pipeline()
{
    cat <<EOF
libcamerasrc
!
video/x-raw,width=${WIDTH},height=${HEIGHT},framerate=${FPS}/1
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
EOF
}

echo "======================================="
echo "HUD Video Test Harness"
echo "Sender Test"
echo "Version 0.1"
echo "TX : ${TX_VER}"
echo "RX : ${RX_VER}"
echo "======================================="
echo
echo "Host : ${PI_HOST}"
echo "Port : ${SRT_PORT}"

PIPELINE=$(build_pipeline)
echo
echo "Pipeline:"
echo "$PIPELINE"
echo

# Start receiver
gst-launch-1.0 -v $PIPELINE


