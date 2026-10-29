"""
Lab 6 - Branch Coverage tests for salon_booking.py
Run:
    coverage run --branch -m pytest BranchCoverageTest_salon_booking.py
    coverage report -m
Every decision is exercised for BOTH its True and False outcome, including
boundary values (<=, >=, >) of each comparison.
"""
import pytest
from salon_booking import extra_time_charge, can_book, arrival_status


# ============ extra_time_charge ============
# Branch: service not in INCLUDED_MIN  (True / False)
def test_unknown_service_raises():
    with pytest.raises(ValueError, match="unknown service"):
        extra_time_charge("massage", 30, "junior", False)


# Branch: duration_min < 0  (True / False)
def test_negative_duration_raises():
    with pytest.raises(ValueError, match="invalid duration"):
        extra_time_charge("haircut", -1, "junior", False)


def test_zero_duration_is_valid():  # boundary: 0 is not < 0
    assert extra_time_charge("haircut", 0, "junior", False) == 0


# Branch: is_member and service != "spa"  (member+non-spa / non-member / member+spa)
def test_member_non_spa_gets_bonus():
    assert extra_time_charge("haircut", 45, "junior", True) == 0       # 30+15
    assert extra_time_charge("colour", 75, "junior", True) == 0        # 60+15


def test_non_member_gets_no_bonus():
    assert extra_time_charge("haircut", 45, "junior", False) == 15 * 10


def test_member_spa_gets_no_bonus():
    assert extra_time_charge("spa", 100, "junior", True) == 10 * 10   # still 90 included


# Branch: extra <= 0  (True / False) + boundaries
def test_exactly_included_time_is_free():  # extra == 0
    assert extra_time_charge("haircut", 30, "senior", False) == 0


def test_one_minute_over_is_charged():     # extra == 1
    assert extra_time_charge("haircut", 31, "junior", False) == 10


# Branch: stylist_level == "junior"  (True / False)
def test_junior_rate():
    assert extra_time_charge("colour", 70, "junior", False) == 10 * 10


def test_non_junior_rate():
    assert extra_time_charge("colour", 70, "mid", False) == 10 * 18


# Branch: extra > 60  (True / False) + boundaries
def test_extra_exactly_60_no_surcharge():
    assert extra_time_charge("haircut", 90, "mid", False) == 60 * 18


def test_extra_61_has_surcharge():
    assert extra_time_charge("haircut", 91, "mid", False) == 61 * 26


# Branch: stylist_level == "senior"  (True / False) inside long overrun
def test_long_overrun_junior():
    assert extra_time_charge("haircut", 100, "junior", False) == 70 * 18


def test_long_overrun_senior():
    assert extra_time_charge("haircut", 100, "senior", False) == 70 * 30


# ============ can_book ============
# Branch: is_walk_in  (True / False)
def test_walk_in_party_of_two():
    assert can_book(2, 1, True) is True


def test_walk_in_party_of_three():
    assert can_book(3, 1, True) is False


# Branch: party_size > 4  (True / False) + boundary
def test_booking_party_of_five_rejected():
    assert can_book(5, 1, False) is False


def test_booking_party_of_four_allowed():
    assert can_book(4, 2, False) is True


# Branch: services <= 2  (True / False)
def test_booking_too_many_services():
    assert can_book(2, 3, False) is False


def test_can_book():
    assert can_book(2, 1, False) is True


# ============ arrival_status ============
# Branch: is_colour (True / False) x is_weekend (True / False) x outcome
def test_colour_weekday_open_at_cutoff():       # cutoff 10
    assert arrival_status(10, True, False) == "open"


def test_colour_weekday_late():                 # 9 -> between -5 and 10
    assert arrival_status(9, True, False) == "late"


def test_colour_weekday_late_lower_boundary():  # cutoff-15 = -5
    assert arrival_status(-5, True, False) == "late"


def test_colour_weekday_closed():
    assert arrival_status(-6, True, False) == "closed"


def test_non_colour_weekday_open():             # cutoff 5
    assert arrival_status(5, False, False) == "open"


def test_non_colour_weekday_late():
    assert arrival_status(4, False, False) == "late"


def test_non_colour_weekday_closed():
    assert arrival_status(-11, False, False) == "closed"


def test_non_colour_weekend_open():             # cutoff 15
    assert arrival_status(15, False, True) == "open"


def test_non_colour_weekend_late():
    assert arrival_status(14, False, True) == "late"


def test_colour_weekend_open():                 # cutoff 20
    assert arrival_status(20, True, True) == "open"


def test_colour_weekend_closed():               # 20-15 = 5
    assert arrival_status(4, True, True) == "closed"
