#!/bin/bash

# libcamera
#  ↓
# queue
#  ↓
# videoconvert
#  ↓
# v4l2h264enc
#  ↓
# mpegtsmux
#  ↓
# srtsink

# What changed?
#   0.1 using x264enc (software encoder)
#   0.2 Using v4l2h264enc (hardware encoder)


set -e
#set -x
trap 'echo; echo "Transmitter stopped"; exit 0' INT

source env-common.sh
source env-pi.sh

build_pipeline()
{
    cat <<EOF
libcamerasrc 
! capsfilter caps=video/x-raw,width=1280,height=720,format=NV12,interlace-mode=progressive 
! v4l2h264enc 
    extra-controls="controls,repeat_sequence_header=1" 
! video/x-h264, level=(string)4 
! h264parse 
! mpegtsmux 
    alignment=7 
! queue
! srtsink
    uri=srt://:9000
    mode=listener
    latency=50
    wait-for-connection=true
EOF
}

echo "======================================="
echo "HUD Video Test Harness"
echo "Sender Test"
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
echo

# Start receiver
gst-launch-1.0 -v $PIPELINE


