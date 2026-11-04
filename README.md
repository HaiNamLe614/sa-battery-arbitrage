# SA Battery Arbitrage

Forecasting South Australian wholesale electricity prices and scheduling a
grid battery to buy low and sell high, using public AEMO market data.

## Goals
- Forecast SA1 5-minute prices 24 hours ahead and beat a naive baseline
- Produce a charge/discharge schedule and compare revenue to perfect foresight
- Serve results through an API, containerised and deployed to AWS

## Non-goals (for now)
- Live trading or bidding into the market
- Regions other than SA1
- Frequency control (FCAS) markets

## Status
M1 complete: baseline forecast done. Next up is M2, a forecasting model with weather features.

## Data
- AEMO aggregated price and demand data for SA1, 5-minute intervals, Nov 2023 to Oct 2025
- 210,528 intervals, with no missing or duplicated timestamps
- Timestamps are AEMO market time (UTC+10, no daylight saving) and mark the end of each interval
- Data isn't stored in the repo. Run `uv run scripts/download_prices.py` to fetch it.

## M0: Data exploration
Notebook: `notebooks/01_spike.ipynb`

All prices in AUD/MWh.

- Prices are negative about a third of the time, mostly around -10 to -20, because wind and solar bid below zero.
- Spikes are rare but extreme. The 99th percentile is 300 but the max in the sample was 14,500.
- There's a clear daily pattern. Prices are lowest around 13:00 (median -14) and highest around 18:00 (median 135), so a battery has a reliable charge/discharge window.

## M1: Baseline forecast
Notebook: `notebooks/02_baseline.ipynb`

**Task:** every day at midnight, forecast all 288 five-minute prices for the next 24 hours.

**Test period:** 1 Aug to 31 Oct 2025, locked and never used for tuning.

**Metric:** MAE in AUD/MWh, reported overall, for normal intervals, and for spikes (price above 300).

| Baseline | MAE | MAE normal | MAE spike |
|---|---|---|---|
| Same time yesterday | 64.0 | 61.5 | 319.2 |
| Same time last week | 80.3 | 77.4 | 374.5 |
| Median of last 7 days | **58.4** | **55.3** | 370.5 |

The 7-day median is the best baseline, so **the number to beat is an MAE of 58.4.** My target for M2 is under 50.

What I learned:
- The baseline gets the midday solar trough right almost every day.
- Most of the error comes from evenings. Either wind covers demand and prices stay near 0, or it doesn't and they jump past 100. The baseline averages the two, so it's wrong either way.
- Spikes only add about 4 to the overall MAE, so better forecasts on normal days matter more than chasing spikes.
- Same time yesterday is better on spikes than the median, which suggests spikes come in runs.

## Roadmap
- [x] M0: Setup and data exploration
- [x] M1: Baseline forecast
- [ ] M2: Forecasting model with weather features
- [ ] M3: Battery optimiser
- [ ] M4: Package, tests and CI
- [ ] M5: Database and data pipeline
- [ ] M6: FastAPI service
- [ ] M7: Docker
- [ ] M8: AWS deployment