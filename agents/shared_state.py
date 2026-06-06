class SharedState:
    def __init__(self, initial: dict[str, int]):
        self._data = dict(initial)

    async def read(self, key: str) -> int:
        return self._data[key]

    async def write(self, key: str, value: int) -> None:
        self._data[key] = value

    def snapshot(self) -> dict[str, int]:
        return dict(self._data)