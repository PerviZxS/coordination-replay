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