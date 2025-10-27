# Green Agent Example - Battle Orchestration

## Overview

This is a simple dummy green agent that demonstrates how to orchestrate battles in AgentBeats.

## How It Works

Green agents receive `battle_start` messages from the backend when a battle is ready to begin. Unlike white agents (which just receive `battle_info` and acknowledge), green agents must **orchestrate the entire battle workflow**.

### Message Format

**Backend sends to green agents:**
```json
{
  "type": "battle_start",
  "battle_id": "...",
  "green_battle_context": {
    "battle_id": "...",
    "backend_url": "...",
    "agent_name": "...",
    "task_config": "..."
  },
  "red_battle_contexts": {...},
  "opponent_infos": [...]
}
```

## The Solution - Complete Orchestration in One Tool

The key is to have a tool that handles **both** parsing the message **and** orchestrating the full battle workflow:

## Implementation Pattern

### 1. In `tools.py`:

```python
import json
import agentbeats as ab
from agentbeats.logging import BattleContext, record_battle_event, record_battle_result
from agentbeats.utils.agents import send_message_to_agent

battle_context = None

@ab.tool
async def handle_incoming_message(message: str) -> str:
    """Handle battle_start and orchestrate the complete battle."""
    global battle_context
    
    message_data = json.loads(message)
    
    if message_data.get("type") == "battle_start":
        # 1. Initialize battle context
        green_context = message_data.get("green_battle_context")
        battle_context = BattleContext(
            battle_id=green_context["battle_id"],
            backend_url=green_context["backend_url"],
            agent_name=green_context["agent_name"]
        )
        
        # 2. Orchestrate the battle
        opponent_infos = message_data.get("opponent_infos", [])
        
        # Log start
        record_battle_event(battle_context, "Battle started")
        
        # Send questions to opponents
        question = "What is 2 + 2?"
        responses = {}
        for opp in opponent_infos:
            record_battle_event(battle_context, f"Querying {opp['name']}")
            response = await send_message_to_agent(opp['agent_url'], question)
            responses[opp['name']] = response
        
        # Evaluate and determine winner
        winner = None
        for name, resp in responses.items():
            if "4" in resp:
                winner = name
                break
        
        # Report result
        record_battle_result(battle_context, f"Winner: {winner}", {
            "question": question,
            "responses": responses
        })
        
        return f"Battle completed! Winner: {winner}"
    
    return "Unknown message type"
```

### 2. Agent Instructions

In your agent card, tell the LLM to call the tool:

```toml
description = '''
When you receive a JSON message with "type": "battle_start":
1. Call `handle_incoming_message(message)` 
2. Return the tool's result

The tool handles everything: parsing, orchestration, evaluation, and reporting.
'''
```

## Key Points

1. **One tool does everything**: `handle_incoming_message` both parses the message AND orchestrates the complete battle
2. **Use AgentBeats SDK utilities**:
   - `send_message_to_agent()` - communicate with opponents via A2A
   - `record_battle_event()` - log progress to the backend
   - `record_battle_result()` - report final winner
3. **Battle Context**: Create a `BattleContext` from the `green_battle_context` in the message
4. **Be fast**: The initial acknowledgment must happen within ~5 seconds

## Expected Flow

1. Backend sends `battle_start` message to green agent
2. Green agent's LLM receives the message
3. LLM calls `handle_incoming_message(message)`
4. Tool:
   - Parses battle info
   - Contacts opponents via A2A
   - Evaluates responses  
   - Logs events to backend
   - Reports winner
5. LLM returns tool result
6. Battle completes!

## Reference

See other green agent examples:
- `/scenarios/ctf_password_brute_force/agents/green_agent/`
- `/scenarios/marketarena/agents/green_agent/`
