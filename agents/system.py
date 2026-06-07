"""Runs one execution of the multi-agent system.

run_once() launches all agents concurrently with asyncio.gather and returns
the final shared state and the order in which agents completed their writes.
Each agent makes a real, concurrent call to the local model; the variable
latency of those calls is what causes the agents to interleave differently
across runs. Each call starts from fresh state so runs are independent.
"""

import asyncio
from agents.shared_state import SharedState
from agents.workers import agent_add, agent_double, agent_subtract


async def run_once(initial: dict[str, int]) -> tuple[dict[str, int], list[str]]:
    state = SharedState(initial)
    key = "value"
    write_order: list[str] = []
    await asyncio.gather(
        agent_add(state, key, write_order),
        agent_double(state, key, write_order),
        agent_subtract(state, key, write_order),
    )
    return state.snapshot(), write_order