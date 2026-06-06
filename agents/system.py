"""Runs one execution of the multi-agent system.

run_once() launches all agents concurrently with asyncio.gather and returns
the final shared state. Each call starts from a fresh state so runs are
independent. Because the agents are deterministic, the only thing that can
differ between two calls is the interleaving chosen by the scheduler, which
is exactly what the divergence experiment in Stage 2 measures.
"""

import asyncio
from agents.shared_state import SharedState
from agents.workers import agent_add, agent_double, agent_subtract


async def run_once(initial: dict[str, int]) -> dict[str, int]:
    state = SharedState(initial)
    key = "value"
    await asyncio.gather(
        agent_add(state, key),
        agent_double(state, key),
        agent_subtract(state, key),
    )
    return state.snapshot()