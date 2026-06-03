# Day 30 — LeetCode Challenge

## 3635. Earliest Finish Time for Land and Water Rides II

| Field | Details |
|---|---|
| **Difficulty** | Medium |
| **Topics** | Greedy · Precomputation · Decoupling · Linear Scan |
| **LeetCode Link** | [3635. Earliest Finish Time for Land and Water Rides II](https://leetcode.com/problems/earliest-finish-time-for-land-and-water-rides-ii/) |

---

## Problem Statement

Identical to [Day 29 (LC 3633)](https://leetcode.com/problems/earliest-finish-time-for-land-and-water-rides-i/), but with **much larger inputs**.

There are two ride categories:

- **Land:** `landStartTime[i]` (opening) and `landDuration[i]`.
- **Water:** `waterStartTime[j]` (opening) and `waterDuration[j]`.

A tourist takes **exactly one ride from each category, in either order**. A ride started at `t` finishes at `t + duration`; you may board the second ride as soon as it opens (waiting if necessary). Return the **earliest** time both rides are finished.

---

## Examples

### Example 1

```
Input:  landStartTime = [2,8], landDuration = [4,1],
        waterStartTime = [6],  waterDuration = [3]
Output: 9
```

Land ride 0 → water ride 0: land `2 → 6`, water `6 → 9`.

### Example 2

```
Input:  landStartTime = [5], landDuration = [3],
        waterStartTime = [1], waterDuration = [10]
Output: 14
```

Water ride 0 → land ride 0: water `1 → 11`, land `11 → 14`.

---

## Constraints

- `1 <= n, m <= 5·10⁴`  ← **the difference from "I"**
- `landStartTime.length == landDuration.length == n`
- `waterStartTime.length == waterDuration.length == m`
- `1 <= all values <= 10⁵`

---

## Intuition

### Why the brute force from "I" no longer works

The Easy version (Day 29) tried **all pairs** in O(n·m). Here `n, m ≤ 5·10⁴`, so:

```
n · m  ≈  5·10⁴ × 5·10⁴  =  2.5·10⁹   →  TLE
```

We must drop the pairwise enumeration and get to **O(n + m)**.

### The decoupling insight

Look at the finish time of a **land → water** plan with a fixed water ride `j`:

```
finish = max(landFinish, waterStart[j]) + waterDur[j]
```

The only thing the *land* ride contributes is `landFinish`. And the expression is **monotonically non-decreasing** in `landFinish` — a smaller `landFinish` can never produce a larger finish.

**Consequence:** no matter which water ride you pair with, the best land ride is *always* the one that finishes earliest. The two choices **decouple** — pick the land ride independently (minimize its completion time), then try each water ride.

Symmetrically, for **water → land** plans, the best water ride is the earliest-finishing one.

### The O(n + m) plan

```
best_land_done  = min over land rides  (start + duration)
best_water_done = min over water rides (start + duration)

answer = min(
    min over water rides:  max(best_land_done,  waterStart) + waterDur,   # land → water
    min over land rides:   max(best_water_done, landStart)  + landDur     # water → land
)
```

Three linear passes. No pairs.

---

## Why the Greedy Choice Is Correct

**Claim:** For land → water plans, using `best_land_done = min_i(landStart[i] + landDur[i])` is optimal for *every* water ride.

**Proof.** Fix any water ride `j`. The land→water finish is

```
g(landFinish) = max(landFinish, waterStart[j]) + waterDur[j].
```

`g` is non-decreasing: if `a ≤ b` then `max(a, w) ≤ max(b, w)`, so `g(a) ≤ g(b)`. Therefore `g` is minimized by the smallest possible `landFinish`, which is `best_land_done`. Since this holds for *each* `j` independently, scanning all water rides against the single `best_land_done` finds the optimal land→water plan. The water→land direction is symmetric. ∎

This is exactly why we never need to consider any land ride other than the fastest-finishing one (and likewise for water).

---

## Algorithm

```
best_land_done  = min(landStart[i]  + landDur[i])
best_water_done = min(waterStart[j] + waterDur[j])

ans = ∞
for each water ride (s, d):  ans = min(ans, max(best_land_done,  s) + d)
for each land ride  (s, d):  ans = min(ans, max(best_water_done, s) + d)
return ans
```

---

## Solution

```python
from typing import List


class Solution:
    def earliestFinishTime(
        self,
        landStartTime: List[int],
        landDuration: List[int],
        waterStartTime: List[int],
        waterDuration: List[int],
    ) -> int:
        best_land_done  = min(s + d for s, d in zip(landStartTime,  landDuration))
        best_water_done = min(s + d for s, d in zip(waterStartTime, waterDuration))

        ans = float("inf")
        for s, d in zip(waterStartTime, waterDuration):     # land → water
            ans = min(ans, max(best_land_done, s) + d)
        for s, d in zip(landStartTime, landDuration):       # water → land
            ans = min(ans, max(best_water_done, s) + d)

        return ans
```

---

## Complexity Analysis

| | Complexity | Reason |
|---|---|---|
| **Time** | **O(n + m)** | Two passes to find the minimums + two passes to sweep |
| **Space** | **O(1)** | Two scalars + a running answer |

A `~2.5·10⁹` → `~2·10⁵` operation reduction versus the pairwise approach.

---

## Full Trace — Example 1

`land = {(2,4), (8,1)}`, `water = {(6,3)}`.

**Precompute:**
- `best_land_done  = min(2+4, 8+1) = min(6, 9) = 6`
- `best_water_done = min(6+3) = 9`

**Land → water** (sweep water rides):
- water `(6, 3)`: `max(6, 6) + 3 = 9`

**Water → land** (sweep land rides):
- land `(2, 4)`: `max(9, 2) + 4 = 13`
- land `(8, 1)`: `max(9, 8) + 1 = 10`

`answer = min(9, 13, 10) = 9` ✓

---

## Full Trace — Example 2

`land = {(5,3)}`, `water = {(1,10)}`.

**Precompute:**
- `best_land_done  = 5+3 = 8`
- `best_water_done = 1+10 = 11`

**Land → water:** water `(1,10)`: `max(8, 1) + 10 = 18`
**Water → land:** land `(5,3)`: `max(11, 5) + 3 = 14`

`answer = min(18, 14) = 14` ✓

---

## Comparison with Day 29 (LC 3633, "I")

| Aspect | Day 29 (3633 — "I", Easy) | Day 30 (3635 — "II", Medium) |
|---|---|---|
| Constraints | `n, m ≤ 100` | `n, m ≤ 5·10⁴` |
| Acceptable approach | O(n·m) brute force | Must be O(n + m) |
| Core idea | Try every pair × both orders | Decouple: best-completion per category, sweep once |
| Why it changes | Small inputs forgive quadratic | `2.5·10⁹` pairs would TLE |

Same physics, same finish-time formula — the only thing that changes is that the larger input **forces** the decoupling optimization (which was just a "bonus" note in Day 29).

---

## Validation

The repository's `solution.py` includes a randomized cross-check: it runs the O(n+m) solution against a brute-force O(n·m) reference on 2000 random small inputs and asserts equality. This guards the greedy/decoupling logic against subtle off-by-one or direction mistakes.

```
randomized cross-check passed ✓
```

---

## Key Insights

| Insight | Explanation |
|---|---|
| **Larger input kills the quadratic** | `n, m ≤ 5·10⁴` ⇒ pairwise enumeration TLEs; O(n + m) required. |
| **Finish is monotone in first-ride completion** | `max(finish, open) + dur` only grows with `finish`, so minimize it independently. |
| **Choices decouple** | Best land ride (earliest finish) is optimal against *every* water ride, and vice versa. |
| **Three linear passes suffice** | Two for the minimums, two for the sweeps — no pairs. |
| **Cross-check against brute force** | A randomized harness catches direction/edge bugs the examples miss. |

---

## Edge Cases

| Case | Behavior |
|---|---|
| Single ride in each category | One land→water value + one water→land value; take min |
| Many land rides, one water ride | `best_land_done` collapses all land rides to one number |
| Second ride already open | `max` selects arrival time; no waiting |
| Second ride opens far in the future | `max` selects the open time; tourist waits |
| All rides identical | Both orders give the same finish |

---

## Approach Tags

`Greedy` · `Decoupling` · `Precompute Minimum` · `Linear Scan` · `Monotonicity Argument`

---

*Day 30 of the LeetCode Daily Challenge*
