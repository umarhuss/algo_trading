from algo_trading.indicators import daily_returns
from algo_trading.strategy import SMA_Crossover
from dataclasses import dataclass
from algo_trading.db_reader import get_prices


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


strategy = SMA_Crossover()
prices = get_prices(1)
real_data_test = Backtester(strategy, prices)
results = real_data_test.run()
print(f"Final Return: {results.final_return:.2%}")
print(f"Number of trades: {sum(1 for i in range(1, len(results.positions)) if results.positions[i] != results.positions[i-1])}")

