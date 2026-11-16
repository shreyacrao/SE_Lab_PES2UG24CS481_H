import math

GST_RATE = 1.18
MAX_INPUT_LENGTH = 1000      # guard against huge inputs (DoS)
MAX_MINUTES = 24 * 60        # a single booking cannot exceed one day


def _to_finite_float(value):
    """Convert a string to a finite float, or return None if not possible."""
    try:
        number = float(value.strip())
    except (ValueError, TypeError, AttributeError, OverflowError):
        return None
    if not math.isfinite(number):          # rejects nan, inf, -inf
        return None
    return number


def parse_booking(text):
    """'service:minutes' -> (Service, minutes) or None for invalid input."""
    if not isinstance(text, str) or len(text) > MAX_INPUT_LENGTH:
        return None

    parts = text.split(':')
    if len(parts) != 2:                    # missing or extra ':'
        return None

    service = parts[0].strip()
    if not service:                        # empty service name
        return None

    minutes = _to_finite_float(parts[1])
    if minutes is None or minutes <= 0 or minutes > MAX_MINUTES:
        return None

    return service.title(), minutes


def duration_average(durations_csv):
    """'30,45,60' -> average duration (float, 2 dp) or None for invalid input."""
    if not isinstance(durations_csv, str) or len(durations_csv) > MAX_INPUT_LENGTH:
        return None

    values = []
    for raw in durations_csv.split(','):
        raw = raw.strip()
        if not raw:                        # empty element, e.g. "30,,45" or ""
            return None
        try:
            value = int(raw)
        except ValueError:                 # non-numeric / oversized digit string
            return None
        if value < 0:                      # negative duration makes no sense
            return None
        values.append(value)

    if not values:                         # avoid ZeroDivisionError
        return None

    # true division instead of '//' so 30,45 -> 37.5, not 37
    return round(sum(values) / len(values), 2)


def payable_bill(text):
    """'bill|discount' -> amount payable after 18% GST (>= 0) or None."""
    if not isinstance(text, str) or len(text) > MAX_INPUT_LENGTH:
        return None

    parts = text.split('|')
    if len(parts) != 2:                    # missing or extra '|'
        return None

    bill = _to_finite_float(parts[0])
    discount = _to_finite_float(parts[1])
    if bill is None or discount is None:
        return None
    if bill < 0 or discount < 0:
        return None

    total = bill * GST_RATE - discount
    if not math.isfinite(total):           # e.g. 1e308 * 1.18 overflows to inf
        return None

    return round(max(total, 0), 2)


def main():
    print("==== Running parse_booking ====")
    user_input = input("Enter service:duration in min (e.g. haircut:45): ")
    result = parse_booking(user_input)
    if result is None:
        print("Invalid input! Use the format service:minutes (e.g. haircut:45)")
    else:
        print("Service and Duration:", result)

    print("\n==== Running duration_average ====")
    user_input = input("Enter durations as CSV (e.g. 30,45,60): ")
    result = duration_average(user_input)
    if result is None:
        print("Invalid input! Enter non-negative whole numbers separated by commas")
    else:
        print("Average Duration:", result)

    print("\n==== Running payable_bill ====")
    user_input = input("Enter bill|discount (e.g. 800|100): ")
    result = payable_bill(user_input)
    if result is None:
        print("Invalid input! Use the format bill|discount with non-negative numbers")
    else:
        print("Payable Bill:", result)


if __name__ == "__main__":
    main()
