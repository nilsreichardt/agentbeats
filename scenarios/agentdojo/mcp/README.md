AGENT_COMMANDS = [
    {
        "name": "Blue Agent",
        "command": "agentbeats run blue_agent_card.toml --launcher_host 0.0.0.0 --launcher_port 9010 --agent_host 0.0.0.0 --agent_port 9011 --backend https://agentbeats.org/api --mcp ['http://localhost:9003/sse', 'http://localhost:9004/sse'] --model_type openai --model_name o4-mini" # can also use model_type=openai, model_name=o4-mini
    },
    {
        "name": "Red Agent",
        "command": "agentbeats run red_agent_card.toml --launcher_host 0.0.0.0 --launcher_port 9020 --agent_host 0.0.0.0 --agent_port 9021 --backend https://agentbeats.org/api --model_type openai --model_name gpt-4o-mini" # use gpt-4o-mini in case it refuses to answer
    },
    {
        "name": "Green Agent",
        "command": "agentbeats run green_agent/green(weaker)_agent_card.toml --launcher_host 0.0.0.0 --launcher_port 9030 --agent_host 0.0.0.0 --agent_port 9031 --backend https://agentbeats.org/api --mcp ['http://localhost:9001/sse', 'http://localhost:9003/sse', 'http://localhost:9004/sse'] --tool green_agent/tools.py --model_type openai --model_name o4-mini"
    }
]