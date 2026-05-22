# Day 18 — LeetCode Challenge

## 33. Search in Rotated Sorted Array

| Field | Details |
|---|---|
| **Difficulty** | Medium |
| **Topics** | Binary Search · Array · Divide and Conquer |
| **LeetCode Link** | [33. Search in Rotated Sorted Array](https://leetcode.com/problems/search-in-rotated-sorted-array/) |

---

## Problem Statement

An integer array `nums`, originally sorted ascending with **distinct** values, is possibly **left-rotated** at an unknown index `k`:

```
[nums[k], nums[k+1], …, nums[n-1], nums[0], …, nums[k-1]]
```

For example `[0,1,2,4,5,6,7]` left-rotated by `3` becomes `[4,5,6,7,0,1,2]`.

Given the (possibly rotated) array and a `target`, return the **index** of `target`, or `-1` if absent.

> **Required:** `O(log n)` runtime.

---

## Examples

### Example 1

```
Input:  nums = [4,5,6,7,0,1,2], target = 0
Output: 4
```

### Example 2

```
Input:  nums = [4,5,6,7,0,1,2], target = 3
Output: -1
```

### Example 3

```
Input:  nums = [1], target = 0
Output: -1
```

---

## Constraints

- `1 <= nums.length <= 5000`
- `-10⁴ <= nums[i] <= 10⁴`
- All values are **unique**.
- `nums` is ascending, possibly rotated.
- `-10⁴ <= target <= 10⁴`

---

## Intuition

### The "one break point" property

A rotated sorted array is two ascending runs with **exactly one drop** between them:

```
[4, 5, 6, 7 | 0, 1, 2]
            ↑ the single break point
```

When we pick any `mid` and split into `[left..mid]` and `[mid..right]`, the break point can lie in **at most one** of the two halves. So **at least one half is always fully sorted.**

That's the whole trick: a normal binary search can't decide direction in a rotated array, but if we first find the *sorted* half, that half has a known `[min, max]` range — and we can check in O(1) whether `target` belongs in it.

### The decision procedure

At each step:

1. If `nums[mid] == target` → return `mid`.
2. Determine the sorted half via `nums[left] <= nums[mid]`:
   - **True** → left half `[left..mid]` is sorted.
   - **False** → right half `[mid..right]` is sorted.
3. For the **sorted** half, its value range is fully known. Check whether `target` falls in that range:
   - If yes → recurse into the sorted half.
   - If no → recurse into the *other* (unsorted) half — it must be there if anywhere.

Each step halves the search space → `O(log n)`.

### Why `nums[left] <= nums[mid]` (with `<=`)

When `left == mid` (a one-element window), `nums[left] == nums[mid]`, and `<=` correctly classifies it as "left sorted." A strict `<` would mishandle that boundary. The `<=` also makes a non-rotated array always take the "left sorted" branch — exactly right.

### Why half-open range checks

For the sorted left half we test `nums[left] <= target < nums[mid]` — strict on the `nums[mid]` side because `mid` was *already* checked in step 1. Including it would be harmless but redundant; excluding it keeps the windows clean and the recursion strictly shrinking.

---

## Algorithm

```
left, right = 0, n - 1
while left <= right:
    mid = (left + right) // 2
    if nums[mid] == target:           return mid

    if nums[left] <= nums[mid]:       # left half sorted
        if nums[left] <= target < nums[mid]:
            right = mid - 1
        else:
            left = mid + 1
    else:                             # right half sorted
        if nums[mid] < target <= nums[right]:
            left = mid + 1
        else:
            right = mid - 1

return -1
```

---

## Solution

```python
from typing import List


class Solution:
    def search(self, nums: List[int], target: int) -> int:
        left, right = 0, len(nums) - 1

        while left <= right:
            mid = (left + right) // 2

            if nums[mid] == target:
                return mid

            if nums[left] <= nums[mid]:           # left half sorted
                if nums[left] <= target < nums[mid]:
                    right = mid - 1
                else:
                    left = mid + 1
            else:                                  # right half sorted
                if nums[mid] < target <= nums[right]:
                    left = mid + 1
                else:
                    right = mid - 1

        return -1
```

---

## Complexity Analysis

| | Complexity | Reason |
|---|---|---|
| **Time** | **O(log n)** | Each iteration discards exactly half the search window |
| **Space** | **O(1)** | Two pointers; iterative, no recursion stack |

Meets the mandated `O(log n)` bound. (Values being **distinct** is what guarantees this — duplicates would degrade it to O(n), see LC 81.)

---

## Full Trace — Example 1: `nums = [4,5,6,7,0,1,2], target = 0`

Indices: `0  1  2  3  4  5  6`

| Step | left | right | mid | nums[mid] | Sorted half | target in it? | New window |
|:-:|:-:|:-:|:-:|:-:|---|---|---|
| 1 | 0 | 6 | 3 | 7 | left `[4..7]` (`4 ≤ 7`) | `0` not in `[4,7)` | `left = 4` |
| 2 | 4 | 6 | 5 | 1 | left `[0..1]` (`0 ≤ 1`) | `0` in `[0,1)` ✓ | `right = 4` |
| 3 | 4 | 4 | 4 | 0 | `nums[mid] == target` | — | **return 4** ✓ |

---

## Full Trace — Example 2: `nums = [4,5,6,7,0,1,2], target = 3`

| Step | left | right | mid | nums[mid] | Sorted half | target in it? | New window |
|:-:|:-:|:-:|:-:|:-:|---|---|---|
| 1 | 0 | 6 | 3 | 7 | left `[4..7]` | `3` not in `[4,7)` | `left = 4` |
| 2 | 4 | 6 | 5 | 1 | left `[0..1]` | `3` not in `[0,1)` | `left = 6` |
| 3 | 6 | 6 | 6 | 2 | left `[2..2]` | `3` not in `[2,2)` | `left = 7` |
| 4 | 7 | 6 | — | — | `left > right`, exit | — | **return −1** ✓ |

---

## Walkthrough — `nums = [6,7,1,2,3,4,5], target = 6` (right half sorted case)

| Step | left | right | mid | nums[mid] | `nums[left] ≤ nums[mid]`? | Sorted half | Decision |
|:-:|:-:|:-:|:-:|:-:|:-:|---|---|
| 1 | 0 | 6 | 3 | 2 | `6 ≤ 2`? **no** | right `[2..5]` | `6` not in `(2,5]` → `right = 2` |
| 2 | 0 | 2 | 1 | 7 | `6 ≤ 7`? yes | left `[6..7]` | `6` in `[6,7)` ✓ → `right = 0` |
| 3 | 0 | 0 | 0 | 6 | — | — | `nums[0] == 6` → **return 0** ✓ |

This shows the `else` branch (right half sorted) working alongside the left-sorted branch.

---

## Why Plain Binary Search Fails Here

In a normal sorted array, `nums[mid] < target` tells you "go right." In a *rotated* array that's a lie:

```
nums = [4,5,6,7,0,1,2], target = 1, mid → 7
```

`7 > 1`, so plain binary search would go **left** — but `1` is on the **right**. The rotation breaks the monotonic invariant binary search relies on.

The fix isn't to abandon binary search — it's to **first locate the sorted half**, where the invariant *does* hold, and reason from there.

---

## Two-Pass Alternative (Find Pivot, Then Search)

```python
def search(self, nums, target):
    n = len(nums)
    # 1) find pivot (index of minimum) — LC 153 logic
    lo, hi = 0, n - 1
    while lo < hi:
        mid = (lo + hi) // 2
        if nums[mid] > nums[hi]:
            lo = mid + 1
        else:
            hi = mid
    pivot = lo
    # 2) ordinary binary search on the correct rotated segment
    lo, hi = (0, pivot - 1) if target >= nums[0] else (pivot, n - 1)
    while lo <= hi:
        mid = (lo + hi) // 2
        if nums[mid] == target:
            return mid
        elif nums[mid] < target:
            lo = mid + 1
        else:
            hi = mid - 1
    return -1
```

Also `O(log n)` (two binary searches). The **one-pass** version above is preferred — fewer moving parts, single loop.

---

## Key Insights

| Insight | Explanation |
|---|---|
| **At least one half is always sorted** | A single break point can't be in both halves of the `mid` split. |
| **Reason from the sorted half** | Its `[min, max]` range is known, so an O(1) range check decides direction. |
| **`<=` in the sorted-half test** | Handles `left == mid` and the no-rotation case correctly. |
| **Half-open range checks** | `mid` is already tested in step 1 — exclude it to keep windows strictly shrinking. |
| **Distinct values guarantee O(log n)** | With duplicates the sorted-half test becomes ambiguous → see LC 81. |

---

## Edge Cases

| Case | Behavior |
|---|---|
| `nums = [1], target = 1` | `mid = 0`, immediate match → `0` |
| `nums = [1], target = 0` | One iteration, no match → `-1` |
| Not rotated (`[1,2,3,4,5]`) | `nums[left] ≤ nums[mid]` always → behaves like plain binary search |
| `target` is the pivot/minimum | Found via the sorted-half range checks |
| `target` outside the value range | Pointers cross → `-1` |

---

## Approach Tags

`Binary Search` · `Rotated Sorted Array` · `Sorted-Half Detection` · `One-Pass`

---

*Day 18 of the LeetCode Daily Challenge*
