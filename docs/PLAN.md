# Plan

Shedline is built in sessions, each with a clear success test. Later sessions build on
earlier ones.

| # | Session | Success |
|---|---|---|
| 1 | Network and data model, synthetic country generator on the IEEE 118 and 300-bus grids | Generated countries validate, bad data is rejected clearly, generation is deterministic from a seed |
| 2 | AC power flow (Newton-Raphson, sparse) and a DC approximation | Matches reference solutions to 1e-6; non-convergence is reported |
| 3 | Supply simulation: breakdowns, repairs, maintenance, fuel limits, fixed demand profiles | Outage rates match configured rates within tolerance; each hour maps to the right stage |
| 4 | Rotation engine: exemptions, no back-to-back cuts, line limits, fairness over weeks | Property tests prove no rule is broken; fairness beats a round-robin baseline |
| 5 | Frequency response, under-frequency shedding and restoration with cold load pickup | Frequency behaves as predicted; restoration never causes a new overload |
| 6 | Live engine and web UI: clock, injected events, WebSocket stream, map, lookup, replay | Playwright covers a week's run, a mid-day station trip and a block lookup |
| 7 | Scale and reporting: 10,000+ blocks, a 52-week run, fairness and unserved-energy reports | A simulated year runs within budget; reports reproduce from the seed |

## Rules

- All data is synthetic and generated from a seed. Every run replays exactly.
- Demand comes from fixed, documented profiles. No forecasting models.
- A shortfall the highest stage cannot cover is reported, never hidden.
