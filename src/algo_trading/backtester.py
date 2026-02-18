from algo_trading.indicators import daily_returns
from algo_trading.strategy import SMA_Crossover
from dataclasses import dataclass


@dataclass
class BacktesterResults:
    positions:list
    equity_curve: list
    final_return:float

class Backtester:
    def __init__(self,strategy,prices):
        self.prices = prices
        self.strategy = strategy


    def run(self):
        strategy = self.strategy
        positions = strategy.positions(self.prices)
        daily_ret = daily_returns(self.prices)
        n = len(daily_ret)


        # List for strategy returns
        strategy_returns = [0]* n
        # Strategy Returns logic
        for i in range(1, n):
            strategy_returns[i] = daily_ret[i] * positions[i-1]

        # Equity Curve
        equity = [1.0]

        # Loop through changing the list with the wealth returns
        for i in range(1, n):
            wealth = equity[i-1] * (1 + strategy_returns[i])
            equity.append(wealth)

        # Final return
        start_wealth = equity[0]
        end_wealth = equity[-1]

        final_return = (end_wealth/start_wealth) -1

        results = BacktesterResults(positions, equity, final_return)

        return results


# prices = [200, 199, 198, 197, 196, 195, 194, 193, 192, 191,
# 190, 189, 188, 187, 186, 185, 184, 183, 182, 181,
# 180, 179, 178, 177, 176, 175, 174, 173, 172, 171,
# 171, 172, 173, 174, 175, 176, 177, 178, 179, 180,
# 181, 182, 183, 184, 185, 186, 187, 188, 189, 190,
# 191, 192, 193, 194, 195, 196, 197, 198, 199, 200]

# test_strat = SMA_Crossover()
# test1 = Backtester(test_strat, prices)
# print(test1.run())
