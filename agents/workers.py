import asyncio
from agents.shared_state import SharedState


async def agent_add(state: SharedState, key: str) -> None:
    value = await state.read(key)
    await asyncio.sleep(0)  # I'm pausing here, run someone else if you want.
    await state.write(key, value + 10)


async def agent_double(state: SharedState, key: str) -> None:
    value = await state.read(key)
    await asyncio.sleep(0)
    await state.write(key, value * 2)


async def agent_subtract(state: SharedState, key: str) -> None:
    value = await state.read(key)
    await asyncio.sleep(0)
    await state.write(key, value - 3)