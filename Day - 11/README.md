# Day 11 — LeetCode Challenge

## 153. Find Minimum in Rotated Sorted Array

| Field | Details |
|---|---|
| **Difficulty** | Medium |
| **Topics** | Binary Search · Array · Divide and Conquer |
| **LeetCode Link** | [153. Find Minimum in Rotated Sorted Array](https://leetcode.com/problems/find-minimum-in-rotated-sorted-array/) |

---

## Problem Statement

A sorted ascending array of length `n` with **unique** elements is rotated between `1` and `n` times. Rotating once turns `[a₀, a₁, …, a_{n-1}]` into `[a_{n-1}, a₀, a₁, …, a_{n-2}]`.

Examples of rotations of `[0, 1, 2, 4, 5, 6, 7]`:
- `[4, 5, 6, 7, 0, 1, 2]` — rotated 4 times
- `[0, 1, 2, 4, 5, 6, 7]` — rotated 7 times (back to original)

Given the rotated array `nums`, return its **minimum** element.

> **Required:** the algorithm must run in **O(log n)** time.

---

## Examples

### Example 1

```
Input:  nums = [3, 4, 5, 1, 2]
Output: 1
```

Original `[1, 2, 3, 4, 5]` rotated 3 times.

### Example 2

```
Input:  nums = [4, 5, 6, 7, 0, 1, 2]
Output: 0
```

Original `[0, 1, 2, 4, 5, 6, 7]` rotated 4 times.

### Example 3

```
Input:  nums = [11, 13, 15, 17]
Output: 11
```

Rotated `n = 4` times — equivalent to no rotation.

---

## Constraints

- `n == nums.length`
- `1 <= n <= 5000`
- `-5000 <= nums[i] <= 5000`
- All elements of `nums` are **unique**.
- `nums` is sorted and rotated between `1` and `n` times.

---

## Intuition

### The shape of a rotated sorted array

A rotated sorted array of unique elements looks like **two ascending runs glued together**, with one "drop" between them:

```
high run ↗  ↘ drop  low run ↗
[ 4, 5, 6, 7,    0, 1, 2 ]
                 ↑ minimum lives right after the drop
```

The minimum is the **start of the lower run** — the first element of the second ascending segment. Equivalently, it's the **rotation pivot**.

### Why binary search works

At any midpoint `mid`, comparing `nums[mid]` to one of the endpoints tells us **which half contains the pivot**.

**Compare with `nums[right]`, not `nums[left]`.** Using `nums[left]` breaks on already-sorted arrays (rotated `n` times) — e.g. `[1, 2, 3]`. With `nums[right]`:

| Situation | Conclusion |
|---|---|
| `nums[mid] > nums[right]` | The drop must be on the right of `mid`. Min is in `(mid, right]`. |
| `nums[mid] ≤ nums[right]` | Right half is sorted. Min is at `mid` or to its left. |

In the second case we set `right = mid` (**not** `mid − 1`) — `mid` itself might be the answer.

### Why we never overshoot

- We only move `left` past `mid` when we've proven the min is strictly to the right.
- We only shrink `right` to `mid` when `mid` is a valid candidate.
- The loop terminates when `left == right`, sitting precisely on the minimum.

---

## Algorithm

```
left, right = 0, len(nums) - 1

while left < right:
    mid = (left + right) // 2

    if nums[mid] > nums[right]:
        left = mid + 1          # pivot lies to the right
    else:
        right = mid              # pivot is mid or to the left

return nums[left]
```

---

## Solution

```python
from typing import List


class Solution:
    def findMin(self, nums: List[int]) -> int:
        left, right = 0, len(nums) - 1

        while left < right:
            mid = (left + right) // 2

            if nums[mid] > nums[right]:
                left = mid + 1
            else:
                right = mid

        return nums[left]
```

---

## Complexity Analysis

| | Complexity | Reason |
|---|---|---|
| **Time** | **O(log n)** | Each iteration halves the search window |
| **Space** | **O(1)** | Two pointers, no auxiliary structures |

Meets the problem's mandated `O(log n)` time requirement.

---

## Full Trace — Example 2: `nums = [4, 5, 6, 7, 0, 1, 2]`

Indices: `0  1  2  3  4  5  6`

| Step | left | right | mid | nums[mid] | nums[right] | Decision | New window |
|:-:|:-:|:-:|:-:|:-:|:-:|---|---|
| 1 | 0 | 6 | 3 | 7 | 2 | `7 > 2` → pivot right of mid | `left = 4` |
| 2 | 4 | 6 | 5 | 1 | 2 | `1 ≤ 2` → pivot at mid or left | `right = 5` |
| 3 | 4 | 5 | 4 | 0 | 1 | `0 ≤ 1` → pivot at mid or left | `right = 4` |
| 4 | 4 | 4 | — | — | — | `left == right`, stop | — |

**Answer: `nums[4] = 0`** ✓

---

## Full Trace — Example 3: `nums = [11, 13, 15, 17]` (not rotated visibly)

| Step | left | right | mid | nums[mid] | nums[right] | Decision |
|:-:|:-:|:-:|:-:|:-:|:-:|---|
| 1 | 0 | 3 | 1 | 13 | 17 | `13 ≤ 17` → `right = 1` |
| 2 | 0 | 1 | 0 | 11 | 13 | `11 ≤ 13` → `right = 0` |
| 3 | 0 | 0 | — | — | — | stop |

**Answer: `nums[0] = 11`** ✓

Notice: if we had compared against `nums[left]`, the first step would mislead us — that's why the **`nums[right]` comparison** is the right choice.

---

## Why Compare to `nums[right]`, Not `nums[left]`?

Try `[1, 2, 3]` with the "compare to `nums[left]`" variant:

- `mid = 1`, `nums[mid] = 2`, `nums[left] = 1`. Since `2 > 1`, you'd conclude "left half is sorted, pivot is on the right" — but the actual minimum is on the **left** (`nums[0] = 1`).

The asymmetry comes from how rotation places the larger values: rotation moves the **front** of the array to the back, so the **right** endpoint always sits in the "lower run" (or equals it when there's no rotation). Comparing to `nums[right]` is therefore robust.

---

## Key Insights

| Insight | Explanation |
|---|---|
| **The minimum = the rotation pivot** | The smallest element marks where the array "wraps around" from high run to low run. |
| **Compare to `nums[right]`** | Robust for both rotated and non-rotated cases; avoids the `nums[left]` edge case. |
| **Use `right = mid`, not `right = mid − 1`** | When `nums[mid] ≤ nums[right]`, `mid` is still a candidate — don't discard it. |
| **Loop until `left == right`** | The window collapses onto the answer; no separate post-check needed. |

---

## Edge Cases

| Case | Behavior |
|---|---|
| `nums = [1]` | Loop never enters; returns `nums[0] = 1` |
| `nums = [2, 1]` | One iteration: `mid=0`, `2 > 1` → `left=1`. Return `1` |
| Already sorted (rotated `n` times) | `nums[mid] ≤ nums[right]` always; `right` shrinks to `0`. Return `nums[0]` |
| Min at the very last index | Impossible — that would mean the array is sorted with the smallest on the right, contradicting the rotation definition |
| All-negative values | Works unchanged; comparisons are correct regardless of sign |

---

## Alternative Phrasings

A common variant uses `nums[left]` with extra branching to handle the no-rotation case:

```python
def findMin(nums):
    left, right = 0, len(nums) - 1
    if nums[left] <= nums[right]:
        return nums[left]            # not rotated
    while left < right:
        mid = (left + right) // 2
        if nums[mid] >= nums[left]:
            left = mid + 1
        else:
            right = mid
    return nums[left]
```

This works but adds a special-case branch. The `nums[right]` version is cleaner — **one rule, no exceptions.**

---

## Approach Tags

`Binary Search` · `Rotated Sorted Array` · `Two Pointers` · `Pivot Search`

---

*Day 11 of the LeetCode Daily Challenge*
