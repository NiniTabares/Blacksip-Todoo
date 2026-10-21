"""Preserve decimal amounts; only reorder when binary summation needs it."""
from decimal import Decimal, InvalidOperation
from itertools import permutations
import logging

_logger = logging.getLogger(__name__)


def stable_order(total_text, amount_texts):
    """Return indices; never fix genuinely inconsistent decimal totals.

    XPath 1.0 uses IEEE-754 numbers. Python sum() on recent Python versions
    may compensate floating point errors, so use explicit left-to-right +=.
    The factorial search is bounded to seven subtotals.
    """
    original = tuple(range(len(amount_texts)))
    try:
        texts = [str(value) for value in amount_texts]
        total_decimal = Decimal(str(total_text))
        decimals = [Decimal(value) for value in texts]
        if not total_decimal.is_finite() or any(not v.is_finite() for v in decimals):
            return original
        if sum(decimals, Decimal('0')) != total_decimal:
            return original
        target = float(str(total_text))
        numbers = [float(value) for value in texts]
    except (ValueError, TypeError, InvalidOperation, OverflowError):
        return original

    def matches(order):
        accumulated = 0.0
        for index in order:
            accumulated += numbers[index]
        return accumulated == target

    if matches(original):
        return original
    ascending = tuple(sorted(original, key=lambda index: decimals[index]))
    descending = tuple(reversed(ascending))
    for order in (ascending, descending):
        if matches(order):
            return order
    if len(original) <= 7:
        for order in permutations(original):
            if matches(order):
                return order
    _logger.warning('FAY02: no stable subtotal order found; amounts preserved')
    return original
