# Shedline

Simulate national load shedding: the planned rolling blackouts a country runs when it does not
have enough electricity for everyone.

> **Status: foundation only.** The project layout, tooling, stage rules and seeded random
> streams exist and are tested. The network model, power flow, supply simulation, rotation
> engine and web UI are not built yet. See [the plan](docs/PLAN.md).

## What it will do

Shedline models the whole chain, so a schedule comes out of a simulated grid rather than a
fixed rota:

- **Supply**: power stations with random breakdowns, maintenance and fuel limits, simulated
  hour by hour. The shortfall decides the stage, from stage 1 up to stage 8.
- **Grid physics**: power flow across regions, so shedding in the right place relieves
  overloaded lines, and frequency response after a large station trips.
- **Rotation**: thousands of feeder blocks shared fairly over weeks, with exemptions for
  critical sites and no back-to-back cuts.
- **Restoration**: bringing blocks back without new overloads (cold load pickup).
- **Live view**: a map of which areas are off, a block schedule lookup and a replayable week.

All data is synthetic and generated from a seed. No real utility or customer data is used.

## What exists today

| Module | What it does |
|---|---|
| `shedline.stages` | Maps available supply, demand and reserve to the smallest stage that covers the shortfall, and reports any shortfall beyond stage 8 |
| `shedline.rng` | Named, independent random streams from one run seed, so runs replay exactly |

## Quickstart

Requires [uv](https://docs.astral.sh/uv/) and Python 3.12.

```bash
make setup   # install locked dependencies
make check   # lint, format check, type check and tests
make help    # list every target
```

## Layout

```
src/shedline/   # the simulator package
tests/          # unit and property tests
docs/PLAN.md    # what is being built, in order
docs/adr/       # architecture decision records
```

## Licence

MIT. See [LICENSE](LICENSE).
