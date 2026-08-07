# 3348. Smallest Divisible Digit Product II (Hard)

## Idea

Digits 1-9 only ever contribute primes {2,3,5,7} to a product. So:

1. Factor `t = 2^a * 3^b * 5^c * 7^d * r`. If `r != 1`, no zero-free number's digit
   product can ever be divisible by `t` → return `"-1"` immediately.
2. Everything else reduces to: find the lexicographically/numerically smallest
   zero-free string `S >= num` whose digit product covers deficiency `(a,b,c,d)`.

**Key state-space fact:** since `t <= 10^14`, the exponents `a,b,c,d` are individually
small (`a<=46, b<=29, c<=20, d<=16`), and — because `2^a*3^b*5^c*7^d <= t` couples them —
they can't all be near-max simultaneously. The true worst-case state space
`(a+1)(b+1)(c+1)(d+1)` (found via Lagrange balancing) is only a few thousand, not
the ~500K a naive per-axis bound suggests. That's what makes an exact DP tractable
even though `num` can be 2·10^5 digits long.

**`dist[a2,b2,c2,d2]`** = min number of digits (2-9; digit 1 is a no-op) needed to
cover deficiency `(a2,b2,c2,d2)`. Computed once via DP: process states in
increasing coordinate order (a2 outer → d2 inner); every transition from a digit
strictly decreases at least one coordinate, so all dependencies are already
computed when needed.

**Same-length search:** enumerate the break point `j` from `n` down to `0`
(`j=n` = "S equals num exactly"). For each `j`, the prefix `num[0..j-1]` must be
zero-free (bounded by the index of num's first `'0'`, if any), and we place the
smallest digit `> num[j]` such that the remaining `m = n-1-j` slots can still
cover the leftover deficiency (checked via `dist[...] <= m`, O(1) lookup). The
**first** feasible `(j, digit)` found scanning `j` descending gives the smallest
valid number — longer prefix match always beats a shorter one. Suffix is then
built greedily left-to-right, placing the smallest digit at each position that
keeps the remainder feasible.

**Longer-number fallback:** if no length-`n` candidate works, the answer has
length `L = max(n+1, dist[a,b,c,d])` and is just the greedy build from scratch
(mostly `1`s with a minimal tail of larger digits) — always exists once step 1
passes.

## Complexity
- Precompute: `O(states * 8)`, states ≈ a few thousand in the worst case over
  all `t <= 10^14`.
- Main scan + suffix build: `O(n)` (each position tries ≤ 9 digits, O(1) lookup).

Tested: examples pass, brute-force cross-check on random small cases (0 mismatches
over 300 trials), and a 200,000-digit stress test runs in ~0.25s.

## Files
- `solution.py` — `Solution.smallestNumber(num, t)`
