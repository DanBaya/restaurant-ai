#!/bin/bash
set -e

echo "Starting Ollama..."
ollama serve &

echo "Waiting for Ollama to be ready..."
until curl -s http://localhost:11434 > /dev/null; do
    sleep 1
done
echo "Ollama is ready."

echo "Starting Flask..."
python app.py