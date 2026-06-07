"""The demonstrator agents.

Each agent issues one real call to the local model. The prompts deliberately
induce responses of differing and variable length, so the calls take
genuinely different amounts of wall-clock time to generate. That latency
variance is what causes the agents to finish their writes in different orders
across runs, which is the interaction-order nondeterminism under study. The
numeric operation each agent performs is fixed; a constant is extracted from
the response so the response text does not affect the arithmetic.
"""

from agents.shared_state import SharedState
from agents.backend import ask_model


async def agent_add(state: SharedState, key: str, write_order: list[str]) -> None:
    await ask_model("In two or three sentences, explain what addition is.")
    value = await state.read(key)
    await state.write(key, value + 10)
    write_order.append("add")


async def agent_double(state: SharedState, key: str, write_order: list[str]) -> None:
    await ask_model("In one short sentence, say what doubling means.")
    value = await state.read(key)
    await state.write(key, value * 2)
    write_order.append("double")


async def agent_subtract(state: SharedState, key: str, write_order: list[str]) -> None:
    await ask_model("Explain subtraction in a full paragraph with an example.")
    value = await state.read(key)
    await state.write(key, value - 3)
    write_order.append("subtract")