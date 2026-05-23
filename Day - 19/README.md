# Day 19 — LeetCode Challenge

## 1752. Check if Array Is Sorted and Rotated

| Field | Details |
|---|---|
| **Difficulty** | Easy |
| **Topics** | Array · Circular Scan · Counting |
| **LeetCode Link** | [1752. Check if Array Is Sorted and Rotated](https://leetcode.com/problems/check-if-array-is-sorted-and-rotated/) |

---

## Problem Statement

Given an array `nums`, return `true` if it was originally sorted in **non-decreasing** order and then **rotated** by some number of positions (including zero). Otherwise return `false`. Duplicates are allowed.

> Rotating array `A` by `x` positions produces `B` such that `B[i] == A[(i + x) % n]` for every valid index `i`.

---

## Examples

### Example 1

```
Input:  nums = [3, 4, 5, 1, 2]
Output: true
```

`[1, 2, 3, 4, 5]` rotated by `2` positions.

### Example 2

```
Input:  nums = [2, 1, 3, 4]
Output: false
```

No rotation of any sorted array produces this.

### Example 3

```
Input:  nums = [1, 2, 3]
Output: true
```

Already sorted (rotation by `0`).

---

## Constraints

- `1 <= nums.length <= 100`
- `1 <= nums[i] <= 100`

---

## Intuition

### The "at most one drop" property

A non-decreasing array, rotated by any amount, has a very specific shape:

```
   original :  [1, 2, 3, 4, 5]
   rotated  :  [3, 4, 5, 1, 2]
                       ↑ exactly one "drop" (5 → 1)
```

It's **two ascending runs glued together circularly**, with at most **one drop** — the position where a larger value is immediately followed by a smaller one.

### Counting drops as a circular scan

Treat the array as **circular**: compare each index `i` to its next neighbour `(i + 1) % n`. Count the number of strict decreases `nums[i] > nums[(i+1) % n]`.

- **0 drops** — all equal (e.g. `[1, 1, 1]`) — trivially valid.
- **1 drop** — exactly one decrease somewhere in the circle.
- **≥ 2 drops** — impossible from any rotation of a sorted array.

Return `true` iff `drops ≤ 1`.

### Why the circular wrap matters

Why include `nums[n-1] vs nums[0]`?

Because in a properly rotated non-decreasing array, the **single drop is always between the original max and the original min** — and that pair appears either:
- inside the array (when rotated, e.g. `5 → 1` at indices `2 → 3` in `[3,4,5,1,2]`), or
- at the wrap-around (when not rotated, e.g. `3 → 1` in `[1,2,3]`).

Using `(i + 1) % n` unifies both cases under one rule: **count drops anywhere in the circular array; allow at most one.**

### Quick sanity check on `[1, 2, 3]`

- `i = 0`: `1 > 2`? no.
- `i = 1`: `2 > 3`? no.
- `i = 2`: `3 > 1`? **yes** — drop counts as 1.

Total = 1 ≤ 1 → `true`. ✓ The wrap supplies the single allowed drop.

---

## Algorithm

```
drops = 0
for i in 0 .. n-1:
    if nums[i] > nums[(i + 1) % n]:
        drops += 1
        if drops > 1:
            return False
return True
```

---

## Solution

```python
from typing import List


class Solution:
    def check(self, nums: List[int]) -> bool:
        n = len(nums)
        drops = 0
        for i in range(n):
            if nums[i] > nums[(i + 1) % n]:
                drops += 1
                if drops > 1:
                    return False
        return True
```

---

## Complexity Analysis

| | Complexity | Reason |
|---|---|---|
| **Time** | **O(n)** | Single pass; short-circuits as soon as `drops` exceeds 1 |
| **Space** | **O(1)** | One integer counter |

Optimal — any algorithm must read every element in the worst case to confirm validity.

---

## Full Trace — Example 1: `nums = [3, 4, 5, 1, 2]`

| i | nums[i] | nums[(i+1) % 5] | Drop? | drops |
|:-:|:-:|:-:|:-:|:-:|
| 0 | 3 | 4 | no | 0 |
| 1 | 4 | 5 | no | 0 |
| 2 | 5 | 1 | **yes** | 1 |
| 3 | 1 | 2 | no | 1 |
| 4 | 2 | 3 (wrap) | no | 1 |

Final `drops = 1 ≤ 1` → **return True** ✓

---

## Full Trace — Example 2: `nums = [2, 1, 3, 4]`

| i | nums[i] | nums[(i+1) % 4] | Drop? | drops |
|:-:|:-:|:-:|:-:|:-:|
| 0 | 2 | 1 | **yes** | 1 |
| 1 | 1 | 3 | no | 1 |
| 2 | 3 | 4 | no | 1 |
| 3 | 4 | 2 (wrap) | **yes** | **2** → **return False** ✓ |

Short-circuits at the second drop.

---

## Full Trace — Example 3: `nums = [1, 2, 3]` (no rotation)

| i | nums[i] | nums[(i+1) % 3] | Drop? | drops |
|:-:|:-:|:-:|:-:|:-:|
| 0 | 1 | 2 | no | 0 |
| 1 | 2 | 3 | no | 0 |
| 2 | 3 | 1 (wrap) | **yes** | 1 |

Final `drops = 1 ≤ 1` → **return True** ✓

The wrap-around supplies the single allowed drop for the no-rotation case.

---

## Why "At Most One Drop" Is the Complete Characterization

**Forward direction** (sorted-and-rotated ⇒ ≤ 1 drop)

If `nums = sorted(A)` rotated by `k`, then `nums` is two ascending runs:
- `sorted(A)[k:]` (ascending)
- `sorted(A)[:k]` (ascending)

Glued circularly, the only place a drop can occur is between the last of the first run (the original max) and the first of the second run (the original min) — that's **exactly one** circular position. If `k = 0`, that drop sits at the wrap.

**Reverse direction** (≤ 1 drop ⇒ sorted-and-rotated)

Let `d` be the unique drop position (or any position, if zero drops). Set `k = d + 1` (mod `n`). Then `nums` rotated by `−k` is `[nums[k], nums[k+1], …, nums[k-1]]`, which is fully non-decreasing because no drop survives the rotation. That's the original sorted array.

So "drops ≤ 1 in the circular scan" ⇔ "is a rotation of a non-decreasing array." ∎

---

## Key Insights

| Insight | Explanation |
|---|---|
| **A rotation of a sorted array = two ascending runs** | Joined circularly, with at most one "drop" between them. |
| **Use `(i + 1) % n` for the circular wrap** | Unifies the unrotated case (drop at wrap) and rotated case (drop internal) under one rule. |
| **Short-circuit on second drop** | Saves time on adversarial input; doesn't change the asymptotic bound. |
| **Duplicates are harmless** | Equal adjacent values aren't drops (`>` is strict), so plateaus like `[1,1,1]` validate correctly. |

---

## Alternative — Three-Pointer / Linear Variant

You could also linearize the check by counting `nums[i-1] > nums[i]` for `i` in `1..n-1`, then appending the wrap comparison:

```python
def check(self, nums):
    drops = sum(1 for i in range(1, len(nums)) if nums[i-1] > nums[i])
    if nums[-1] > nums[0]:
        drops += 1
    return drops <= 1
```

Same `O(n)` time, same `O(1)` space — purely stylistic. The `% n` version is the cleanest expression of the circular-scan idea.

---

## Edge Cases

| Case | Behavior |
|---|---|
| `nums = [1]` | No iterations; `drops = 0` → **True** |
| `nums = [1, 1, 1]` | All equal; no strict drops → **True** |
| `nums = [2, 1]` | Drop at `i = 0` (`2 > 1`); wrap `1 → 2` is not a drop → 1 drop → **True** |
| `nums = [1, 2, 3]` (unrotated) | Single drop at the wrap `3 → 1` → **True** |
| `nums = [1, 3, 2]` | Drops at `3 → 2` and wrap `2 → 1` → 2 drops → **False** |

---

## Approach Tags

`Circular Scan` · `Counting` · `Single Pass` · `Constant Space`

---

*Day 19 of the LeetCode Daily Challenge*
