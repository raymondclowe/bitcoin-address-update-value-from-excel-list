#!/bin/bash

# Add uv to PATH
export PATH="$HOME/.local/bin:$PATH"

# Run Electrum daemon in the uv environment
uv run electrum daemon -d