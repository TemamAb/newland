#!/bin/sh

# Check Akash CLI is operational
if ! akash version >/dev/null 2>&1; then
  echo "Akash CLI check failed" >&2
  exit 1
fi

# Check Python dependencies
if ! python -c "import web3, aiohttp" 2>/dev/null; then
  echo "Python dependencies check failed" >&2
  exit 1
fi

# Optional: Check web service endpoint
if ! curl -fsS http://localhost:8080/healthz >/dev/null 2>&1; then
  echo "Health endpoint check failed" >&2
  exit 1
fi

exit 0
