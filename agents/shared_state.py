"""Shared state store accessed by all agents.

A thin wrapper over a dictionary. Read and write are async so that the
asyncio scheduler can interleave agents between operations; this is what
makes interaction-order nondeterminism observable. In later stages the
coordination log is attached inside read() and write(), so that every
state access is recorded automatically without the agents being aware of it.
"""

class SharedState:
    def __init__(self, initial: dict[str, int]):
        self._data = dict(initial)

    async def read(self, key: str) -> int:
        return self._data[key]

    async def write(self, key: str, value: int) -> None:
        self._data[key] = value

    def snapshot(self) -> dict[str, int]:
        return dict(self._data)