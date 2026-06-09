# Day 35 — LeetCode Challenge

## 2161. Partition Array According to Given Pivot

| Field | Details |
|---|---|
| **Difficulty** | Medium |
| **Topics** | Array · Two Pointers · Stable Partition · Dutch National Flag |
| **LeetCode Link** | [2161. Partition Array According to Given Pivot](https://leetcode.com/problems/partition-array-according-to-given-pivot/) |

---

## Problem Statement

Given a 0-indexed array `nums` and an integer `pivot`, rearrange `nums` so that:

1. Every element **less than** `pivot` appears **before** every element **greater than** `pivot`.
2. Every element **equal to** `pivot` sits **between** the less-than and greater-than groups.
3. The **relative order** of the less-than elements is preserved, and likewise for the greater-than elements.

Return the rearranged array.

---

## Examples

### Example 1

```
Input:  nums = [9,12,5,10,14,3,10], pivot = 10
Output: [9,5,3,10,10,12,14]
```

- Less than 10: `[9, 5, 3]` (original order kept)
- Equal: `[10, 10]`
- Greater than 10: `[12, 14]` (original order kept)

### Example 2

```
Input:  nums = [-3,4,3,2], pivot = 2
Output: [-3,2,4,3]
```

- Less: `[-3]`, Equal: `[2]`, Greater: `[4, 3]`.

---

## Constraints

- `1 <= nums.length <= 10⁵`
- `-10⁶ <= nums[i] <= 10⁶`
- `pivot` equals some element of `nums`.

---

## Intuition

### A *stable* three-way partition

This is a classic "Dutch National Flag" style partition (`< pivot`, `== pivot`, `> pivot`) — but with an extra twist: the relative order **within** the less-than and greater-than groups must be preserved. That word **stable** rules out the standard in-place swap-based 3-way partition (swaps scramble relative order).

### Bucket while scanning

The cleanest stable approach: a single left-to-right pass that drops each element into one of two lists:

```
less:    elements < pivot   (appended in scan order)
greater: elements > pivot   (appended in scan order)
equal:   just count them    (every pivot value is identical)
```

Because we append in the **same order** we encounter elements, each list naturally preserves the original relative ordering — no extra sorting or index tracking needed.

### Why pivots are merely counted

Every element equal to `pivot` has the *exact same value* (`pivot`). There's no ordering to preserve among identical values, so we don't store them — we just count how many and emit `pivot` that many times in the middle.

### Stitch the result

```
result = less + [pivot] * equal_count + greater
```

All three conditions fall out: smaller-first, pivots in the middle, larger-last, both outer groups order-preserved.

---

## Algorithm

```
less, greater = [], []
equal_count = 0
for x in nums:
    if   x < pivot: less.append(x)
    elif x > pivot: greater.append(x)
    else:           equal_count += 1
return less + [pivot] * equal_count + greater
```

---

## Solution

```python
from typing import List


class Solution:
    def pivotArray(self, nums: List[int], pivot: int) -> List[int]:
        less = []
        greater = []
        equal_count = 0

        for x in nums:
            if x < pivot:
                less.append(x)
            elif x > pivot:
                greater.append(x)
            else:
                equal_count += 1

        return less + [pivot] * equal_count + greater
```

---

## Complexity Analysis

| | Complexity | Reason |
|---|---|---|
| **Time** | **O(n)** | One pass to bucket + O(n) concatenation |
| **Space** | **O(n)** | Output array; the two buckets together hold ≤ n elements |

Optimal — you must read all `n` elements and produce `n` outputs.

---

## Full Trace — Example 1: `nums = [9,12,5,10,14,3,10], pivot = 10`

| x | bucket | `less` | `greater` | `equal_count` |
|:-:|:-:|---|---|:-:|
| 9 | < | `[9]` | `[]` | 0 |
| 12 | > | `[9]` | `[12]` | 0 |
| 5 | < | `[9,5]` | `[12]` | 0 |
| 10 | == | `[9,5]` | `[12]` | 1 |
| 14 | > | `[9,5]` | `[12,14]` | 1 |
| 3 | < | `[9,5,3]` | `[12,14]` | 1 |
| 10 | == | `[9,5,3]` | `[12,14]` | 2 |

**Stitch:** `[9,5,3] + [10,10] + [12,14] = [9,5,3,10,10,12,14]` ✓

---

## Why the In-Place Swap Partition Fails Here

The textbook Dutch National Flag uses three pointers and **swaps** elements in place — O(1) space. But swapping moves elements past each other, **destroying relative order**. Example:

```
nums = [9, 12, 5], pivot = 10
```

A swap-based partition might move `5` before `9` is settled, or reorder `9` and `5` relative to the original. Since the problem *demands* stable order within each group, the swap approach is incorrect here. The bucket method trades O(1) → O(n) space to guarantee stability — a necessary trade-off.

---

## Alternative — Two-Pointer Fill (Order-Aware)

You can avoid building intermediate lists by writing directly into a result array with two indices: a forward pointer for "less" and a backward pointer for "greater", filling greater in **reverse** then reversing that segment. It's fiddlier and doesn't beat the bucket method asymptotically:

```python
def pivotArray(self, nums, pivot):
    n = len(nums)
    res = [pivot] * n
    i, j = 0, n - 1
    # Forward pass fills "less" from the front.
    for x in nums:
        if x < pivot:
            res[i] = x; i += 1
    # Backward pass fills "greater" from the back (preserves order by scanning back).
    for x in reversed(nums):
        if x > pivot:
            res[j] = x; j -= 1
    return res
```

This is a neat one-array variant: the middle is pre-filled with `pivot`, `less` grows from the left, `greater` grows from the right (scanning `nums` in reverse so the back-to-front writes restore original order). Same O(n) time and space, slightly more subtle. The two-list bucket version is the most readable.

---

## Key Insights

| Insight | Explanation |
|---|---|
| **Stability is the catch** | Relative order within "less" and "greater" must be preserved — rules out swap-based partition. |
| **Bucket in scan order** | Appending as you scan automatically maintains relative order. |
| **Count, don't store, pivots** | Equal elements are identical — just emit `pivot × count`. |
| **Concatenate to assemble** | `less + pivots + greater` satisfies all three conditions in one line. |
| **Two-pointer fill is an O(1)-list alternative** | Pre-fill with pivot, grow from both ends; scan reversed for the greater group. |

---

## Edge Cases

| Case | Behavior |
|---|---|
| `nums = [1], pivot = 1` | One pivot, no less/greater → `[1]` |
| All equal to pivot (`[3,3,3]`) | All counted → `[3,3,3]` |
| No elements equal except the guaranteed one | Middle has exactly the pivot occurrences |
| All less than pivot | `greater` empty; result is `less + pivots` |
| All greater than pivot | `less` empty; result is `pivots + greater` |
| Mixed with duplicate pivots (`[5,1,5,1,5]`) | `[1,1] + [5,5,5] = [1,1,5,5,5]` |

---

## Approach Tags

`Stable Partition` · `Bucketing` · `Three-Way Split` · `Order Preservation`

---

*Day 35 of the LeetCode Daily Challenge*
