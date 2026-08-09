# 1140. Stone Game II

**Difficulty:** Medium
**Topics:** Array, Math, Dynamic Programming, Prefix Sum, Game Theory
**Link:** https://leetcode.com/problems/stone-game-ii/

## Problem

There are `piles.length` piles of stones arranged in a row, `piles[i]` stones
in the i-th pile. Alice and Bob alternate turns, Alice first. On a turn, the
player takes all stones from the first `X` remaining piles, where
`1 <= X <= 2M`, and then `M = max(M, X)`. `M` starts at 1. The game ends when
all stones are taken. Both players play optimally to maximize their own
total. Return the maximum number of stones Alice can end up with.

## Approach: Top-Down DP over (index, M)

### Key Observation

The state of the game is fully described by:
- `i`: index of the first remaining pile (piles are always taken from the
  front, so the remaining piles are always a suffix)
- `m`: the current value of `M`, which controls the max number of piles the
  current player may take (`1 <= X <= 2m`)

Define `dp(i, m)` as the maximum number of stones the player **whose turn it
is** can collect from `piles[i:]`, given the current `M = m`.

### Recurrence

For a chosen move `X = x` (with `1 <= x <= 2m`), the current player takes
piles `[i, i+x)`, then it becomes the opponent's turn with the new state
`(i + x, max(m, x))`. Since the total stones left in the suffix is
`suffix_sum[i]`, and the opponent will play optimally to maximize their own
share `dp(i + x, max(m, x))` from that point on, the current player's
resulting total for that choice is:

```
suffix_sum[i] - dp(i + x, max(m, x))
```

The current player picks the `x` that maximizes this value:

```
dp(i, m) = max over x in [1, 2m], i+x <= n of:
               suffix_sum[i] - dp(i + x, max(m, x))
```

### Base Case (early termination)

If `i + 2m >= n`, the current player can take **all** remaining piles in one
move (since `X` can go up to `2m`, which covers everything left). So:

```
dp(i, m) = suffix_sum[i]   when i + 2m >= n
```

This base case is essential for both correctness and performance -- without
it the state space would still be correct but this closed form lets us stop
recursing immediately once a player can sweep the rest of the board.

### Answer

`dp(0, 1)` is the maximum Alice can collect, since the game starts at index 0
with `M = 1` and it is Alice's turn.

### Suffix Sums

`suffix_sum[i]` (total stones in `piles[i:]`) is precomputed once in O(n) so
that each transition is O(1) besides the branching factor of `x`.

## Complexity

- **Time:** O(n^2) states `(i, m)` since `m` ranges up to `n`, each with up
  to O(n) choices of `x` in the worst case, giving O(n^3) in the absolute
  worst case; however because of the early-termination base case, `m` never
  needs to exceed `n`, and in practice the effective state space explored is
  small since `M` doubles quickly and most states hit the base case. The
  standard accepted bound for this DP is **O(n^3)** worst case, which is
  fine for `n <= 100`.
- **Space:** O(n^2) for the memoization cache (`i` and `m` both bounded by
  `n`), plus O(n) for the suffix sum array.

## Example Walkthrough

`piles = [2,7,9,4,4]`

- Alice takes 1 pile (`2`), M becomes 1 (X=1 <= 2*1).
- Bob takes 2 piles (`7+9=16`)... but playing optimally, the actual optimal
  line has Alice take 1 pile, Bob take 2 piles, then Alice take the
  remaining 2 piles: `2 + 4 + 4 = 10`.
- Output: `10`

`piles = [1,2,3,4,5,100]`

- Optimal play lets Alice secure the pile of `100` plus enough small piles
  to reach `104`.
- Output: `104`

## Notes

- This is a classic minimax game-theory DP: instead of tracking both
  players' scores directly, we track "whoever moves now gets
  `total_remaining - best_the_opponent_can_do_after`," which cleanly
  captures optimal adversarial play with a single recurrence.
- `functools.lru_cache` is used for memoization on `(i, m)`; the cache is
  cleared after use so repeated calls to `stoneGameII` on different inputs
  do not leak stale state.
