#!/usr/bin/env bash
set -euo pipefail

# Script: yt_hype.sh
# Usage: RAPIDAPI_KEY=xxxx ./yt_hype.sh
# This script calls the yt-api hype endpoint and prints the JSON response.

RAPIDAPI_KEY="${RAPIDAPI_KEY:-}"
if [ -z "$RAPIDAPI_KEY" ]; then
  echo "RAPIDAPI_KEY is not set. Export it or run 'op read' to inject it from 1Password.'" >&2
  exit 2
fi

curl --request GET \
  --url 'https://yt-api.p.rapidapi.com/hype?geo=US' \
  --header 'Content-Type: application/json' \
  --header "x-rapidapi-host: yt-api.p.rapidapi.com" \
  --header "x-rapidapi-key: $RAPIDAPI_KEY"
