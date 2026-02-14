from algo_trading.indicators import sma, daily_returns
import pytest
from pytest import approx


def test_sma_alignment():
    prices = [100, 102, 101, 105]
    time = 3

    result = sma(prices, time)

    expected = [None, None, 101,102.666666667]

    assert len(result) == 4
    assert result == pytest.approx(expected)

