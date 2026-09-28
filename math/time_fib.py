"""Fibonacci Benchmark: Iterative vs Recursive (with cache)

Two modes are tested:
  - cold cache: cache cleared and re-filled bottom-up before each timed call.
  - warm cache: cache persists, showing recursive at its O(1) best.
"""

from statistics import mean, median, stdev
from time import perf_counter as counter
from functools import lru_cache
from sys import setrecursionlimit

setrecursionlimit(10**6)
COL = 14


class FibBenchmark:
    """Benchmarks iterative vs recursive (lru_cache) Fibonacci implementations.

    Args:
        ns:         List of Fibonacci indices to test.
        iterations: Timed calls per (n, algorithm) pair.
        warm_cache: False -> cache cleared before each call (cold / fair).
                    True  -> cache persists (best-case recursive).
    """

    def __init__(self, ns=None, iterations=300, warm_cache=False):
        self.ns = ns or [10, 50, 100, 500, 1_000, 5_000, 10_000]
        self.iterations = iterations
        self.warm_cache = warm_cache
        self._iter_cache: dict[int, int] = {}
        self._results: list[dict] = []

    # ── Algorithms ────────────────────────────────────────────────────────────

    @staticmethod
    def _make_fib_rec():
        """Return a fresh fib_rec instance with an empty lru_cache."""

        @lru_cache(maxsize=None)
        def fib_rec(x: int) -> int:
            return x if x < 2 else fib_rec(x - 1) + fib_rec(x - 2)

        return fib_rec

    def _fib_iter(self, x: int) -> int:
        """Iterative Fibonacci with instance-level cache."""
        if x in self._iter_cache:
            return self._iter_cache[x]
        if x < 2:
            return x
        a, b = 0, 1
        for _ in range(2, x + 1):
            a, b = b, a + b
        self._iter_cache[x] = b
        return b

    # ── Benchmark core ────────────────────────────────────────────────────────

    def _benchmark(self, func, n: int, clear_cache=None) -> dict:
        times = []
        for _ in range(self.iterations):
            if clear_cache:
                clear_cache()
            t0 = counter()
            func(n)
            times.append((counter() - t0) * 1_000)
        return {
            "mean": mean(times),
            "median": median(times),
            "stdev": stdev(times) if len(times) > 1 else 0.0,
        }

    def run(self):
        """Run the full benchmark suite, store results, then print via __str__."""
        self._results.clear()

        for n in self.ns:
            print(f"  Benchmarking n={n} ...", end="\r")

            fib_rec = self._make_fib_rec()

            # Fill cache bottom-up to avoid recursion-depth overflow on first call.
            for i in range(n + 1):
                fib_rec(i)

            if self.warm_cache:
                clear = None
            else:

                def clear(fr=fib_rec, val=n):
                    fr.cache_clear()
                    for i in range(val + 1):
                        fr(i)

            iter_stats = self._benchmark(self._fib_iter, n)
            rec_stats = self._benchmark(fib_rec, n, clear_cache=clear)

            self._results.append(
                {
                    "n": n,
                    "iter_mean": iter_stats["mean"],
                    "iter_median": iter_stats["median"],
                    "iter_stdev": iter_stats["stdev"],
                    "rec_mean": rec_stats["mean"],
                    "rec_median": rec_stats["median"],
                    "rec_stdev": rec_stats["stdev"],
                }
            )

        print(" " * 50, end="\r")
        print(self)

    # ── Reporting ─────────────────────────────────────────────────────────────

    @staticmethod
    def _row(*cells) -> str:
        return "| " + " | ".join(str(c).ljust(COL) for c in cells) + " |"

    @staticmethod
    def _divider() -> str:
        seg = "-" * (COL + 2)
        return "+" + ("+".join([seg] * 6)) + "+"

    def __str__(self) -> str:
        if not self._results:
            return "<FibBenchmark: no results yet — call run() first>"

        mode = "warm (persistent)" if self.warm_cache else "cold (cleared each call)"
        bars = "=" * 67
        lines = [
            f"\n{bars}",
            f"  Fibonacci Benchmark  |  {self.iterations} iters per n  |  cache: {mode}",
            f"{bars}\n",
            self._divider(),
            self._row(
                "n", "Algorithm", "Mean (ms)", "Median (ms)", "Stdev (ms)", "Winner"
            ),
            self._divider(),
        ]

        iter_wins = 0
        for r in self._results:
            iter_faster = r["iter_mean"] < r["rec_mean"]
            if iter_faster:
                iter_wins += 1
            speedup = max(r["iter_mean"], r["rec_mean"]) / max(
                min(r["iter_mean"], r["rec_mean"]), 1e-12
            )
            winner_iter = f"<< x{speedup:.1f}" if iter_faster else ""
            winner_rec = f"<< x{speedup:.1f}" if not iter_faster else ""
            lines += [
                self._row(
                    r["n"],
                    "Iterative",
                    f"{r['iter_mean']:.6f}",
                    f"{r['iter_median']:.6f}",
                    f"{r['iter_stdev']:.6f}",
                    winner_iter,
                ),
                self._row(
                    "",
                    "Recursive",
                    f"{r['rec_mean']:.6f}",
                    f"{r['rec_median']:.6f}",
                    f"{r['rec_stdev']:.6f}",
                    winner_rec,
                ),
                self._divider(),
            ]

        rec_wins = len(self._results) - iter_wins
        overall = "Iterative" if iter_wins >= rec_wins else "Recursive (cached)"
        lines.append("\n-- Per-n Summary " + "-" * 50)
        for r in self._results:
            faster = "iter" if r["iter_mean"] < r["rec_mean"] else "rec "
            delta = abs(r["iter_mean"] - r["rec_mean"])
            lines.append(f"  n={r['n']:<8} faster: {faster}   delta = {delta:.6f} ms")
        lines += [
            "-" * 67,
            f"  Overall winner: {overall}  ({iter_wins}-{rec_wins} across tested n values)",
            "-" * 67 + "\n",
        ]

        return "\n".join(lines)


# ── Main ──────────────────────────────────────────────────────────────────────

if __name__ == "__main__":
    FibBenchmark(iterations=10000, warm_cache=False).run()
    FibBenchmark(iterations=10000, warm_cache=True).run()
