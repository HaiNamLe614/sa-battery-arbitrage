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
M0: data spike in progress
