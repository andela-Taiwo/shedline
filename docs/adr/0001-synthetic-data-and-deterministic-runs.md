# 0001: Synthetic data and deterministic runs

## Status

Accepted

## Context

Shedline needs a country's worth of power stations, lines and feeder blocks. Real utility
data is not available offline and would include information about real customers.
Simulations also involve randomness (breakdowns, repair times), which makes bugs hard to
reproduce unless runs can be replayed.

## Decision

- Every country, station fleet and block layout is synthetic, generated from a seed.
- Each random process draws from its own named stream (`shedline.rng.stream`), derived from
  the run seed and the stream's name. Streams are independent: drawing more numbers from one
  never changes another.

## Consequences

- Any run, and any failing test, can be replayed exactly from its seed.
- Adding a new random process does not change the results of existing ones.
- Results describe a realistic but fictional country, not any real grid.
