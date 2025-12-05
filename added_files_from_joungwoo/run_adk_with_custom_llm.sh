#!/bin/bash
# ADK Web with Custom LLM - Run script

DOCKER_CONTAINER="43a7821ec23580ac2939c3a3c45d567a6d980ad6a8751f60bc343f09169d4870"

echo "🚀 Starting ADK Web with Custom LLM..."
echo ""

docker exec -it "$DOCKER_CONTAINER" bash -c '
# Load environment variables
source /root/.bashrc

# Verify environment
echo "=== Environment Check ==="
echo "Model: $model"
echo "API Base: $api_base"
echo ""

# Navigate to project directory
cd /root/chainreaction

# Run ADK Web
echo "=== Starting ADK Web Server ==="
adk web . --host 0.0.0.0 --port 38010 --allow_origins="*" --reload --reload_agents
'
