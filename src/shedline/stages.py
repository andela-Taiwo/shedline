"""Load-shedding stages and how a supply shortfall maps to one.

A stage is a fixed block of demand to remove: stage ``n`` removes ``n * stage_size_mw``.
The declared stage is the smallest one that covers the shortfall plus the operating
reserve the system operator must keep. Shortfalls beyond the highest stage are reported,
not hidden, because they mean the grid is at risk of a full blackout.
"""

from __future__ import annotations

import math
from dataclasses import dataclass

MAX_STAGE = 8


@dataclass(frozen=True)
class StagePolicy:
    """How shortfalls translate into stages.

    stage_size_mw: demand removed by each stage.
    reserve_mw: operating reserve that must stay available on top of demand.
    """

    stage_size_mw: float
    reserve_mw: float = 0.0

    def __post_init__(self) -> None:
        if not math.isfinite(self.stage_size_mw) or self.stage_size_mw <= 0:
            raise ValueError("stage_size_mw must be a positive, finite number")
        if not math.isfinite(self.reserve_mw) or self.reserve_mw < 0:
            raise ValueError("reserve_mw must be zero or a positive, finite number")


@dataclass(frozen=True)
class StageDecision:
    """The stage declared for one period, and any shortfall it cannot cover."""

    stage: int
    shed_mw: float
    uncovered_mw: float

    @property
    def at_risk(self) -> bool:
        """True when even the highest stage leaves part of the shortfall uncovered."""
        return self.uncovered_mw > 0


def declare_stage(available_mw: float, demand_mw: float, policy: StagePolicy) -> StageDecision:
    """Return the smallest stage that keeps demand plus reserve within available supply."""
    for name, value in (("available_mw", available_mw), ("demand_mw", demand_mw)):
        if not math.isfinite(value) or value < 0:
            raise ValueError(f"{name} must be zero or a positive, finite number")

    shortfall = demand_mw + policy.reserve_mw - available_mw
    if shortfall <= 0:
        return StageDecision(stage=0, shed_mw=0.0, uncovered_mw=0.0)

    needed = math.ceil(shortfall / policy.stage_size_mw)
    stage = min(needed, MAX_STAGE)
    shed = stage * policy.stage_size_mw
    return StageDecision(stage=stage, shed_mw=shed, uncovered_mw=max(0.0, shortfall - shed))
