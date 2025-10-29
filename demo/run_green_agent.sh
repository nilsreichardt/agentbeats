#!/bin/bash
# Script to run the green agent (evaluation agent)

cd "$(dirname "$0")/green_agent"

# Load environment variables if .env exists
if [ -f ../.env ]; then
    export $(cat ../.env | grep -v '^#' | xargs)
fi

# Default values if not set in .env
GREEN_AGENT_PORT=${GREEN_AGENT_PORT:-8002}
GREEN_LAUNCHER_PORT=${GREEN_LAUNCHER_PORT:-7002}
MODEL_TYPE=${MODEL_TYPE:-openai}
MODEL_NAME=${MODEL_NAME:-gpt-4o-mini}

echo "========================================"
echo "Starting Green Agent (Evaluation)"
echo "========================================"
echo "Agent Port: $GREEN_AGENT_PORT"
echo "Launcher Port: $GREEN_LAUNCHER_PORT"
echo "Model: $MODEL_TYPE/$MODEL_NAME"
echo "========================================"
echo ""

agentbeats run green_agent_card.toml \
    --launcher_host 0.0.0.0 \
    --launcher_port $GREEN_LAUNCHER_PORT \
    --agent_host 0.0.0.0 \
    --agent_port $GREEN_AGENT_PORT \
    --model_type $MODEL_TYPE \
    --model_name $MODEL_NAME \
    --tool tools.py
