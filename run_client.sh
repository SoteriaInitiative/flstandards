#!/bin/bash
set -e

# Display relevant environment configuration
echo "SERVER_ADDRESS=${SERVER_ADDRESS:-localhost:8080}"
echo "BANK_ID=${BANK_ID:-1}"
echo "GCS_BUCKET_NAME=${GCS_BUCKET_NAME:-}"
echo "GOAML_PREFIX=${GOAML_PREFIX:-20250823_191247}"
echo "GOAML_LIMIT=${GOAML_LIMIT:-}"

python app/client.py
