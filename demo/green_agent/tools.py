# -*- coding: utf-8 -*-
"""
Dummy Green Agent Tools

This file provides example tools for a green (evaluation) agent.
These tools are used to communicate with other agents and report battle results.
"""

import json
import asyncio
import random
import agentbeats as ab
from agentbeats.logging import BattleContext, record_battle_event, record_battle_result

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
    global battle_context

    if not battle_context:
        return "Error: Battle context not initialized"

    try:
        def wait_secs_log(label: str, secs: float):
            record_battle_event(battle_context, f"{label}")

        async def sleep_scaled(secs: float):
            # await asyncio.sleep(min(secs * 0.05, 0.25))
            # await asyncio.sleep(secs * 0.2)
            await asyncio.sleep(secs)

        wait_secs_log("Spinning up database", 1)
        await sleep_scaled(1)
        wait_secs_log("Spinning up Marketplace API", 1)
        await sleep_scaled(1)
        wait_secs_log("Environment ready", 0.5)
        await sleep_scaled(0.5)

        seller_count = 5
        consumer_count = 10
        rounds = 3

        sellers = {}
        overall_profit = {f"Seller {i}": 0.0 for i in range(1, seller_count + 1)}
        round_winners = []

        for r in range(1, rounds + 1):
            wait_secs_log(f"Starting round {r}", 0.2)
            await sleep_scaled(0.2)

            wait_secs_log("White Agents can now create products", 0.2)
            await sleep_scaled(0.2)

            sellers = {}
            creation_order = list(range(1, seller_count + 1))
            random.shuffle(creation_order)
            for i in creation_order:
                price = float(random.randint(10, 50))
                prod_name = f"Product {i}"
                sellers[f"Seller {i}"] = {
                    "name": f"Seller {i}",
                    "product": prod_name,
                    "description": "",
                    "image": "",
                    "price": price,
                    "round_profit": 0.0,
                }
                wait = random.choice([0.1, 0.2])
                wait_secs_log(f"Seller {i} created product \"{prod_name}\"", wait)
                await sleep_scaled(wait)

            wait_secs_log("Every seller created a product. Going to the next phase", 0.2)
            await sleep_scaled(0.2)

            async def consumer_phase(day: int):
                wait_secs_log("Consumer can now buy products", 5)
                await sleep_scaled(5)
                product_names = [sellers[s]["product"] for s in sellers]
                consumer_order = list(range(1, consumer_count + 1))
                random.shuffle(consumer_order)
                for c in consumer_order:
                    do_buy = random.random() < 0.5
                    if do_buy:
                        chosen_seller_key = random.choice(list(sellers.keys()))
                        chosen_product = sellers[chosen_seller_key]["product"]
                        price = sellers[chosen_seller_key]["price"]
                        sellers[chosen_seller_key]["round_profit"] += price
                        overall_profit[chosen_seller_key] += price
                        wait_secs_log(f"Consumer {c} bought {chosen_product}", 2)
                        await sleep_scaled(2)
                    else:
                        wait_secs_log(f"Consumer {c} decided not to buy anything", 2)
                        await sleep_scaled(2)

            async def seller_edit_phase(day: int):
                wait_secs_log("Seller can now edit their product pages", 0.2)
                await sleep_scaled(0.2)
                edit_order = list(range(1, seller_count + 1))
                random.shuffle(edit_order)
                for i in edit_order:
                    key = f"Seller {i}"
                    action = random.choice([
                        "name",
                        "description",
                        "image",
                        "price",
                        "nothing",
                    ])
                    if action == "name":
                        sellers[key]["product"] = f"{sellers[key]['product']}"
                        w = random.choice([1.0, 1.5, 2.0])
                        wait_secs_log(f"Seller {i} edited their product name", w)
                        await sleep_scaled(w)
                    elif action == "description":
                        sellers[key]["description"] = "Updated description"
                        w = random.choice([1.0, 1.5, 2.0])
                        wait_secs_log(f"Seller {i} changed product description", w)
                        await sleep_scaled(w)
                    elif action == "image":
                        sellers[key]["image"] = "updated.png"
                        w = random.choice([1.0, 1.5, 2.0])
                        wait_secs_log(f"Seller {i} changed product image", w)
                        await sleep_scaled(w)
                    elif action == "price":
                        old = sellers[key]["price"]
                        delta = 1.0 + random.uniform(-0.2, 0.2)
                        sellers[key]["price"] = max(1.0, round(old * delta, 2))
                        w = random.choice([1.0, 1.5, 2.0])
                        wait_secs_log(f"Seller {i} changed the price of their product", w)
                        await sleep_scaled(w)
                    else:
                        w = random.choice([1.0, 1.5, 2.0])
                        wait_secs_log(f"Seller {i} decided not to edit their product page", w)
                        await sleep_scaled(w)

                wait_secs_log("Every seller made their decision. Going to the next phase", 0.2)
                await sleep_scaled(0.2)

            wait_secs_log("Starting day 1", 0.2)
            await sleep_scaled(0.2)
            wait_secs_log("Using random order for products since it's the first day", 5)
            await sleep_scaled(5)
            await consumer_phase(day=1)
            wait_secs_log("Every consumer made their decision. Going to the next phase", 0.2)
            await sleep_scaled(0.2)

            wait_secs_log("Starting day 2", 0.2)
            await sleep_scaled(0.2)
            await seller_edit_phase(day=2)
            await consumer_phase(day=2)
            wait_secs_log("Every consumer made their decision. Going to the next phase", 0.2)
            await sleep_scaled(0.2)

            wait_secs_log("Starting day 3", 0.2)
            await sleep_scaled(0.2)
            await seller_edit_phase(day=3)
            await consumer_phase(day=3)
            wait_secs_log("Every consumer made their decision. Going to the next phase", 0.2)
            await sleep_scaled(0.2)

            wait_secs_log(f"Round {r} finished", 0.2)
            await sleep_scaled(0.2)

            winner_key = max(sellers.keys(), key=lambda k: sellers[k]["round_profit"])
            round_winners.append({"round": r, "winner": winner_key, "profit": sellers[winner_key]["round_profit"]})
            wait_secs_log(f"Winner of round {r}: {winner_key}", 0.2)
            await sleep_scaled(0.2)

            for k in sellers:
                sellers[k]["round_profit"] = 0.0

        wait_secs_log("Calculating average of all rounds", 0.2)
        await sleep_scaled(0.2)

        averages = {}
        for k, total in overall_profit.items():
            averages[k] = total / rounds

        overall_winner = max(overall_profit.keys(), key=lambda k: overall_profit[k])
        wait_secs_log(f"Seller {overall_winner.split(' ')[1]} is the overall winner", 0.2)
        await sleep_scaled(0.2)

        table = []
        for seller in sorted(overall_profit.keys(), key=lambda k: int(k.split(" ")[1])):
            table.append({
                "seller": seller,
                "avg_profit": round(averages[seller], 2),
                "total_profit": round(overall_profit[seller], 2),
            })

        record_battle_result(
            battle_context,
            f"Overall winner: {overall_winner}",
            overall_winner,
            {
                "round_winners": round_winners,
                "overall_winner": overall_winner,
                "results_table": table,
                "meta": {
                    "sellers": seller_count,
                    "consumers": consumer_count,
                    "rounds": rounds,
                },
            },
        )

        return f"Battle completed. Overall winner: {overall_winner}"

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
