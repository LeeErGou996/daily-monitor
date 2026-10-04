# Dashboard v2 Migration Checklist

## 1. Routing and preservation
- [ ] Preserve the current site under `/legacy/` without deleting its functionality.
- [ ] Add a visible LEGACY notice with a link to the current site.
- [ ] Make the repository root URL redirect to `/v2/`.

## 2. Overview dashboard
- [ ] Replace three stacked price charts with one normalized comparison chart including the weighted portfolio.
- [ ] Keep compact ETF market cards and show clear last-sync status.
- [ ] Make allocation controls reflect final percentages and persist settings locally.

## 3. CPPI correctness
- [ ] Treat “Current Portfolio Value” as today’s value directly; do not reapply historical portfolio return.
- [ ] Calculate floor, cushion, equity exposure, and cash allocation from the current value.
- [ ] Remove wording that implies an absolute floor guarantee.

## 4. Goal projection correctness
- [ ] Reject start dates after the available market-history range instead of silently using the first row.
- [ ] Detect required-return solutions outside the numerical search interval and report them as out of range.
- [ ] Keep the actual-vs-required path and adaptive CAGR calculation.

## 5. UX and release validation
- [ ] Add responsive layout for narrow screens.
- [ ] Replace “real-time” wording with latest daily market data / last sync.
- [ ] Keep methodology sections collapsed by default.
- [ ] Verify `/legacy/`, `/v2/`, root redirect, data loading, CPPI, TVM, and responsive CSS before publishing.
