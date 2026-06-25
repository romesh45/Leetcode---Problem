# Day 51 — LeetCode Challenge

## 3737. Count Subarrays With Majority Element I

| Field | Details |
|---|---|
| **Difficulty** | Medium |
| **Topics** | Array · Prefix Sum · Hash Map |
| **LeetCode Link** | [3737. Count Subarrays With Majority Element I](https://leetcode.com/problems/count-subarrays-with-majority-element-i/) |

---

## Problem Statement

Given an integer array `nums` and an integer `target`, return the number of subarrays in which `target` is the **majority element** — i.e., it appears **strictly more than half** the time.

---

## Examples

### Example 1
```
Input:  nums = [1,2,2,3], target = 2
Output: 5
```
Valid subarrays: `[2]`, `[2]`, `[2,2]`, `[1,2,2]`, `[2,2,3]`.

### Example 2
```
Input:  nums = [1,1,1,1], target = 1
Output: 10
```
All 10 subarrays have `1` as the majority element.

### Example 3
```
Input:  nums = [1,2,3], target = 4
Output: 0
```
`target` never appears → no valid subarrays.

---

## Constraints

- `1 <= nums.length <= 1000`
- `1 <= nums[i] <= 10⁹`
- `1 <= target <= 10⁹`

---

## Intuition

### Reformulating majority

`target` is the majority in `nums[i..j]` means:

```
count(target) > (j - i + 1) / 2
```

which is equivalent to:

```
count(target) > count(non-target)
count(target) - count(non-target) > 0
```

### The ±1 mapping

Map every element to `+1` (if it equals `target`) or `−1` (otherwise). Call this `mapped[]`.

The sum of `mapped[i..j]` equals `count(target) − count(non-target)` in that window. So:

```
target is majority in nums[i..j]  ⟺  sum(mapped[i..j]) > 0
```

### Reducing to prefix sums

Define:
```
prefix[0] = 0
prefix[k] = mapped[0] + mapped[1] + … + mapped[k-1]
```

Then:
```
sum(mapped[i..j]) = prefix[j+1] - prefix[i]
```

The condition becomes:
```
prefix[j+1] - prefix[i] > 0  ⟺  prefix[j+1] > prefix[i]
```

**For each right endpoint `j`, count how many left endpoints `i ∈ [0, j]` satisfy `prefix[i] < prefix[j+1]`.**

With `n ≤ 1000`, an `O(n²)` double loop over all pairs is entirely within limits (at most 10⁶ comparisons).

---

## Algorithm

```
Build prefix[0..n] from ±1 mapped array.

count = 0
for j in 0..n-1:
    for i in 0..j:
        if prefix[j+1] > prefix[i]:
            count += 1

return count
```

---

## Solution

```python
from typing import List


class Solution:
    def countSubarrays(self, nums: List[int], target: int) -> int:
        n = len(nums)

        prefix = [0] * (n + 1)
        for i in range(n):
            prefix[i + 1] = prefix[i] + (1 if nums[i] == target else -1)

        count = 0
        for j in range(n):
            pj = prefix[j + 1]
            for i in range(j + 1):
                if pj > prefix[i]:
                    count += 1

        return count
```

---

## Complexity Analysis

| | Complexity | Reason |
|---|---|---|
| **Time** | **O(n²)** | Double loop over all (i, j) pairs; `n ≤ 1000` → ≤ 10⁶ ops |
| **Space** | **O(n)** | Prefix sum array of length `n + 1` |

---

## Full Trace — Example 1: `nums = [1,2,2,3], target = 2`

**Mapped:** `[-1, +1, +1, -1]`

**Prefix:** `[0, -1, 0, 1, 0]`

| j | prefix[j+1] | i values with prefix[i] < prefix[j+1] | subarrays counted |
|:-:|:-:|:-:|:-:|
| 0 | −1 | none (only prefix[0]=0, not < −1) | 0 |
| 1 | 0 | i=0: prefix[0]=0? No. i=1: prefix[1]=−1 < 0 ✓ | 1 → `[2]` |
| 2 | 1 | i=0: 0<1 ✓, i=1: −1<1 ✓, i=2: 0<1 ✓ | 3 → `[2,2]`,`[1,2,2]`,`[2]` |
| 3 | 0 | i=1: −1<0 ✓ | 1 → `[2,2,3]` |

**Total: 0 + 1 + 3 + 1 = 5** ✓

---

## Full Trace — Example 2: `nums = [1,1,1,1], target = 1`

**Mapped:** `[+1, +1, +1, +1]`

**Prefix:** `[0, 1, 2, 3, 4]`

Every subarray `[i..j]` gives `prefix[j+1] - prefix[i] = (j-i+1) > 0`. So all `n(n+1)/2 = 10` subarrays are valid. **Answer: 10** ✓

---

## Why the Prefix Difference Captures Majority Exactly

For subarray `nums[i..j]` of length `L = j - i + 1`:

| Count of target | Count of non-target | mapped sum | majority? |
|:-:|:-:|:-:|:-:|
| 3 | 2 | +1 | ✓ (3 > 2.5) |
| 2 | 2 | 0 | ✗ (not strictly more) |
| 1 | 4 | −3 | ✗ |

`mapped sum > 0` captures the strict inequality precisely — no edge cases around "exactly half."

---

## Edge Cases

| Case | Behaviour |
|---|---|
| Target not in array | All prefix differences ≤ 0 → returns 0 |
| Single element = target | `prefix[1] = 1 > 0 = prefix[0]` → counted |
| All elements = target | All `n(n+1)/2` subarrays valid |
| All elements ≠ target | All prefix differences ≤ 0 → returns 0 |
| Alternating `[t, x, t, x, …]` | Only odd-length subarrays starting with `t` qualify |

---

## Key Insights

| Insight | Explanation |
|---|---|
| **Majority ↔ count gap > 0** | Rewrite `count > length/2` as `count(target) − count(non-target) > 0` |
| **±1 mapping linearises it** | Sum of mapped window = count gap; direct prefix-sum query |
| **prefix[j+1] > prefix[i]** | Standard "count pairs with prefix sum condition" pattern |
| **O(n²) sufficient** | `n ≤ 1000`; no need for a BIT or merge sort to count inversions |

---

## Approach Tags

`Prefix Sum` · `±1 Encoding` · `Majority Element` · `Subarray Count`

---

*Day 51 of the LeetCode Daily Challenge*
