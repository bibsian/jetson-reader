#!/bin/bash
cd /workspace
uv sync
/workspace/.venv/bin/python -m ipykernel install --user --name=reader --display-name="Reading Assistant"
/usr/sbin/sshd
exec jupyter notebook --ip=0.0.0.0 --port=8888 --allow-root --no-browser
