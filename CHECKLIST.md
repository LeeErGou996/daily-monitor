# Dashboard v2 Migration Checklist

## 1. Routing and preservation
- [x] Preserve the current site under `/legacy/` without deleting its functionality.
- [x] Add a visible LEGACY notice with a link to the current site.
- [x] Make the repository root URL redirect to `/v2/`.

## 2. Overview dashboard
- [x] Keep one normalized comparison chart containing VUAA, XNAS, SEC0, VGWE, and the weighted portfolio.
- [x] Keep compact market cards for all four ETFs, including SEC0.DE, and show clear last-sync status.
- [x] Use four-fund allocation controls with default weights VUAA 35% / XNAS 35% / SEC0 20% / VGWE 10%, keeping the total at 100% and persisting settings locally.
- [x] Backfill SEC0.DE from the portfolio inception date when the stored history does not yet contain the new ticker.

## 3. CPPI correctness
- [x] Treat “Current Portfolio Value” as today’s value directly; do not reapply historical portfolio return.
- [x] Calculate floor, cushion, equity exposure, and cash allocation from the current value.
- [x] Remove wording that implies an absolute floor guarantee.

## 4. Goal projection correctness
- [x] Reject start dates after the available market-history range instead of silently using the first row.
- [x] Detect required-return solutions outside the numerical search interval and report them as out of range.
- [x] Keep the modeled-vs-required path and adaptive CAGR calculation.
- [x] Reorganize Goal Projection around four decision variables only: Baseline CAGR, Adaptive CAGR, Funding Ratio, and Path Gap.
- [x] Make the current model value and required path value explicit without adding another primary metric.
- [x] Persist Goal Projection inputs locally so the planning state survives refresh.
- [x] Improve the progress chart labels and currency formatting without changing the underlying projection model.
- [x] Plot Goal Projection on a proportional time axis so daily historical observations and monthly forward points use their true calendar spacing.
- [x] Mark the boundary between recorded market history and forward required-path projection.
- [x] Explain negative required CAGR as a contribution-versus-target condition without changing the solver.
- [x] Interpret Daily DCA as an amount contributed every calendar day, including weekends and holidays.
- [x] Convert Goal Projection compounding and CAGR annualization from 252 trading days to 365.25 calendar days.
- [x] Accumulate non-trading-day contributions and invest them on the next available market-price date in the historical portfolio replay.
- [x] Keep the required path, modeled portfolio, Funding Ratio, Path Gap, and adaptive CAGR under the same calendar-day convention.

## 5. UX and release validation
- [x] Add responsive layout for narrow screens.
- [x] Replace “real-time” wording with latest daily market data / last sync.
- [x] Keep methodology sections collapsed by default.
- [x] Verify SEC0 snapshot data, SEC0 historical backfill, four-asset portfolio calculations, CPPI, TVM, and responsive rendering before publishing. CI data update and GitHub Pages deployment both passed.
- [x] Verify the Goal Projection redesign on desktop and narrow screens, including persisted inputs, solver error states, and chart rendering. Default-parameter regression passed and GitHub Pages build/deploy completed successfully.
- [x] Verify proportional date spacing, latest-data boundary marker, negative-CAGR explanation, and unchanged numerical outputs before publishing. Screenshot configuration regression passed and GitHub Pages build/deploy completed successfully.
- [x] Verify natural-day contribution totals, weekend/holiday accumulation, solver outputs, chart continuity, and responsive rendering before publishing. Natural-day regression passed; GitHub Actions data update and Pages build/deploy completed successfully.

## 6. v3 Pro dashboard (branch `feature/dashboard-v3-pro-20261004`)
- [x] Keep `/v2/` and `/legacy/` unchanged; add `/v3/` and point the repository root redirect to `/v3/`.
- [x] Restyle: dark/light theme, refined layout, sparkline asset cards, responsive down to 390px.
- [x] Analytics window selector (1M/3M/6M/YTD/ALL), configurable risk-free rate, benchmark, rebalancing policy and trading cost.
- [x] Risk desk: Sharpe, Sortino, Calmar, VaR/CVaR 95%, beta/alpha, tracking error, information ratio, drawdown, rolling volatility, rolling beta, correlation matrix, risk contribution, return distribution.
- [x] Returns calendar, best/worst periods, rebalance trade planner (EUR and shares) and policy comparison net of costs.
- [x] Beta-based stress scenarios and worst realized windows.
- [x] CPPI historical backtest; Goal Projection model unchanged (output verified identical to v2) plus Monte Carlo goal probability.
- [x] CSV export and print/PDF.

## 7. v3 Fire Drill / shadow mode (branch `feature/v3-fire-drill-20261005`)
- [x] Add a Fire Drill page: crash presets (playbook −70%, 2000–02, 2007–09, 2020, 2022, −75% cascade) and a custom scenario (per-ETF drawdown, months/years to bottom, optional recovery, crash volatility).
- [x] Shadow mode: simulated closes continue from the last real close and replace the data behind every v3 page, with a banner, SIMULATION marker on charts, a day slider, replay, and re-roll.
- [x] Real data, allocation and saved settings are never modified; leaving shadow mode restores them.
- [x] Drill report: drawdown, loss in EUR, time underwater, cash-reserve check (6 months / 3 years), margin-call check, three-question behavioral pre-screen.
