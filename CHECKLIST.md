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
- [ ] Plot Goal Projection on a proportional time axis so daily historical observations and monthly forward points use their true calendar spacing.
- [ ] Mark the boundary between recorded market history and forward required-path projection.
- [ ] Explain negative required CAGR as a contribution-versus-target condition without changing the solver.

## 5. UX and release validation
- [x] Add responsive layout for narrow screens.
- [x] Replace “real-time” wording with latest daily market data / last sync.
- [x] Keep methodology sections collapsed by default.
- [x] Verify SEC0 snapshot data, SEC0 historical backfill, four-asset portfolio calculations, CPPI, TVM, and responsive rendering before publishing. CI data update and GitHub Pages deployment both passed.
- [x] Verify the Goal Projection redesign on desktop and narrow screens, including persisted inputs, solver error states, and chart rendering. Default-parameter regression passed and GitHub Pages build/deploy completed successfully.
- [ ] Verify proportional date spacing, latest-data boundary marker, negative-CAGR explanation, and unchanged numerical outputs before publishing.
