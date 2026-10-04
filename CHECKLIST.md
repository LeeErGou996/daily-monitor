# Dashboard v2 Migration Checklist

## 1. Routing and preservation
- [x] Preserve the current site under `/legacy/` without deleting its functionality.
- [x] Add a visible LEGACY notice with a link to the current site.
- [x] Make the repository root URL redirect to `/v2/`.

## 2. Overview dashboard
- [x] Replace three stacked price charts with one normalized comparison chart including the weighted portfolio.
- [x] Keep compact ETF market cards and show clear last-sync status.
- [x] Make allocation controls reflect final percentages and persist settings locally.

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
- [x] Verify `/legacy/`, `/v2/`, root redirect, data loading, CPPI, TVM, and responsive CSS before publishing. GitHub Pages deployment completed successfully.
