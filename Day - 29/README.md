# Day 29 — LeetCode Challenge

## 3633. Earliest Finish Time for Land and Water Rides I

| Field | Details |
|---|---|
| **Difficulty** | Easy |
| **Topics** | Array · Brute Force · Enumeration · Greedy |
| **LeetCode Link** | [3633. Earliest Finish Time for Land and Water Rides I](https://leetcode.com/problems/earliest-finish-time-for-land-and-water-rides-i/) |

---

## Problem Statement

There are two categories of rides:

- **Land rides:** `landStartTime[i]` (earliest boarding time) and `landDuration[i]` (length).
- **Water rides:** `waterStartTime[j]` and `waterDuration[j]`.

A tourist must take **exactly one ride from each category**, in **either order**. Rules:

- A ride can start at its opening time or any later moment.
- Starting at time `t`, it finishes at `t + duration`.
- Immediately after finishing one ride, the tourist may board the other (if open) or wait until it opens.

Return the **earliest possible time** to finish both rides.

---

## Examples

### Example 1

```
Input:  landStartTime = [2,8], landDuration = [4,1],
        waterStartTime = [6],  waterDuration = [3]
Output: 9
```

Best plan (land ride 0 → water ride 0): land `2 → 6`, water opens at `6`, start at `6 → 9`. Finish `9`.

### Example 2

```
Input:  landStartTime = [5], landDuration = [3],
        waterStartTime = [1], waterDuration = [10]
Output: 14
```

Best plan (water ride 0 → land ride 0): water `1 → 11`, land opened at `5`, start at `11 → 14`. Finish `14`.

---

## Constraints

- `1 <= n, m <= 100`
- `landStartTime.length == landDuration.length == n`
- `waterStartTime.length == waterDuration.length == m`
- `1 <= all values <= 1000`

---

## Intuition

### The finish-time formula for a fixed pair

Pick land ride `i` and water ride `j`. Two possible orders:

**Land then water:**
```
finish land at    : landStart[i] + landDur[i]
board water at    : max(that, waterStart[j])      ← wait if water not open yet
finish at         : max(landStart[i] + landDur[i], waterStart[j]) + waterDur[j]
```

**Water then land:**
```
finish water at   : waterStart[j] + waterDur[j]
board land at     : max(that, landStart[i])       ← wait if land not open yet
finish at         : max(waterStart[j] + waterDur[j], landStart[i]) + landDur[i]
```

The **`max`** is the key piece — it models *waiting* for the second ride to open if you arrive before its start time.

### Brute force over all pairs

With `n, m ≤ 100`, there are at most `10⁴` `(land, water)` pairs. For each, compute both order finish times and keep the global minimum. Trivially fast.

### Why both orders must be tried

Order matters because waiting is asymmetric. In Example 1, land→water finishes at `9`, but water→land (for the same rides) finishes at `13`. Neither order dominates universally — it depends on the start times and durations — so we evaluate both per pair.

---

## Algorithm

```
best = ∞
for each land ride i:
    land_done = landStart[i] + landDur[i]
    for each water ride j:
        water_done = waterStart[j] + waterDur[j]
        f1 = max(land_done, waterStart[j]) + waterDur[j]   # land → water
        f2 = max(water_done, landStart[i]) + landDur[i]    # water → land
        best = min(best, f1, f2)
return best
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
        best = float("inf")

        for i in range(len(landStartTime)):
            land_done = landStartTime[i] + landDuration[i]
            for j in range(len(waterStartTime)):
                water_done = waterStartTime[j] + waterDuration[j]
                f1 = max(land_done, waterStartTime[j]) + waterDuration[j]
                f2 = max(water_done, landStartTime[i]) + landDuration[i]
                best = min(best, f1, f2)

        return best
```

---

## Complexity Analysis

| | Complexity | Reason |
|---|---|---|
| **Time** | **O(n · m)** | Every pair × 2 orders, constant work each (≤ 10⁴ pairs) |
| **Space** | **O(1)** | Just a running minimum |

---

## Full Trace — Example 1

`land = {(2,4), (8,1)}`, `water = {(6,3)}`.

| Pair (i, j) | `land_done` | `water_done` | f1 (land→water) | f2 (water→land) |
|---|:-:|:-:|---|---|
| (0, 0) | `2+4=6` | `6+3=9` | `max(6,6)+3 = 9` | `max(9,2)+4 = 13` |
| (1, 0) | `8+1=9` | `6+3=9` | `max(9,6)+3 = 12` | `max(9,8)+1 = 10` |

Minimum over all = `min(9, 13, 12, 10)` = **9** ✓ (achieved by land ride 0 → water ride 0).

---

## Full Trace — Example 2

`land = {(5,3)}`, `water = {(1,10)}`.

| Pair | `land_done` | `water_done` | f1 (land→water) | f2 (water→land) |
|---|:-:|:-:|---|---|
| (0, 0) | `5+3=8` | `1+10=11` | `max(8,1)+10 = 18` | `max(11,5)+3 = 14` |

Minimum = `min(18, 14)` = **14** ✓ (water ride 0 → land ride 0).

---

## Bonus — O(n + m) Linear Variant

The two orders **decouple**, so we don't actually need all pairs:

- For **land → water**: only the *earliest land completion time* matters (we want to be done with land ASAP), combined with each water ride. So precompute `best_land_done = min(landStart[i] + landDur[i])`, then for each water ride compute `max(best_land_done, waterStart[j]) + waterDur[j]`.
- Symmetric for **water → land**.

```python
def earliestFinishTime(self, landStart, landDur, waterStart, waterDur):
    best_land_done  = min(s + d for s, d in zip(landStart,  landDur))
    best_water_done = min(s + d for s, d in zip(waterStart, waterDur))

    ans = float("inf")
    for s, d in zip(waterStart, waterDur):     # land → water
        ans = min(ans, max(best_land_done, s) + d)
    for s, d in zip(landStart, landDur):       # water → land
        ans = min(ans, max(best_water_done, s) + d)
    return ans
```

- **Time:** O(n + m); **Space:** O(1).
- For the "I" (Easy) constraints both are instant, but this is the scaling pattern that the harder "II" version demands.

**Why the decoupling is valid:** in a land→water plan, the water ride's finish is `max(landFinish, waterStart) + waterDur`, which is *monotonically non-decreasing* in `landFinish`. So minimizing `landFinish` independently can never hurt — the best land ride to pair with *any* water ride is always the one that finishes earliest.

---

## Key Insights

| Insight | Explanation |
|---|---|
| **`max(arrival, open)` models waiting** | You can't board before the ride opens; the max captures the idle wait. |
| **Both orders per pair** | Order isn't symmetric — waiting differs by direction, so try land-first and water-first. |
| **Brute force suffices for "I"** | `n, m ≤ 100` ⇒ ≤ 10⁴ pairs ⇒ trivial. |
| **Orders decouple ⇒ O(n+m) possible** | The best first-category ride is always the earliest-finishing one, independent of the second ride. |

---

## Edge Cases

| Case | Behavior |
|---|---|
| Single land + single water ride | One pair, two orders evaluated |
| Second ride already open on arrival | `max` picks the arrival time; no waiting |
| Second ride opens much later | `max` picks the open time; tourist waits |
| All rides start at time 1 | Finish = sum of the two shortest durations (plus minimal waiting) |
| Very long first ride | The other order (short ride first) often wins |

---

## Approach Tags

`Brute Force Enumeration` · `Both-Order Evaluation` · `Wait Modeling (max)` · `Decoupling Optimization`

---

*Day 29 of the LeetCode Daily Challenge*
