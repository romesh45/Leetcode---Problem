# Day 15 — LeetCode Challenge

## 2540. Minimum Common Value

| Field | Details |
|---|---|
| **Difficulty** | Easy |
| **Topics** | Two Pointers · Array · Hash Set · Binary Search |
| **LeetCode Link** | [2540. Minimum Common Value](https://leetcode.com/problems/minimum-common-value/) |

---

## Problem Statement

Given two integer arrays `nums1` and `nums2`, both **sorted in non-decreasing order**, return the **smallest integer** that appears in **both** arrays. If no such integer exists, return `-1`.

A value is "common" if it appears at least once in each array.

---

## Examples

### Example 1

```
Input:  nums1 = [1, 2, 3], nums2 = [2, 4]
Output: 2
```

`2` is in both arrays; no smaller value qualifies.

### Example 2

```
Input:  nums1 = [1, 2, 3, 6], nums2 = [2, 3, 4, 5]
Output: 2
```

Common values are `{2, 3}`; minimum is `2`.

---

## Constraints

- `1 <= nums1.length, nums2.length <= 10⁵`
- `1 <= nums1[i], nums2[j] <= 10⁹`
- Both arrays are sorted non-decreasing.

---

## Intuition

### Exploit the sortedness — two pointers march forward

Both arrays are sorted, so a **merge-style** walk works perfectly:

```
nums1:  [1, 2, 3, 6]
         ↑ i
nums2:  [2, 3, 4, 5]
         ↑ j
```

Compare `nums1[i]` vs `nums2[j]`:
- **Equal** → we found the smallest common value. Both pointers have only ever moved forward through sorted values, so any earlier common value would have already been caught.
- **`nums1[i] < nums2[j]`** → `nums1[i]` is strictly smaller than `nums2[j]` and everything beyond. It can't appear in `nums2[j:]`. Discard it by advancing `i`.
- **`nums1[i] > nums2[j]`** → symmetric; advance `j`.

When either pointer runs off the end without a match, no common value exists → return `-1`.

### Why "first match = minimum"

At any point in the scan, every value at index `< i` in `nums1` and every value at index `< j` in `nums2` has been **proven** to not be common (we only stepped past them because they were strictly smaller than the other array's current candidate). So the **first** equality we encounter is automatically the smallest common value.

### Why not just use a set?

You could convert one array to a set and scan the other:

```python
s = set(nums2)
for v in nums1:
    if v in s:
        return v
return -1
```

This works and is `O(n + m)` time, but uses `O(m)` extra space and **throws away the sortedness** of `nums2`. The two-pointer approach is the same time complexity in `O(1)` extra space — strictly better.

### Why not binary search?

You could iterate `nums1` and binary-search each value in `nums2` → `O(n log m)`. That's worse than two-pointer for most inputs, and only competitive when one array is dramatically larger than the other. Two-pointer is the cleaner default.

---

## Algorithm

```
i, j = 0, 0
while i < len(nums1) and j < len(nums2):
    if nums1[i] == nums2[j]:
        return nums1[i]
    elif nums1[i] < nums2[j]:
        i += 1
    else:
        j += 1
return -1
```

---

## Solution

```python
from typing import List


class Solution:
    def getCommon(self, nums1: List[int], nums2: List[int]) -> int:
        i, j = 0, 0
        n1, n2 = len(nums1), len(nums2)

        while i < n1 and j < n2:
            if nums1[i] == nums2[j]:
                return nums1[i]
            elif nums1[i] < nums2[j]:
                i += 1
            else:
                j += 1

        return -1
```

---

## Complexity Analysis

| | Complexity | Reason |
|---|---|---|
| **Time** | **O(n + m)** | Each pointer advances at most `n` or `m` times; constant work per step |
| **Space** | **O(1)** | Two integer pointers, nothing else |

This is optimal — any algorithm must read each array at least until it finds a match or proves none exists, which is Ω(n + m) in the worst case.

---

## Full Trace — Example 2: `nums1 = [1, 2, 3, 6], nums2 = [2, 3, 4, 5]`

| Step | i | j | nums1[i] | nums2[j] | Comparison | Action |
|:-:|:-:|:-:|:-:|:-:|---|---|
| 1 | 0 | 0 | 1 | 2 | `1 < 2` | `i = 1` |
| 2 | 1 | 0 | 2 | 2 | `2 == 2` | **return 2** ✓ |

Only two comparisons needed. ✓

---

## Full Trace — `nums1 = [1, 2, 3], nums2 = [4, 5, 6]` (no common)

| Step | i | j | nums1[i] | nums2[j] | Comparison | Action |
|:-:|:-:|:-:|:-:|:-:|---|---|
| 1 | 0 | 0 | 1 | 4 | `1 < 4` | `i = 1` |
| 2 | 1 | 0 | 2 | 4 | `2 < 4` | `i = 2` |
| 3 | 2 | 0 | 3 | 4 | `3 < 4` | `i = 3` |
| 4 | — | — | — | — | `i == n1`, exit loop | **return −1** ✓ |

Pointer `i` walks off the end → no common value.

---

## Alternative — Set-Based One-Liner

```python
def getCommon(self, nums1, nums2):
    s = set(nums2)
    return next((v for v in nums1 if v in s), -1)
```

- **Time:** `O(n + m)` — set build is O(m), then O(n) lookups averaging O(1).
- **Space:** `O(m)` extra.

Concise and "just works" — but ignores the sorted structure. Use this when the input isn't sorted; use two pointers when it is.

---

## Alternative — Binary Search

```python
from bisect import bisect_left

def getCommon(self, nums1, nums2):
    for v in nums1:
        i = bisect_left(nums2, v)
        if i < len(nums2) and nums2[i] == v:
            return v
    return -1
```

- **Time:** `O(n log m)`.
- **Space:** `O(1)`.

Slower than two-pointer in general; only attractive when `n` is much smaller than `m`.

---

## Key Insights

| Insight | Explanation |
|---|---|
| **Sortedness lets pointers move one direction only** | Each comparison either finds the answer or eliminates one element. |
| **First match is automatically the minimum** | Both pointers monotonically advance through sorted values; no earlier match was possible. |
| **Two pointers > set > binary search here** | Optimal time and space; cleanly leverages the given structure. |
| **Duplicates don't matter** | The first time both pointers land on the same value, we return it — regardless of multiplicity. |

---

## Edge Cases

| Case | Behavior |
|---|---|
| `nums1 = [1], nums2 = [1]` | Single match immediately → return `1` |
| Disjoint ranges (`[1,2,3]` vs `[4,5,6]`) | Pointer runs off the end → return `-1` |
| One array fully contained in the other | First overlapping value is returned |
| Duplicates in both (`[1,1,2]`, `[2,2,2]`) | First equality wins → return `2` |
| Length-1 arrays | Loop runs at most once |

---

## Approach Tags

`Two Pointers` · `Sorted Arrays` · `Merge Pattern` · `Linear Scan`

---

*Day 15 of the LeetCode Daily Challenge*
