import math

from hypothesis import given, settings, strategies as st
from salon_booking import parse_booking, duration_average, payable_bill


# ---------------------------------------------------------------
# 1. "No crash" fuzz tests: random text / None must never raise
# ---------------------------------------------------------------

@settings(max_examples=500)
@given(st.text() | st.none())
def test_parse_booking_no_crash(s):
    try:
        parse_booking(s)
    except Exception as e:
        assert False, f"parse_booking crashed on {s!r} with: {e!r}"


@settings(max_examples=500)
@given(st.text() | st.none())
def test_duration_average_no_crash(s):
    try:
        duration_average(s)
    except Exception as e:
        assert False, f"duration_average crashed on {s!r} with: {e!r}"


@settings(max_examples=500)
@given(st.text() | st.none())
def test_payable_bill_no_crash(s):
    try:
        payable_bill(s)
    except Exception as e:
        assert False, f"payable_bill crashed on {s!r} with: {e!r}"


# ---------------------------------------------------------------
# 2. Targeted fuzz tests: inputs that LOOK valid but hide edge cases
# ---------------------------------------------------------------

# "service:minutes" where minutes can be any float text, incl. nan / inf / negative
@given(
    st.text(min_size=0, max_size=20),
    st.floats(allow_nan=True, allow_infinity=True),
)
def test_parse_booking_structured(service, minutes):
    s = f"{service}:{minutes}"
    try:
        result = parse_booking(s)
    except Exception as e:
        assert False, f"parse_booking crashed on {s!r} with: {e!r}"
    if result is not None:
        name, mins = result
        assert isinstance(name, str) and name != ""
        assert math.isfinite(mins) and mins > 0


# CSV of integers, possibly empty, possibly with blank entries like "30,,45"
@given(st.lists(st.integers() | st.just(""), max_size=10))
def test_duration_average_structured(items):
    s = ",".join(str(x) for x in items)
    try:
        result = duration_average(s)
    except Exception as e:
        assert False, f"duration_average crashed on {s!r} with: {e!r}"
    if result is not None:
        assert isinstance(result, (int, float))
        assert result >= 0


# "bill|discount" with any floats, incl. nan / inf / negative
@given(
    st.floats(allow_nan=True, allow_infinity=True),
    st.floats(allow_nan=True, allow_infinity=True),
)
def test_payable_bill_structured(bill, discount):
    s = f"{bill}|{discount}"
    try:
        result = payable_bill(s)
    except Exception as e:
        assert False, f"payable_bill crashed on {s!r} with: {e!r}"
    if result is not None:
        assert math.isfinite(result), f"non-finite bill {result} for {s!r}"
        assert result >= 0


# ---------------------------------------------------------------
# 3. Property tests on VALID inputs: the fixed code must still be correct
# ---------------------------------------------------------------

@given(
    st.sampled_from(["haircut", "facial", "manicure", "hair spa", "pedicure"]),
    st.integers(min_value=1, max_value=600),
)
def test_parse_booking_valid(service, minutes):
    assert parse_booking(f"{service}:{minutes}") == (service.title(), float(minutes))


@given(st.lists(st.integers(min_value=1, max_value=600), min_size=1, max_size=20))
def test_duration_average_valid(values):
    s = ",".join(map(str, values))
    assert duration_average(s) == round(sum(values) / len(values), 2)


@given(
    st.integers(min_value=0, max_value=100000),
    st.integers(min_value=0, max_value=100000),
)
def test_payable_bill_valid(bill, discount):
    expected = round(max(bill * 1.18 - discount, 0), 2)
    assert payable_bill(f"{bill}|{discount}") == expected


# ---------------------------------------------------------------
# 4. Explicit regression cases from the handout-style examples
# ---------------------------------------------------------------

def test_known_edge_cases():
    assert parse_booking("haircut:45") == ("Haircut", 45.0)
    assert parse_booking(None) is None
    assert parse_booking("haircut") is None          # no ':'
    assert parse_booking("a:b:c") is None            # too many ':'
    assert parse_booking(":45") is None              # empty service
    assert parse_booking("haircut:abc") is None      # non-numeric
    assert parse_booking("haircut:-10") is None      # negative minutes
    assert parse_booking("haircut:nan") is None
    assert parse_booking("haircut:inf") is None

    assert duration_average("30,45,60") == 45.0
    assert duration_average("") is None              # ZeroDivision / empty
    assert duration_average("30,,45") is None        # blank element
    assert duration_average("30,abc") is None
    assert duration_average("30,-5") is None         # negative duration
    assert duration_average(None) is None

    assert payable_bill("800|100") == 844.0
    assert payable_bill("100|500") == 0              # never negative
    assert payable_bill("800") is None               # missing '|'
    assert payable_bill("nan|0") is None
    assert payable_bill("inf|0") is None
    assert payable_bill("-800|0") is None
    assert payable_bill("800|-100") is None          # negative discount
    assert payable_bill(None) is None
