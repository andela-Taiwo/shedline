"""Deterministic, independent random streams derived from one run seed.

Every random process in a simulation (station breakdowns, repair times, demand noise)
gets its own named stream. Adding a new stream, or drawing more numbers from one, never
changes the numbers another stream produces, so a run stays reproducible as the model grows.
"""

from __future__ import annotations

import hashlib

import numpy as np


def stream(seed: int, *names: str) -> np.random.Generator:
    """Return a generator for the stream identified by ``seed`` and ``names``.

    The same seed and names always give the same sequence; different names give
    statistically independent sequences.
    """
    if seed < 0:
        raise ValueError("seed must be zero or positive")
    if not names or any(not name for name in names):
        raise ValueError("a stream needs at least one non-empty name")
    key = hashlib.sha256("\x1f".join(names).encode()).digest()
    words = [int.from_bytes(key[i : i + 4], "little") for i in range(0, len(key), 4)]
    return np.random.Generator(np.random.PCG64(np.random.SeedSequence([seed, *words])))
