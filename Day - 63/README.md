# Day 60 — LeetCode Challenge

## 1288. Remove Covered Intervals

| Field | Details |
|---|---|
| **Difficulty** | Medium |
| **Topics** | Array · Greedy · Sorting |
| **LeetCode Link** | [1288. Remove Covered Intervals](https://leetcode.com/problems/remove-covered-intervals/) |

---

## Problem Statement

Given an array of intervals `[li, ri]`, remove every interval covered by another. Interval `[a, b]` is covered by `[c, d]` if `c <= a` and `b <= d`. Return the count of remaining intervals.

---

## Examples

### Example 1
```
Input:  intervals = [[1,4],[3,6],[2,8]]
Output: 2
```
`[3,6]` is covered by `[2,8]` → removed. `[1,4]` and `[2,8]` remain.

### Example 2
```
Input:  intervals = [[1,4],[2,3]]
Output: 1
```
`[2,3]` is covered by `[1,4]` → removed.

---

## Constraints

- `1 <= intervals.length <= 1000`
- `0 <= li < ri <= 10⁵`
- All intervals are unique

---

## Intuition

### Coverage condition

`[a, b]` is covered by `[c, d]` iff `c <= a` **and** `b <= d` — both the left and right endpoints are dominated.

### Sort to handle left automatically

Sort by **left ascending, right descending**. After sorting, every interval we've already processed has `left <= current.left`. That satisfies the left-side coverage condition for free — we never need to check it again.

This reduces the problem to: is there any previously seen interval whose `right >= current.right`? Tracking a running `max_right` answers this in O(1) per step.

### Why right descending on ties

When two intervals share the same left, the wider one must come first. Example: `[1,6]` before `[1,4]`. After processing `[1,6]`, `max_right = 6 >= 4`, so `[1,4]` is correctly identified as covered. If we processed `[1,4]` first, `max_right = 4` and `[1,6]` would incorrectly look uncovered — but `[1,6]` isn't covered by `[1,4]`, so that part would be fine. The real problem is `[1,4]` wouldn't be seen as covered. The descending-right sort fixes this.

---

## Algorithm

```
Sort intervals by (left asc, right desc)

remaining = 0
max_right = 0

for (l, r) in sorted intervals:
    if r > max_right:
        remaining += 1
        max_right = r
    # else: covered by a previous interval

return remaining
```

---

## Solution

```python
from typing import List


class Solution:
    def removeCoveredIntervals(self, intervals: List[List[int]]) -> int:
        intervals.sort(key=lambda x: (x[0], -x[1]))

        remaining = 0
        max_right = 0

        for l, r in intervals:
            if r > max_right:
                remaining += 1
                max_right = r

        return remaining
```

---

## Complexity Analysis

| | Complexity | Reason |
|---|---|---|
| **Time** | **O(n log n)** | Sort dominates; sweep is O(n) |
| **Space** | **O(1)** | Two variables, in-place sort |

---

## Full Trace — Example 1: `[[1,4],[3,6],[2,8]]`

After sort `(left asc, right desc)`: `[[1,4],[2,8],[3,6]]`

| Interval | r > max_right? | remaining | max_right |
|:-:|:-:|:-:|:-:|
| [1,4] | 4 > 0 ✓ | 1 | 4 |
| [2,8] | 8 > 4 ✓ | 2 | 8 |
| [3,6] | 6 > 8? ✗ | 2 | 8 |

**Answer: 2** ✓ — `[3,6]` covered by `[2,8]`.

---

## Full Trace — Tie-breaking: `[[1,4],[1,6],[1,8]]`

After sort `(left asc, right desc)`: `[[1,8],[1,6],[1,4]]`

| Interval | r > max_right? | remaining | max_right |
|:-:|:-:|:-:|:-:|
| [1,8] | 8 > 0 ✓ | 1 | 8 |
| [1,6] | 6 > 8? ✗ | 1 | 8 |
| [1,4] | 4 > 8? ✗ | 1 | 8 |

**Answer: 1** ✓ — `[1,6]` and `[1,4]` both covered by `[1,8]`.

---

## Key Insights

| Insight | Explanation |
|---|---|
| **Sort left asc** | After sorting, left-side coverage is guaranteed for all previous intervals |
| **Sort right desc on ties** | Wider interval processed first; narrower ones immediately seen as covered |
| **Track max_right** | Only the right endpoint needs checking; max_right captures the best cover so far |
| **r > max_right = uncovered** | Strict `>` because coverage requires `b <= d` (not strict) |

---

## Approach Tags

`Greedy` · `Sorting` · `Interval Coverage` · `Single Pass`

---

*Day 60 of the LeetCode Daily Challenge*
