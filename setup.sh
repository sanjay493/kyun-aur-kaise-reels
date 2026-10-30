#!/usr/bin/env bash
# One-time setup: Python packages + Kokoro voice model (~350 MB, not stored in git).
set -e
cd "$(dirname "$0")"
pip install --break-system-packages -q -r requirements.txt 2>/dev/null || pip install -q -r requirements.txt
mkdir -p models
BASE=https://github.com/thewh1teagle/kokoro-onnx/releases/download/model-files-v1.0
[ -s models/kokoro-v1.0.onnx ] || curl -sSL -o models/kokoro-v1.0.onnx $BASE/kokoro-v1.0.onnx
[ -s models/voices-v1.0.bin ]  || curl -sSL -o models/voices-v1.0.bin  $BASE/voices-v1.0.bin
command -v ffmpeg >/dev/null || echo "WARNING: ffmpeg not found - install it before rendering"
echo "Setup done."
