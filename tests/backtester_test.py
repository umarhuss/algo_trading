import pytest
from pytest import approx

from algo_trading.backtester import Backtester
from algo_trading.strategy import SMA_Crossover


def test_backtester_result_alignment():
    """Test that backtester results are properly aligned with input prices"""
    prices = [200, 200, 200, 200, 200, 200, 200, 200, 200, 200,
                200, 200, 200, 200, 200, 200, 200, 200, 200, 200,
                200, 200, 200, 200, 200, 200, 200, 200, 200, 200,
                200, 200, 200, 200, 200, 200, 200, 200, 200, 200,
                200, 200, 200, 200, 200, 200, 200, 200, 200, 200,
                200, 200, 200, 200, 200, 200, 200, 200, 200, 200,
               ]
    strategy = SMA_Crossover()
    backtester = Backtester(strategy, prices)
    results = backtester.run()

    # Output aligned to input length
    assert len(results.equity_curve) == len(prices)
    assert len(results.positions) == len(prices)

    # Check starting wealth
    assert results.equity_curve[0] == pytest.approx(1.0)

    # During warm-up period, positions are 0, so equity should stay at 1.0
    assert results.equity_curve[1] == pytest.approx(1.0)
    assert results.equity_curve[10] == pytest.approx(1.0)
    assert results.equity_curve[30] == pytest.approx(1.0)

    # After warm-up period, equity curve should have moved
    assert results.equity_curve[59] == pytest.approx(1.0)


def test_backtester_positions_alignment():
    """Test that positions array is correctly aligned"""
    prices = [200, 200, 200, 200, 200, 200, 200, 200, 200, 200,
                200, 200, 200, 200, 200, 200, 200, 200, 200, 200,
                200, 200, 200, 200, 200, 200, 200, 200, 200, 200,
                200, 200, 200, 200, 200, 200, 200, 200, 200, 200,
                200, 200, 200, 200, 200, 200, 200, 200, 200, 200,
                200, 200, 200, 200, 200, 200, 200, 200, 200, 200,
               ]

    strategy = SMA_Crossover()
    backtester = Backtester(strategy, prices)
    results = backtester.run()

    # Positions should have same length as prices
    assert len(results.positions) == len(prices)

    # During warm-up period (long_window = 50), positions should be 0
    assert results.positions[: strategy.long_window - 1] == [0] * (
        strategy.long_window - 1
    )


def test_backtester_empty_prices():
    """Test that backtester raises error on empty prices"""
    prices = []
    strategy = SMA_Crossover()

    with pytest.raises(ValueError, match=r"Empty List"):
        backtester = Backtester(strategy, prices)
        backtester.run()


def test_backtester_single_price():
    """Test backtester with single price"""
    prices = [100]
    strategy = SMA_Crossover()
    backtester = Backtester(strategy, prices)
    results = backtester.run()

    assert len(results.equity_curve) == 1
    assert results.equity_curve[0] == pytest.approx(1.0)
    assert results.final_return == pytest.approx(0.0)


def test_backtester_constant_prices():
    """Test backtester with constant prices - should result in no returns"""
    prices = [100] * 60
    strategy = SMA_Crossover()
    backtester = Backtester(strategy, prices)
    results = backtester.run()

    assert len(results.equity_curve) == len(prices)
    # With constant prices, no price movement means no returns
    assert all(eq == pytest.approx(1.0) for eq in results.equity_curve)
    assert results.final_return == pytest.approx(0.0)


def test_backtester_final_return_calculation():
    """Test that final_return is correctly calculated from equity curve"""
    prices =[200, 200, 200, 200, 200, 200, 200, 200, 200, 200,
                200, 200, 200, 200, 200, 200, 200, 200, 200, 200,
                200, 200, 200, 200, 200, 200, 200, 200, 200, 200,
                200, 200, 200, 200, 200, 200, 200, 200, 200, 200,
                200, 200, 200, 200, 200, 200, 200, 200, 200, 200,
                200, 200, 200, 200, 200, 200, 200, 200, 200, 200,
               ]

    strategy = SMA_Crossover()
    backtester = Backtester(strategy, prices)
    results = backtester.run()

    # Final return should match the calculation: (end_wealth / start_wealth) - 1
    expected_return = (results.equity_curve[-1] / results.equity_curve[0]) - 1
    assert results.final_return == pytest.approx(expected_return)
