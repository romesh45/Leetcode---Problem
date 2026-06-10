# Day 36 — LeetCode Challenge

## 3689. Maximum Total Subarray Value I

| Field | Details |
|---|---|
| **Difficulty** | Medium |
| **Topics** | Array · Math · Greedy · Observation |
| **LeetCode Link** | [3689. Maximum Total Subarray Value I](https://leetcode.com/problems/maximum-total-subarray-value-i/) |

---

## Problem Statement

Given an integer array `nums` of length `n` and an integer `k`, choose **exactly `k`** non-empty subarrays `nums[l..r]`. Subarrays **may overlap**, and the **same** subarray (same `l` and `r`) **may be chosen multiple times**.

The **value** of a subarray is `max(nums[l..r]) − min(nums[l..r])`. The **total value** is the sum over all `k` chosen subarrays.

Return the **maximum** possible total value.

---

## Examples

### Example 1

```
Input:  nums = [1,3,2], k = 2
Output: 4
```

Pick `[1,3,2]` twice: each has value `3 − 1 = 2` → total `4`.

### Example 2

```
Input:  nums = [4,2,5,1], k = 3
Output: 12
```

Pick a max-value subarray (value `5 − 1 = 4`) three times → total `12`.

---

## Constraints

- `1 <= n == nums.length <= 5·10⁴`
- `0 <= nums[i] <= 10⁹`
- `1 <= k <= 10⁵`

---

## Intuition

### The best single subarray is the whole array

The value of a subarray is `max − min`. For **any** subarray `sub`:

```
max(sub) ≤ globalMax        (a part can't exceed the whole's maximum)
min(sub) ≥ globalMin        (a part can't go below the whole's minimum)
⟹  value(sub) = max(sub) − min(sub) ≤ globalMax − globalMin
```

And the **entire array** achieves `globalMax − globalMin` exactly. So the maximum value any single chosen subarray can contribute is `globalMax − globalMin` — no subarray beats the full array.

### Repetition is allowed, so just repeat the best

The problem explicitly permits overlapping and **duplicate** picks. There's no constraint demanding `k` *distinct* subarrays. So the greedy optimum is to choose the single best subarray (the whole array) all `k` times:

```
answer = k × (globalMax − globalMin)
```

### That's the whole problem

No DP, no heap, no scanning of subarrays — the structure collapses to a one-liner once you spot that the maximum subarray value is a fixed quantity.

---

## Algorithm

```
return k × (max(nums) − min(nums))
```

---

## Solution

```python
from typing import List


class Solution:
    def maxTotalValue(self, nums: List[int], k: int) -> int:
        return k * (max(nums) - min(nums))
```

---

## Complexity Analysis

| | Complexity | Reason |
|---|---|---|
| **Time** | **O(n)** | One pass each for `max` and `min` |
| **Space** | **O(1)** | Two scalars |

> **Overflow note:** the result can reach `10⁵ × 10⁹ = 10¹⁴`, which exceeds 32-bit range. Python handles big ints natively; in Java/C++ use `long`.

---

## Proof of Optimality

**Claim:** `k × (globalMax − globalMin)` is the maximum achievable total.

**Upper bound.** Each of the `k` chosen subarrays contributes at most `globalMax − globalMin` (shown above). Summing `k` terms, the total is at most `k × (globalMax − globalMin)`.

**Achievability.** Choosing the whole array `k` times is legal (repeats allowed) and yields exactly `k × (globalMax − globalMin)`.

Upper bound meets achievability ⇒ it's the maximum. ∎

---

## Worked Verification

| Input | globalMax | globalMin | diff | k | `k × diff` |
|---|:-:|:-:|:-:|:-:|:-:|
| `[1,3,2]` | 3 | 1 | 2 | 2 | **4** ✓ |
| `[4,2,5,1]` | 5 | 1 | 4 | 3 | **12** ✓ |
| `[5]` | 5 | 5 | 0 | 10 | **0** ✓ |
| `[0, 10⁹]` | 10⁹ | 0 | 10⁹ | 10⁵ | **10¹⁴** ✓ |

---

## Looking Ahead — The "II" Version

This problem is labeled **I** because repeats make it trivial. A typical **"II"** variant forbids reuse: you must pick **`k` distinct** subarrays and maximize the sum of their values. That's dramatically harder:

- There are `O(n²)` subarrays, far too many to enumerate when `n = 5·10⁴`.
- You'd want the **`k` largest** subarray values without materializing all of them.
- Standard machinery: a max-heap seeded with candidate ranges, expanded lazily, often combined with **monotonic stacks** (to reason about which subarray extends the current max/min) or **binary search on the answer** plus a counting routine.

None of that is needed here — but it's the natural next step and worth recognizing.

---

## Key Insights

| Insight | Explanation |
|---|---|
| **Max subarray value = `globalMax − globalMin`** | A part can't exceed the whole's max nor undercut its min. |
| **The whole array attains the bound** | So the best single pick is fixed and known immediately. |
| **Repeats allowed ⇒ repeat the best** | No distinctness constraint, so use the top subarray `k` times. |
| **Collapses to one line** | `k × (max − min)`; no search structure required. |
| **Mind the overflow** | Up to `10¹⁴`; use 64-bit ints outside Python. |

---

## Edge Cases

| Case | Behavior |
|---|---|
| Single element (`[5]`) | `max == min` → value `0` regardless of `k` |
| All equal (`[7,7,7]`) | `max − min = 0` → total `0` |
| Two extremes (`[0, 10⁹]`) | `10⁹ × k` |
| Large `k` | Linear scaling, no special handling |
| `k = 1` | Just `globalMax − globalMin` |

---

## Approach Tags

`Math Observation` · `Greedy` · `Global Max/Min` · `Constant-Formula`

---

*Day 36 of the LeetCode Daily Challenge*
