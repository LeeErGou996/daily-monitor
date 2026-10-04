# Dashboard v2 Migration Checklist

## 1. Routing and preservation
- [x] Preserve the current site under `/legacy/` without deleting its functionality.
- [x] Add a visible LEGACY notice with a link to the current site.
- [x] Make the repository root URL redirect to `/v2/`.

## 2. Overview dashboard
- [ ] Keep one normalized comparison chart containing VUAA, XNAS, SEC0, VGWE, and the weighted portfolio.
- [ ] Keep compact market cards for all four ETFs, including SEC0.DE, and show clear last-sync status.
- [ ] Use four-fund allocation controls with default weights VUAA 35% / XNAS 35% / SEC0 20% / VGWE 10%, keeping the total at 100% and persisting settings locally.
- [ ] Backfill SEC0.DE from the portfolio inception date when the stored history does not yet contain the new ticker.

## 3. CPPI correctness
- [x] Treat “Current Portfolio Value” as today’s value directly; do not reapply historical portfolio return.
- [x] Calculate floor, cushion, equity exposure, and cash allocation from the current value.
- [x] Remove wording that implies an absolute floor guarantee.

## 4. Goal projection correctness
- [x] Reject start dates after the available market-history range instead of silently using the first row.
- [x] Detect required-return solutions outside the numerical search interval and report them as out of range.
- [x] Keep the actual-vs-required path and adaptive CAGR calculation.

## 5. UX and release validation
- [x] Add responsive layout for narrow screens.
- [x] Replace “real-time” wording with latest daily market data / last sync.
- [x] Keep methodology sections collapsed by default.
- [ ] Verify SEC0 snapshot data, SEC0 historical backfill, four-asset portfolio calculations, CPPI, TVM, and responsive rendering before publishing.
