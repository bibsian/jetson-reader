#!/bin/bash
# Setup script for Jetson Nano

set -e

echo "Installing system dependencies..."
sudo apt-get update
sudo apt-get install -y \
    tesseract-ocr \
    libgl1-mesa-glx \
    espeak-ng

echo "Installing uv..."
curl -LsSf https://astral.sh/uv/install.sh | sh

echo "Installing Piper TTS..."
# Download Piper binary for ARM64
PIPER_VERSION="v1.2.0"
wget -O /tmp/piper.tar.gz "https://github.com/rhasspy/piper/releases/download/${PIPER_VERSION}/piper_arm64.tar.gz"
tar -xzf /tmp/piper.tar.gz -C /usr/local/bin/
rm /tmp/piper.tar.gz

# Download a voice model
mkdir -p ~/.local/share/piper/voices
wget -O ~/.local/share/piper/voices/en_US-lessac-medium.onnx \
    "https://huggingface.co/rhasspy/piper-voices/resolve/main/en/en_US/lessac/medium/en_US-lessac-medium.onnx"
wget -O ~/.local/share/piper/voices/en_US-lessac-medium.onnx.json \
    "https://huggingface.co/rhasspy/piper-voices/resolve/main/en/en_US/lessac/medium/en_US-lessac-medium.onnx.json"

echo "Setup complete!"
