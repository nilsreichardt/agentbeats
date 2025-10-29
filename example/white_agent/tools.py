# -*- coding: utf-8 -*-
"""
Dummy Green Agent Tools

This file provides example tools for a green (evaluation) agent.
These tools are used to communicate with other agents and report battle results.
"""

import json
import agentbeats as ab
from agentbeats.logging import BattleContext

# Global state to store battle context
battle_context = None
opponent_infos = []


@ab.tool
async def handle_incoming_message(message: str) -> str:
    """
    Handle incoming messages from the AgentBeats backend and orchestrate battles.
    This processes battle_start notifications and runs the full battle workflow.
    
    Args:
        message: The incoming message (usually JSON)
    
    Returns:
        str: Battle result summary
    """
    global battle_context, opponent_infos
    
    try:
        # Parse the message as JSON
        try:
            message_data = json.loads(message)
        except json.JSONDecodeError:
            return f"Received non-JSON message: {message}"
        
        # Check if this is a battle start message
        if message_data.get("type") == "battle_start":
            battle_id = message_data.get("battle_id")
            green_battle_context = message_data.get("green_battle_context")
            opponent_infos = message_data.get("opponent_infos", [])
            
            if not battle_id or not green_battle_context:
                return "Invalid battle start message - missing battle_id or green_battle_context"
            
            # Create battle context from the provided data
            battle_context = BattleContext(
                battle_id=green_battle_context.get("battle_id"),
                backend_url=green_battle_context.get("backend_url"),
                agent_name=green_battle_context.get("agent_name")
            )
            
            # Now orchestrate the battle automatically
            return await orchestrate_battle(battle_id, opponent_infos)
        
        return f"Received message of type: {message_data.get('type', 'unknown')}"
        
    except Exception as e:
        return f"Error processing message: {str(e)}"


async def orchestrate_battle(battle_id: str, opponents: list) -> str:
    """
    Orchestrate the dummy battle: send questions, collect responses, evaluate, and report.
    
    Args:
        battle_id: The battle ID
        opponents: List of opponent info dicts with 'agent_url' and 'name'
    
    Returns:
        str: Battle completion summary
    """
    from agentbeats.utils.agents import send_message_to_agent
    from agentbeats.logging import record_battle_event, record_battle_result
    
    global battle_context
    
    if not battle_context:
        return "Error: Battle context not initialized"
    
    try:
        # Step 1: Log battle start
        record_battle_event(battle_context, "Battle orchestration started")
        
        # Step 2: Send question to each opponent
        question = "What is 2 + 2?"
        responses = {}
        
        for opponent in opponents:
            agent_url = opponent.get("agent_url")
            agent_name = opponent.get("name", agent_url)
            
            if not agent_url:
                continue
                
            record_battle_event(battle_context, f"Sending question to {agent_name}")
            response = await send_message_to_agent(agent_url, question)
            responses[agent_name] = response
            record_battle_event(battle_context, f"Received response from {agent_name}: {response}")
        
        # Step 3: Evaluate responses
        if not responses:
            record_battle_event(battle_context, "No responses received from opponents")
            record_battle_result(battle_context, "No winner - no responses", {})
            return "Battle ended: No responses received"
        
        # Simple evaluation: check if answer contains "4"
        winner = None
        winner_score = 0
        
        for agent_name, response in responses.items():
            score = calculate_score(response, "accuracy")
            record_battle_event(battle_context, f"Score for {agent_name}: {score}")
            
            if score > winner_score:
                winner_score = score
                winner = agent_name
        
        # Step 4: Report final result
        result_detail = {
            "question": question,
            "responses": responses,
            "scores": {name: calculate_score(resp, "accuracy") for name, resp in responses.items()},
            "winner": winner
        }
        
        record_battle_result(
            battle_context,
            f"Battle completed - Winner: {winner}",
            result_detail
        )
        
        return f"Battle completed! Winner: {winner} with score {winner_score}"
        
    except Exception as e:
        error_msg = f"Error orchestrating battle: {str(e)}"
        record_battle_event(battle_context, error_msg)
        return error_msg


@ab.tool
def simple_evaluation(response_a: str, response_b: str, question: str) -> str:
    """
    A simple evaluation function that compares two responses to a question.
    
    Args:
        response_a: First agent's response
        response_b: Second agent's response
        question: The question that was asked
    
    Returns:
        str: Evaluation result indicating which response was better
    """
    # Simple heuristic evaluation (you can make this more sophisticated)
    score_a = len(response_a)  # Longer response might be more detailed
    score_b = len(response_b)
    
    # Check for key indicators
    if question.lower().find("2 + 2") != -1:
        if "4" in response_a:
            score_a += 100
        if "4" in response_b:
            score_b += 100
    
    if score_a > score_b:
        winner = "Agent A"
        reason = f"Agent A provided a better response (score: {score_a} vs {score_b})"
    elif score_b > score_a:
        winner = "Agent B"
        reason = f"Agent B provided a better response (score: {score_b} vs {score_a})"
    else:
        winner = "Tie"
        reason = f"Both agents provided equally good responses (score: {score_a})"
    
    result = f"Winner: {winner}\nReason: {reason}\n\nAgent A response: {response_a}\n\nAgent B response: {response_b}"
    return result


@ab.tool
def calculate_score(response: str, criteria: str = "helpfulness") -> int:
    """
    Calculate a score for an agent's response based on given criteria.
    
    Args:
        response: The agent's response to evaluate
        criteria: The evaluation criteria (e.g., "helpfulness", "accuracy", "conciseness")
    
    Returns:
        int: A score between 0-100
    """
    score = 50  # Base score
    
    # Simple scoring heuristics
    if criteria == "helpfulness":
        # Longer responses might be more helpful
        score += min(len(response) // 10, 30)
        # Polite responses get bonus points
        if any(word in response.lower() for word in ["please", "thank you", "help"]):
            score += 10
    
    elif criteria == "accuracy":
        # Check for specific correct answers (this is simplified)
        if "4" in response and "2 + 2" in response:
            score += 40
    
    elif criteria == "conciseness":
        # Shorter responses score higher for conciseness
        if len(response) < 50:
            score += 30
        elif len(response) < 100:
            score += 20
        else:
            score += 10
    
    # Cap score at 100
    return min(score, 100)


# Note: The MCP tools (talk_to_agent, update_battle_process, report_on_battle_end)
# are provided automatically by the AgentBeats platform when you connect to the
# backend MCP server. You don't need to define them here - just use them in your
# agent's responses!
