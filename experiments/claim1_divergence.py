"""Claim 1: interaction order diverges under concurrency with real agents.

Runs the multi-agent system N times. Each agent makes one real call to the
local model at temperature 0, so the response content is effectively constant
across runs and the only varying element is the wall-clock latency of the
concurrent model calls. Any difference in write order across runs is therefore
attributable to how those real latencies interleave, not to the model's output
and not to the agents' logic. The script reports how often the write order and
the final state diverged, and the wall-clock time per run.
"""

import asyncio
import time
from collections import Counter
from agents.system import run_once


def measure_divergence(n: int, initial: dict[str, int]) -> dict:
    orders: list[tuple[str, ...]] = []
    final_states: list[int] = []
    run_times: list[float] = []

    overall_start = time.perf_counter()
    for i in range(n):
        run_start = time.perf_counter()
        state, write_order = asyncio.run(run_once(dict(initial)))
        elapsed = time.perf_counter() - run_start

        orders.append(tuple(write_order))
        final_states.append(state["value"])
        run_times.append(elapsed)
        print(f"  run {i + 1}/{n}: {tuple(write_order)} in {elapsed:.1f}s")

    total_time = time.perf_counter() - overall_start
    distinct_orders = Counter(orders)
    distinct_finals = Counter(final_states)

    return {
        "runs": n,
        "distinct_orders": len(distinct_orders),
        "order_distribution": dict(distinct_orders),
        "distinct_final_states": len(distinct_finals),
        "final_state_distribution": dict(distinct_finals),
        "order_divergence_rate": 1.0 - (distinct_orders.most_common(1)[0][1] / n),
        "total_time_seconds": total_time,
        "mean_run_time_seconds": sum(run_times) / n,
    }


def main() -> None:
    result = measure_divergence(n=30, initial={"value": 5})
    print()
    print(f"Runs: {result['runs']}")
    print(f"Distinct write orders observed: {result['distinct_orders']}")
    print(f"Order distribution: {result['order_distribution']}")
    print(f"Distinct final states: {result['distinct_final_states']}")
    print(f"Final state distribution: {result['final_state_distribution']}")
    print(f"Order divergence rate: {result['order_divergence_rate']:.3f}")
    print(f"Total time: {result['total_time_seconds']:.1f}s")
    print(f"Mean time per run: {result['mean_run_time_seconds']:.1f}s")


if __name__ == "__main__":
    main()