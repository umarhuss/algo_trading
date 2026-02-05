from indicators import daily_returns
from strategy import SMA_Crossover

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



