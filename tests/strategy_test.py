import pytest
from pytest import approx
from algo_trading.strategy import SMA_Crossover

def test_sma_strategy_alignment():
   prices = [200, 199, 198, 197, 196, 195, 194, 193, 192, 191,
            190, 189, 188, 187, 186, 185, 184, 183, 182, 181,
            180, 179, 178, 177, 176, 175, 174, 173, 172, 171,
            171, 172, 173, 174, 175, 176, 177, 178, 179, 180,
            181, 182, 183, 184, 185, 186, 187, 188, 189, 190,
            191, 192, 193, 194, 195, 196, 197, 198, 199, 200
            ]
   test = SMA_Crossover()
   results = test.positions(prices)

   expected_tail = [0, 0, 1, 1, 1, 1, 1, 1, 1, 1]

   assert results[:test.long_window-1] == [0]* (test.long_window-1)
   assert results[test.long_window:] == expected_tail

def test_sma_strategy_empty_list():
   prices = []
   test = SMA_Crossover()

   with pytest.raises(ValueError, match=r"Empty List"):
        test.positions(prices)


def test_sma_strategy_constant_prices():
      prices = [200, 200, 200, 200, 200, 200, 200, 200, 200, 200,
                200, 200, 200, 200, 200, 200, 200, 200, 200, 200,
                200, 200, 200, 200, 200, 200, 200, 200, 200, 200,
                200, 200, 200, 200, 200, 200, 200, 200, 200, 200,
                200, 200, 200, 200, 200, 200, 200, 200, 200, 200,
                200, 200, 200, 200, 200, 200, 200, 200, 200, 200,
               ]

      test = SMA_Crossover()
      results = test.positions(prices)

      assert results == [0]*len(prices)



