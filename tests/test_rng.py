import pytest

from shedline.rng import stream


def test_same_seed_and_name_repeat_exactly() -> None:
    a = stream(42, "stations", "breakdowns").random(5)
    b = stream(42, "stations", "breakdowns").random(5)
    assert (a == b).all()


def test_different_names_give_different_streams() -> None:
    a = stream(42, "breakdowns").random(5)
    b = stream(42, "repairs").random(5)
    assert (a != b).any()


def test_different_seeds_give_different_streams() -> None:
    assert (stream(1, "demand").random(5) != stream(2, "demand").random(5)).any()


def test_name_parts_are_not_concatenated_ambiguously() -> None:
    a = stream(7, "ab", "c").random(3)
    b = stream(7, "a", "bc").random(3)
    assert (a != b).any()


def test_drawing_from_one_stream_does_not_shift_another() -> None:
    expected = stream(9, "repairs").random(3)
    noisy = stream(9, "breakdowns")
    noisy.random(1000)
    assert (stream(9, "repairs").random(3) == expected).all()


@pytest.mark.parametrize(("seed", "names"), [(-1, ("x",)), (1, ()), (1, ("",))])
def test_rejects_bad_arguments(seed: int, names: tuple[str, ...]) -> None:
    with pytest.raises(ValueError):
        stream(seed, *names)
