# Reading Assistant

A Jetson Nano-based tool that helps users learn to read physical books by detecting wand taps on words and speaking them aloud.

## Quick Start

```bash
# Install dependencies
uv sync

# Run the assistant
uv run reader
```

## Development

See [SCAFFOLDING.md](SCAFFOLDING.md) for architecture and implementation details.

### Dev Container

```bash
cd .devcontainer
docker compose up -d --build
ssh -p 2222 root@localhost  # password: dev
```
