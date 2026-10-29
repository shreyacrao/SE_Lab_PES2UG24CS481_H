"""
Lab 6 - Code (Line) Coverage tests for salon_booking.py
Run:
    coverage run -m pytest CodeCoverageTest_salon_booking.py
    coverage report -m
"""
import pytest
from salon_booking import extra_time_charge, can_book, arrival_status


# ---------------- extra_time_charge ----------------
def test_within_included_time():
    assert extra_time_charge("haircut", 20, "junior", False) == 0


def test_unknown_service_raises():
    with pytest.raises(ValueError, match="unknown service"):
        extra_time_charge("massage", 30, "junior", False)


def test_negative_duration_raises():
    with pytest.raises(ValueError, match="invalid duration"):
        extra_time_charge("haircut", -5, "junior", False)


def test_member_bonus_time_no_charge():
    # haircut 30 + 15 member bonus = 45 included -> 45 min is free
    assert extra_time_charge("haircut", 45, "junior", True) == 0


def test_junior_extra_charge():
    # 10 extra minutes * Rs.10
    assert extra_time_charge("haircut", 40, "junior", False) == 100


def test_non_junior_extra_charge():
    # 10 extra minutes * Rs.18
    assert extra_time_charge("haircut", 40, "mid", False) == 180


def test_long_overrun_non_senior():
    # 70 extra minutes -> (18 + 8) * 70
    assert extra_time_charge("haircut", 100, "mid", False) == 70 * 26


def test_long_overrun_senior():
    # 70 extra minutes -> (18 + 8 + 4) * 70
    assert extra_time_charge("haircut", 100, "senior", False) == 70 * 30


# ---------------- can_book ----------------
def test_can_book():
    assert can_book(2, 1, False) is True


def test_walk_in_booking():
    assert can_book(2, 1, True) is True


def test_party_too_large():
    assert can_book(5, 1, False) is False


# ---------------- arrival_status ----------------
def test_arrival_open():
    assert arrival_status(10, True, False) == "open"


def test_arrival_late():
    assert arrival_status(0, False, False) == "late"


def test_arrival_closed():
    assert arrival_status(-20, False, False) == "closed"


def test_arrival_weekend():
    assert arrival_status(15, False, True) == "open"
