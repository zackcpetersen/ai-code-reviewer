#!/bin/bash
set -e

# Validate inputs
if [ "LANGCHAIN_TRACING_V2" = "true" ]; then
  if [ -z "LANGCHAIN_API_KEY" ] || [ -z "LANGCHAIN_PROJECT" ]; then
    echo "Error: langchain_api_key and langchain_project are required when langchain_tracing_v2 is true"
    exit 1
  fi
fi

python3 /app/main.py
