# FxDataIngestor — Forex Data Pipeline & Backtester

A polyglot trading data pipeline built with **C#/.NET** and **Python**. The system ingests real daily forex exchange rates from a REST API, stores them in a normalised SQLite database, and runs a systematic SMA crossover backtest against 25 years of historical data.

---

## What This Project Does

```
Frankfurter API (real forex data)
    → C# ingestion service (daily scheduler)
        → SQLite database (normalised schema)
            → Python backtester (SMA crossover strategy)
                → Backtest result: +13.41% return (USD/GBP, 2000–2026)
```

---

## Tech Stack

| Layer | Technology |
|---|---|
| Data ingestion | C# / .NET (Worker Service) |
| Database ORM | EF Core + SQLite |
| Data source | [Frankfurter API](https://frankfurter.dev) (free, no key required) |
| Backtesting | Python |
| DB connectivity (Python) | `sqlite3` (stdlib) |

---

## Project Structure

```
trading_project/
├── dotnet/
│   └── FxDataIngestor/
│       ├── Migrations/                         # EF Core migration files
│       ├── Models/
│       │   ├── FxDbContext.cs                  # EF Core database context
│       │   ├── Instrument.cs                   # Currency pair entity
│       │   ├── PriceIngestionService.cs        # Duplicate-safe ingestion logic
│       │   └── prices.cs                       # Daily price entity
│       ├── FrankfurterClientRequest.cs         # REST API client (latest + historical)
│       ├── Program.cs                          # DI setup and app entry point
│       └── Worker.cs                           # Background scheduler (15:05 UTC daily)
├── src/
│   └── algo_trading/
│       ├── backtester.py                       # Backtesting engine
│       ├── db_reader.py                        # Reads prices from SQLite into Python
│       ├── indicators.py                       # SMA + daily returns calculations
│       └── strategy.py                         # SMA crossover strategy
└── tests/
    ├── backtester_test.py
    ├── indicators_test.py
    └── strategy_test.py
```

---

## C# Ingestion Service

### Features
- Calls the Frankfurter API daily at **15:05 UTC** (after ECB rate publication at ~16:00 CET)
- Skips weekends automatically
- Prevents duplicate inserts using a **composite primary key** (`InstrumentId + Timeframe + BarTime`)
- Supports **historical backfill** from any start date
- Full dependency injection using .NET's built-in DI container
- Error handling with structured logging throughout

### Running the ingestion service

```bash
cd dotnet/FxDataIngestor
dotnet run
```

---

## Database Schema

**Instruments**

| Column | Type | Notes |
|---|---|---|
| Id | int | Primary key (auto-increment) |
| Symbol | string | e.g. `USD/GBP` (unique index) |
| Base | string | e.g. `USD` |
| Quote | string | e.g. `GBP` |
| Type | string | e.g. `Forex` |

**Prices**

| Column | Type | Notes |
|---|---|---|
| InstrumentId | int | Foreign key → Instruments |
| Timeframe | string | e.g. `1D` |
| BarTime | DateOnly | Date of the rate |
| Close | decimal | Exchange rate |

Composite primary key on Prices: `InstrumentId + Timeframe + BarTime`

---

## Python Backtester

### Strategy: SMA Crossover (20/50)

- **Data:** Daily closing prices read directly from SQLite
- **Indicators:** 20-day and 50-day simple moving averages
- **Signal:** Long (`1`) when SMA20 > SMA50, flat (`0`) otherwise
- **Execution:** Signal on day `t` → position applied on day `t+1` (no lookahead bias)
- **Warm-up:** Position = 0 until both SMAs are available

### Backtest Result (USD/GBP, 2000–2026)

```
Final Return: 13.41%
Number of trades: 150
```

### Running the backtester

```bash
source .venv/bin/activate
python src/algo_trading/backtester.py
```

### Running the tests

```bash
pytest tests/
```

---

## Key Engineering Concepts

- **Async/await** — non-blocking API calls and database writes in C#
- **Dependency injection** — clean service wiring via .NET's built-in DI container
- **EF Core migrations** — schema managed as code, fully reproducible
- **Composite primary keys** — data integrity enforced at the database level
- **Separation of concerns** — API client, ingestion service, scheduler, and DB context each have a single responsibility
- **Polyglot architecture** — C# handles ingestion and persistence; Python handles research and analysis
- **Duplicate prevention** — `FirstOrDefaultAsync` checks before every insert

---

## Setup

### Prerequisites
- .NET 8 SDK
- Python 3.10+

### Install Python dependencies

```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

### Run EF Core migrations (first time only)

```bash
cd dotnet/FxDataIngestor
dotnet ef database update
```

This creates the `Fx_data.db` SQLite file with the correct schema.

---

## Roadmap

- [x] Daily forex ingestion (C# Worker Service)
- [x] Historical backfill from any start date
- [x] Normalised SQLite schema with duplicate prevention
- [x] SMA crossover backtester (Python)
- [x] Python reads directly from SQLite (polyglot pipeline)
- [ ] Multiple currency pairs via configuration (appsettings.json)
- [ ] Additional strategy metrics (Sharpe ratio, max drawdown)
- [ ] ASP.NET Core Web API to expose backtest results
- [ ] Frontend dashboard to visualise equity curves
