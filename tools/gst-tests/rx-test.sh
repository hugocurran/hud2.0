#!/bin/bash

# SRT
#  ↓
# tsparse
#  ↓
# tsdemux
#  ↓
# h264parse
#  ↓
# decoder
#  ↓
# autovideosink

# What changed?
#   0.1 Add sync=false to autovideosink
#   0.2 Added tsparse before tsdemux

set -e

source env-common.sh
source env-wsl.sh

trap 'echo; echo "Receiver stopped"; exit 0' INT

build_pipeline()
{
    cat <<EOF
srtsrc 
    uri=srt://${PI_HOST}:${SRT_PORT}
    latency=50
! tsparse
! tsdemux
! h264parse
! avdec_h264
! autovideosink 
    sync=false
EOF
}

echo "======================================="
echo "HUD Video Test Harness"
echo "Receiver Test"
echo "Version 0.2"
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

# Start receiver
gst-launch-1.0 -v $PIPELINE


