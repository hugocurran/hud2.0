#!/bin/bash

set -e

echo "Installing Raspberry Pi HUD dependencies..."

sudo apt update

sudo apt install -y \
    python3-opencv \
    python3-gi \
    python3-gi-cairo \
    python3-numpy \
    gir1.2-gstreamer-1.0 \
    gir1.2-gst-plugins-base-1.0 \
    gir1.2-gst-plugins-bad-1.0 \
    gstreamer1.0-tools \
    gstreamer1.0-plugins-base \
    gstreamer1.0-plugins-good \
    gstreamer1.0-plugins-bad \
    ffmpeg

if [ ! -d ".venv" ]; then
    python3 -m venv --system-site-packages .venv
fi

source .venv/bin/activate

python3 -m pip install --upgrade pip

python3 -m pip install pymavlink

echo
echo "Done."
echo
echo "Activate using:"
echo
echo "source .venv/bin/activate"
