#!/bin/bash
apt-get update && apt-get install -y cmake libopenblas-dev liblapack-dev libx11-dev
pip install --no-cache-dir dlib
pip install --no-cache-dir face_recognition
