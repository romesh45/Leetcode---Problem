# Day 54 — LeetCode Challenge

## 1846. Maximum Element After Decreasing and Rearranging

| Field | Details |
|---|---|
| **Difficulty** | Medium |
| **Topics** | Array · Greedy · Sorting |
| **LeetCode Link** | [1846. Maximum Element After Decreasing and Rearranging](https://leetcode.com/problems/maximum-element-after-decreasing-and-rearranging/) |

---

## Problem Statement

Given an array of positive integers `arr`, perform any number of these operations:

- **Decrease** any element to a smaller positive integer.
- **Rearrange** elements in any order.

The resulting array must satisfy:
- `arr[0] == 1`
- `abs(arr[i] - arr[i-1]) <= 1` for all `i ≥ 1`

Return the **maximum possible value** of any element after satisfying these conditions.

---

## Examples

### Example 1
```
Input:  arr = [2,2,1,2,1]
Output: 2
```
Rearrange to `[1,2,2,2,1]` — adjacent differences all ≤ 1.

### Example 2
```
Input:  arr = [100,1,1000]
Output: 3
```
Rearrange to `[1,100,1000]`, decrease to `[1,2,3]`.

### Example 3
```
Input:  arr = [1,2,3,4,5]
Output: 5
```
Already valid as-is.

---

## Constraints

- `1 <= arr.length <= 10⁵`
- `1 <= arr[i] <= 10⁹`

---

## Intuition

### What the constraints really allow

Since we can **rearrange freely** and only **decrease** (never increase), the question becomes: what is the best sequence we can build from the available values?

To maximise the largest element, we want the sequence to climb as steeply as possible. The steepest valid climb is `1, 2, 3, 4, …` — increasing by exactly 1 each step.

Position `i` (1-indexed) can hold **at most value `i`** (since we start at 1 and can increase by at most 1 per step). The element at position `i` also cannot exceed its **original value** (we can only decrease).

So the value at position `i` is bounded by `min(original_value, i)`.

### Greedy on sorted array

**Sort ascending.** Then process values one by one, tracking `cur` (the value we just placed):

```
cur = min(v, cur + 1)
```

- `cur + 1`: fastest we can grow from the previous position.
- `v`: the original value caps what we can place.

**Why sorting is optimal:** A small value can only block upward progress. Processing small values early lets us place them at low positions where they belong (or where they're forced anyway), leaving large values for later positions where growth is only limited by `+1` per step.

**Why greedy works:** At each step, placing the maximum possible value (`min(v, cur + 1)`) never hurts future positions — it either keeps pace or stays below the optimal climb, but a higher `cur` only opens more possibilities later.

---

## Algorithm

```
Sort arr in ascending order.

cur = 0
for v in arr:
    cur = min(v, cur + 1)

return cur
```

---

## Solution

```python
from typing import List


class Solution:
    def maximumElementAfterDecrementingAndRearranging(self, arr: List[int]) -> int:
        arr.sort()
        cur = 0
        for v in arr:
            cur = min(v, cur + 1)
        return cur
```

---

## Complexity Analysis

| | Complexity | Reason |
|---|---|---|
| **Time** | **O(n log n)** | Sort dominates; single pass is O(n) |
| **Space** | **O(1)** | In-place sort, one variable |

---

## Full Trace — Example 1: `arr = [2,2,1,2,1]`

Sorted: `[1, 1, 2, 2, 2]`

| v | cur = min(v, cur+1) | cur |
|:-:|:-:|:-:|
| 1 | min(1, 0+1) = 1 | 1 |
| 1 | min(1, 1+1) = 1 | 1 |
| 2 | min(2, 1+1) = 2 | 2 |
| 2 | min(2, 2+1) = 2 | 2 |
| 2 | min(2, 2+1) = 2 | 2 |

**Answer: 2** ✓ — the second `1` acts as a ceiling, blocking growth past 1 until a `2` arrives.

---

## Full Trace — Example 2: `arr = [100,1,1000]`

Sorted: `[1, 100, 1000]`

| v | cur = min(v, cur+1) | cur |
|:-:|:-:|:-:|
| 1 | min(1, 0+1) = 1 | 1 |
| 100 | min(100, 1+1) = 2 | 2 |
| 1000 | min(1000, 2+1) = 3 | 3 |

**Answer: 3** ✓ — the large values are unconstrained; growth is limited to `+1` per step.

---

## Full Trace — Example 3: `arr = [1,2,3,4,5]`

Sorted: `[1, 2, 3, 4, 5]`

| v | cur = min(v, cur+1) | cur |
|:-:|:-:|:-:|
| 1 | min(1, 1) = 1 | 1 |
| 2 | min(2, 2) = 2 | 2 |
| 3 | min(3, 3) = 3 | 3 |
| 4 | min(4, 4) = 4 | 4 |
| 5 | min(5, 5) = 5 | 5 |

**Answer: 5** ✓ — perfectly balanced; `v` and `cur+1` are always equal.

---

## Why `min(arr[-1], n)` Is Wrong

A tempting shortcut: after sorting, return `min(arr[-1], n)`. This works for most cases but fails when small values create a bottleneck mid-array.

Counter-example: `arr = [1, 1, 1, 100]`, `n = 4`.

- `min(100, 4) = 4` — **wrong**.
- Sorted trace: `cur` = 1, 1, 1, 2 → **answer = 2**.

The three `1`s mean the sequence can only reach `1, 1, 1, 2`. The `100` can only contribute `cur + 1 = 2` because its predecessor is capped at 1.

---

## Edge Cases

| Case | Behaviour |
|---|---|
| Single element | `cur = min(v, 1) = 1` always |
| All equal (e.g. `[5,5,5,5,5]`) | `cur` climbs 1,2,3,4,5 — answer = 5 |
| All 1s (e.g. `[1,1,1,1]`) | `cur` stays at 1 throughout — answer = 1 |
| Already sorted 1…n | `cur` tracks exactly — answer = n |
| Huge values, small n | Growth capped at n — answer = n |

---

## Key Insights

| Insight | Explanation |
|---|---|
| **Rearrange + decrease only** | We can build any non-decreasing sequence up to the original values |
| **Optimal shape is 1,2,3,…** | Steepest valid climb maximises the last element |
| **Sort then greedy** | Small values placed first; each step bounded by `min(v, cur+1)` |
| **Single bottleneck dominates** | One cluster of small values caps growth for all later elements |

---

## Approach Tags

`Greedy` · `Sorting` · `Single Pass`

---

*Day 54 of the LeetCode Daily Challenge*
