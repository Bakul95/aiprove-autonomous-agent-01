#!/bin/sh
# Run the autonomous agent. Prefers the python with eth-account installed.
if [ -x "$HOME/.local/evm/bin/python" ]; then
  PY="$HOME/.local/evm/bin/python"
else
  PY="python3"
fi
exec "$PY" "$(dirname "$0")/run.py" "$@"
