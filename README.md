# Mini Systematic Trading Backtester (Python)

## Goal
Build a small, correct backtesting engine for a rule-based trading strategy using daily closing prices.
The first strategy to implement is an SMA crossover trend-following strategy.

## Current MVP (Phase 1)
- Convert daily closing prices to daily returns
- Compute SMA(short) and SMA(long) with proper warm-up handling
- Generate a daily **position series** (0 = flat, 1 = long) using SMA crossover
- Backtest the strategy using a realistic timing rule
- Output basic performance results (e.g., cumulative return; more metrics later)

## Strategy specification: SMA Crossover (20/50)
- **Data:** daily closing prices
- **Indicators:**
  - `SMA_short` = 20-day simple moving average
  - `SMA_long` = 50-day simple moving average
- **Rule (positions):**
  - If `SMA_short(t) > SMA_long(t)`, then `position(t) = 1`
  - Else `position(t) = 0`
- **Warm-up:** `position = 0` until both SMAs are available
- **Execution timing:** signal on day `t` → position applied on day `t+1` (to avoid lookahead bias)

## Why 20/50?
These are initial default parameters (not optimized) to keep development simple.
Robust parameter selection will be addressed later using out-of-sample testing.

## Project structure
- `src/algo_trading/` – core logic (indicators, strategies, backtester)
- `scripts/` – runnable examples / toy backtests
- `tests/` – unit tests (pytest)

## How to run (coming soon)
A toy example will be runnable via `scripts/` and will print positions + returns + cumulative return.

## Roadmap
- **Phase 1:** Core strategy + toy backtest (correctness first)
- **Phase 2:** Unit tests (pytest) for indicators, strategy, backtester
- **Phase 3:** Add transaction costs / slippage and additional metrics (drawdown, Sharpe)
- **Phase 4:** API (FastAPI) + persistence of backtest runs (SQLite/Postgres)
- **Phase 5:** Docker + CI + documentation polish

