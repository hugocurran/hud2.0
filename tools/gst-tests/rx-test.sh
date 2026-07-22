#!/bin/bash

# SRT
#  ↓
# tsdemux
#  ↓
# h264parse
#  ↓
# decoder
#  ↓
# autovideosink

set -e

source env-common.sh
source env-wsl.sh

trap 'echo; echo "Receiver stopped"; exit 0' INT

build_pipeline()
{
    cat <<EOF
srtsrc uri=srt://${PI_HOST}:${SRT_PORT}
! tsdemux
! h264parse
! avdec_h264
! autovideosink
EOF
}

echo "======================================="
echo "HUD GStreamer Receiver"
echo "======================================="
echo "Host : ${PI_HOST}"
echo "Port : ${SRT_PORT}"

PIPELINE=$(build_pipeline)
echo
echo "Pipeline:"
echo "$PIPELINE"

# Start receiver
gst-launch-1.0 -v $PIPELINE


