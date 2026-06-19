# Day 46 — LeetCode Challenge

## 1732. Find the Highest Altitude

| Field | Details |
|---|---|
| **Difficulty** | Easy |
| **Topics** | Array · Prefix Sum · Running Maximum |
| **LeetCode Link** | [1732. Find the Highest Altitude](https://leetcode.com/problems/find-the-highest-altitude/) |

---

## Problem Statement

A biker's trip has `n + 1` points. They start at point `0` with altitude `0`. Given an array `gain` of length `n`, where `gain[i]` is the **net altitude change** from point `i` to point `i + 1`, return the **highest** altitude reached.

---

## Examples

### Example 1

```
Input:  gain = [-5,1,5,0,-7]
Output: 1
```

Altitudes: `[0, -5, -4, 1, 1, -6]` → highest `1`.

### Example 2

```
Input:  gain = [-4,-3,-2,-1,4,3,2]
Output: 0
```

Altitudes: `[0, -4, -7, -9, -10, -6, -3, -1]` → highest is the start, `0`.

---

## Constraints

- `n == gain.length`, `1 <= n <= 100`
- `-100 <= gain[i] <= 100`

---

## Intuition

### Altitudes are a prefix sum

The altitude at point `i + 1` is the start (`0`) plus all the gains up to there:

```
altitude(0)   = 0
altitude(i+1) = gain[0] + gain[1] + … + gain[i]   (a prefix sum)
```

So the answer is the **maximum prefix sum of `gain`**, with the empty prefix (the start point, value `0`) included as a candidate.

### Carry a running sum, not the whole array

We don't need to store every altitude — just sweep once, maintaining the running `altitude` and the best seen.

### Why seed `highest = 0`

Point `0` always has altitude `0`. If every gain is negative (Example 2), the biker only descends, so the highest point *is* the start. Initializing `highest = 0` captures this without a special case — it's the empty-prefix candidate.

---

## Algorithm

```
altitude = 0
highest  = 0                # the start point counts
for g in gain:
    altitude += g
    highest = max(highest, altitude)
return highest
```

---

## Solution

```python
from typing import List


class Solution:
    def largestAltitude(self, gain: List[int]) -> int:
        altitude = 0
        highest = 0
        for g in gain:
            altitude += g
            if altitude > highest:
                highest = altitude
        return highest
```

---

## One-Liner Variant

```python
from itertools import accumulate


class Solution:
    def largestAltitude(self, gain: List[int]) -> int:
        return max(0, *accumulate(gain))
```

`accumulate(gain)` yields the running prefix sums (the altitudes after the start); the leading `0` guards the start point in case all sums are negative.

---

## Complexity Analysis

| | Complexity | Reason |
|---|---|---|
| **Time** | **O(n)** | Single pass over `gain` |
| **Space** | **O(1)** | Two scalars (running sum + best) |

---

## Full Trace — Example 1: `gain = [-5, 1, 5, 0, -7]`

| step | `g` | `altitude` | `highest` |
|:-:|:-:|:-:|:-:|
| start | — | 0 | 0 |
| 1 | -5 | -5 | 0 |
| 2 | 1 | -4 | 0 |
| 3 | 5 | 1 | 1 |
| 4 | 0 | 1 | 1 |
| 5 | -7 | -6 | 1 |

**Answer: 1** ✓

---

## Full Trace — Example 2: `gain = [-4, -3, -2, -1, 4, 3, 2]`

| step | `g` | `altitude` | `highest` |
|:-:|:-:|:-:|:-:|
| start | — | 0 | 0 |
| 1 | -4 | -4 | 0 |
| 2 | -3 | -7 | 0 |
| 3 | -2 | -9 | 0 |
| 4 | -1 | -10 | 0 |
| 5 | 4 | -6 | 0 |
| 6 | 3 | -3 | 0 |
| 7 | 2 | -1 | 0 |

The running altitude never climbs above the start → **0** ✓

---

## Key Insights

| Insight | Explanation |
|---|---|
| **Altitude = prefix sum of gains** | Start at 0; each point's height is the cumulative gain to it. |
| **Answer = max prefix sum (incl. empty)** | The highest point is the largest running total, or 0 if all are negative. |
| **Seed `highest = 0`** | Counts the start point; no special case for all-descending trips. |
| **Running sum beats storing the array** | O(1) space — only the current height and the best matter. |

---

## Edge Cases

| Case | Behavior |
|---|---|
| All negative gains | Never rises above start → `0` |
| All positive gains | Highest is the final point (sum of all) |
| Single gain | Max of `0` and that one altitude |
| Mixed (rise then fall) | Peak captured mid-trip |
| Start is the peak | Returns `0` |

---

## Approach Tags

`Prefix Sum` · `Running Maximum` · `Single Pass` · `Constant Space`

---

*Day 46 of the LeetCode Daily Challenge*
