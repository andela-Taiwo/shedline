import math

import pytest
from hypothesis import given
from hypothesis import strategies as st

from shedline.stages import MAX_STAGE, StagePolicy, declare_stage

POLICY = StagePolicy(stage_size_mw=1000, reserve_mw=500)


def test_no_shedding_when_supply_covers_demand_and_reserve() -> None:
    decision = declare_stage(available_mw=30_500, demand_mw=30_000, policy=POLICY)
    assert decision.stage == 0
    assert decision.shed_mw == 0
    assert not decision.at_risk


def test_smallest_stage_that_covers_the_shortfall() -> None:
    # Shortfall is 30_000 + 500 - 28_000 = 2_500 MW, so stage 3 (3_000 MW).
    decision = declare_stage(available_mw=28_000, demand_mw=30_000, policy=POLICY)
    assert decision.stage == 3
    assert decision.shed_mw == 3_000
    assert decision.uncovered_mw == 0


def test_exact_multiple_does_not_round_up() -> None:
    decision = declare_stage(available_mw=28_500, demand_mw=30_000, policy=POLICY)
    assert decision.stage == 2


def test_shortfall_beyond_the_highest_stage_is_reported() -> None:
    decision = declare_stage(available_mw=10_000, demand_mw=30_000, policy=POLICY)
    assert decision.stage == MAX_STAGE
    assert decision.uncovered_mw == 30_000 + 500 - 10_000 - MAX_STAGE * 1000
    assert decision.at_risk


@pytest.mark.parametrize(
    ("available", "demand"), [(-1, 10), (10, -1), (math.nan, 10), (10, math.inf)]
)
def test_rejects_bad_inputs(available: float, demand: float) -> None:
    with pytest.raises(ValueError):
        declare_stage(available_mw=available, demand_mw=demand, policy=POLICY)


@pytest.mark.parametrize(("size", "reserve"), [(0, 0), (-5, 0), (100, -1), (math.nan, 0)])
def test_rejects_bad_policy(size: float, reserve: float) -> None:
    with pytest.raises(ValueError):
        StagePolicy(stage_size_mw=size, reserve_mw=reserve)


amounts = st.floats(min_value=0, max_value=100_000, allow_nan=False, allow_infinity=False)


@given(available=amounts, demand=amounts)
def test_declared_stage_is_minimal_and_sufficient(available: float, demand: float) -> None:
    decision = declare_stage(available_mw=available, demand_mw=demand, policy=POLICY)
    shortfall = demand + POLICY.reserve_mw - available
    assert 0 <= decision.stage <= MAX_STAGE
    # Sufficient: what is shed plus what is uncovered accounts for the whole shortfall.
    assert decision.shed_mw + decision.uncovered_mw >= max(0.0, shortfall) - 1e-6
    # Minimal: one stage lower would not have been enough (unless capped at the top).
    if decision.stage > 0 and not decision.at_risk:
        assert (decision.stage - 1) * POLICY.stage_size_mw < shortfall
