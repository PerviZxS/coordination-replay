"""The demonstrator agents.

Each agent performs a fixed, deterministic operation on a shared value:
read it, then write back a modified version. The agents are intentionally
trivial and contain no randomness, so that any variation in the final
result across runs is attributable solely to the order in which the agents
access shared state, not to the agents themselves.
"""

import asyncio
from agents.shared_state import SharedState


async def agent_add(state: SharedState, key: str) -> None:
    value = await state.read(key)
    # Yield between read and write so other agents can interleave here.
    # This exposes the read-modify-write race that real I/O (e.g. an LLM
    # call) would introduce naturally in a production system.
    await asyncio.sleep(0)
    await state.write(key, value + 10)


async def agent_double(state: SharedState, key: str) -> None:
    value = await state.read(key)
    await asyncio.sleep(0)
    await state.write(key, value * 2)


async def agent_subtract(state: SharedState, key: str) -> None:
    value = await state.read(key)
    await asyncio.sleep(0)
    await state.write(key, value - 3)