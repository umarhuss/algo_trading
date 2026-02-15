from algo_trading.indicators import sma, daily_returns
import pytest
from pytest import approx


def test_sma_alignment_and_values_window_3():
    prices = [100, 102, 101, 105]
    window = 3

    result = sma(prices, window)

    # output aligned to input length
    assert len(result) == len(prices)

    # first window-1 values are None 
    assert result[: window - 1] == [None] * (window - 1)

    # known-answer tail (only where SMA exists)
    expected_tail = [
        (100 + 102 + 101) / 3,     # index 2
        (102 + 101 + 105) / 3,     # index 3
    ]
    assert result[window - 1 :] == pytest.approx(expected_tail)


def test_sma_window_greater_than_length_returns_all_none():
    # if window > len(prices), we return a list of Nones of length n
    prices = [100, 102, 101, 105]
    window = 6

    result = sma(prices, window)

    assert len(result) == len(prices)
    assert all(x is None for x in result)


def test_sma_empty_prices_returns_empty_list():
    prices = []
    window = 3

    result = sma(prices, window)

    assert result == []


def test_sma_window_1_equals_prices():
    # window=1 means SMA at each point is just the price itself (no warm-up)
    prices = [100, 102, 101, 105]
    window = 1

    result = sma(prices, window)

    assert result == pytest.approx(prices)


def test_sma_constant_prices_stays_constant_after_warmup():
    prices = [10, 10, 10, 10, 10, 10]
    window = 3

    result = sma(prices, window)

    assert len(result) == len(prices)
    assert result[: window - 1] == [None] * (window - 1)
    assert result[window - 1 :] == pytest.approx([10, 10, 10, 10])


