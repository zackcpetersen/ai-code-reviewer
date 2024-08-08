#!/bin/bash
set -e

# Validate inputs
if [ "$INPUT_LANGCHAIN_TRACING_V2" = "true" ]; then
  if [ -z "$INPUT_LANGCHAIN_API_KEY" ] || [ -z "$INPUT_LANGCHAIN_PROJECT" ]; then
    echo "Error: langchain_api_key and langchain_project are required when langchain_tracing_v2 is true"
    exit 1
  fi
fi

python3 /app/main.py
