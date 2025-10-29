#!/bin/bash
# Script to run the white agent (implementation agent)

cd "$(dirname "$0")/white_agents"

# Load environment variables if .env exists
if [ -f ../.env ]; then
    export $(cat ../.env | grep -v '^#' | xargs)
fi

# Default values if not set in .env
WHITE_AGENT_PORT=${WHITE_AGENT_PORT:-8006}
WHITE_LAUNCHER_PORT=${WHITE_LAUNCHER_PORT:-7006}
MODEL_TYPE=${MODEL_TYPE:-openai}
MODEL_NAME=${MODEL_NAME:-gpt-4o-mini}

echo "========================================"
echo "Starting White Agent (Implementation)"
echo "========================================"
echo "Agent Port: $WHITE_AGENT_PORT"
echo "Launcher Port: $WHITE_LAUNCHER_PORT"
echo "Model: $MODEL_TYPE/$MODEL_NAME"
echo "========================================"
echo ""

agentbeats run white_agent_card_4.toml \
    --launcher_host 0.0.0.0 \
    --launcher_port $WHITE_LAUNCHER_PORT \
    --agent_host 0.0.0.0 \
    --agent_port $WHITE_AGENT_PORT \
    --model_type $MODEL_TYPE \
    --model_name $MODEL_NAME