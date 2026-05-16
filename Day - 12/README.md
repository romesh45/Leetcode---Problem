# Day 12 — LeetCode Challenge

## 154. Find Minimum in Rotated Sorted Array II

| Field | Details |
|---|---|
| **Difficulty** | Hard |
| **Topics** | Binary Search · Array · Divide and Conquer |
| **LeetCode Link** | [154. Find Minimum in Rotated Sorted Array II](https://leetcode.com/problems/find-minimum-in-rotated-sorted-array-ii/) |

---

## Problem Statement

A sorted-ascending array (possibly with **duplicates**) of length `n` is rotated between `1` and `n` times. Rotating once turns `[a₀, a₁, …, a_{n-1}]` into `[a_{n-1}, a₀, a₁, …, a_{n-2}]`.

Examples of rotations of `[0, 1, 4, 4, 5, 6, 7]`:
- `[4, 5, 6, 7, 0, 1, 4]` — rotated 4 times
- `[0, 1, 4, 4, 5, 6, 7]` — rotated 7 times (no visible change)

Given the rotated array `nums` (which **may contain duplicates**), return the **minimum** element.

> **Goal:** decrease the overall operation steps as much as possible.

---

## Examples

### Example 1

```
Input:  nums = [1, 3, 5]
Output: 1
```

### Example 2

```
Input:  nums = [2, 2, 2, 0, 1]
Output: 0
```

---

## Constraints

- `n == nums.length`
- `1 <= n <= 5000`
- `-5000 <= nums[i] <= 5000`
- `nums` is sorted and rotated between `1` and `n` times.

---

## Intuition

### What changes vs. LC 153?

In [LC 153](https://leetcode.com/problems/find-minimum-in-rotated-sorted-array/), elements are **unique** → at any mid, `nums[mid]` vs. `nums[right]` is strictly `>` or `<`, giving a clean two-way split. Each iteration **halves** the search space → `O(log n)`.

With duplicates allowed, a third case appears: **`nums[mid] == nums[right]`**. This case is genuinely **ambiguous** — the minimum could be on either side. Two examples make this concrete:

| Array | `mid` | `nums[mid]` | `nums[right]` | Min position |
|---|:-:|:-:|:-:|:-:|
| `[3, 3, 1, 3]` | 1 | 3 | 3 | **left of mid** (index 2 ≠ left, but min `1` lies in `(mid, right)`) |
| `[3, 1, 3, 3, 3]` | 2 | 3 | 3 | **left of mid** (index 1) |
| `[10, 1, 10, 10, 10]` | 2 | 10 | 10 | **left of mid** (index 1) |
| `[1, 10, 10, 10, 10]` | 2 | 10 | 10 | **left of mid** (index 0) |

The same `nums[mid] == nums[right]` signal corresponds to different min locations. **No deterministic O(1) decision can resolve this ambiguity.**

### The safe fallback: `right -= 1`

When stuck on a tie, shrink the window by one from the right.

**Why it's safe:** Suppose `nums[right]` happens to *be* the unique minimum. Since `nums[mid] == nums[right]`, `nums[mid]` is also that minimum — so we still have a copy inside the window. Dropping `right` never loses the answer.

**Why we use the right side, not the left:** The same logic argument doesn't apply on the left endpoint — `nums[mid] == nums[right]` says nothing about `nums[left]`. So `right -= 1` is the principled choice.

### Why complexity degrades

In the duplicate-tie case we shrink the window by **1**, not by half. The pathological input
```
[3, 3, 3, …, 3, 1, 3, …, 3]
```
keeps triggering the tie branch, giving **O(n)** worst case. Average/typical inputs remain logarithmic.

---

## Algorithm

```
left, right = 0, len(nums) - 1

while left < right:
    mid = (left + right) // 2

    if   nums[mid] >  nums[right]:  left  = mid + 1   # min in (mid, right]
    elif nums[mid] <  nums[right]:  right = mid       # min at mid or left
    else:                           right -= 1        # ambiguous → shrink by 1

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
            elif nums[mid] < nums[right]:
                right = mid
            else:
                right -= 1

        return nums[left]
```

---

## Complexity Analysis

| | Complexity | Reason |
|---|---|---|
| **Time (average)** | **O(log n)** | Two of the three branches halve the window |
| **Time (worst case)** | **O(n)** | All-equal-with-one-min inputs force the `right -= 1` branch every step |
| **Space** | **O(1)** | Two pointers, no auxiliary structures |

> **Follow-up answer:** Yes, duplicates **do** affect complexity. Without them, every iteration cuts the window in half → `O(log n)`. With duplicates, the `nums[mid] == nums[right]` tie can only safely be resolved by shrinking the window by 1, so adversarial inputs like `[3, 3, 3, 3, 1, 3, 3]` push the worst case to **O(n)**.

---

## Full Trace — Example 2: `nums = [2, 2, 2, 0, 1]`

Indices: `0  1  2  3  4`

| Step | left | right | mid | nums[mid] | nums[right] | Branch | New window |
|:-:|:-:|:-:|:-:|:-:|:-:|---|---|
| 1 | 0 | 4 | 2 | 2 | 1 | `2 > 1` → right side | `left = 3` |
| 2 | 3 | 4 | 3 | 0 | 1 | `0 < 1` → at mid or left | `right = 3` |
| 3 | 3 | 3 | — | — | — | `left == right`, stop | — |

**Answer: `nums[3] = 0`** ✓

---

## Full Trace — `nums = [3, 3, 1, 3]` (tie-case demo)

| Step | left | right | mid | nums[mid] | nums[right] | Branch | New window |
|:-:|:-:|:-:|:-:|:-:|:-:|---|---|
| 1 | 0 | 3 | 1 | 3 | 3 | **tie** → `right -= 1` | `right = 2` |
| 2 | 0 | 2 | 1 | 3 | 1 | `3 > 1` → right side | `left = 2` |
| 3 | 2 | 2 | — | — | — | stop | — |

**Answer: `nums[2] = 1`** ✓

The tie branch correctly preserved the minimum by dropping a duplicate.

---

## Worst-Case Trace — `nums = [1, 1, 1, 1, 1]` (all equal)

Every step is a tie:

| Step | left | right | Branch |
|:-:|:-:|:-:|---|
| 1 | 0 | 4 | tie → `right = 3` |
| 2 | 0 | 3 | tie → `right = 2` |
| 3 | 0 | 2 | tie → `right = 1` |
| 4 | 0 | 1 | tie → `right = 0` |
| 5 | 0 | 0 | stop |

5 iterations for `n = 5` — linear. **Answer: `1`** ✓

---

## Why Dropping `right` Is Always Safe

Claim: If `nums[mid] == nums[right]` and `left < mid < right`, then removing index `right` from the search window preserves at least one occurrence of the minimum.

Proof sketch:
1. The minimum value `m` of the (full original) array appears somewhere in `[left, right]` at the start of each iteration (loop invariant).
2. Two sub-cases:
   - `nums[right] ≠ m` → the min sits somewhere in `[left, right − 1]`. Dropping `right` is harmless.
   - `nums[right] == m` → then `nums[mid] == m` too (given the tie). So `mid ∈ [left, right − 1]` also holds an occurrence of `m`. Dropping `right` still leaves one inside.

Either way, the invariant survives. ∎

---

## Comparison to LC 153

| Aspect | LC 153 (unique) | LC 154 (duplicates) |
|---|---|---|
| Branches | 2 | 3 |
| Window shrink per step | always half | half (2 branches) or 1 (tie branch) |
| Worst case | `O(log n)` | `O(n)` |
| Code change | — | one extra `elif` + `right -= 1` |

The algorithm is essentially the same — just with an honest "I don't know, step conservatively" branch.

---

## Key Insights

| Insight | Explanation |
|---|---|
| **Duplicates break the binary-search invariant** | `nums[mid] == nums[right]` can correspond to different min locations — no O(1) tiebreak exists. |
| **`right -= 1` is the safe, minimal step** | Preserves the loop invariant without overshooting; never discards the only copy of the minimum. |
| **Worst case is genuinely linear** | Adversarial inputs (mostly equal elements) force the tie branch repeatedly. This is a property of the problem, not the algorithm. |
| **Same skeleton as LC 153** | The only diff is splitting the original "else" into two branches: `<` (binary-step left) and `==` (single step). |

---

## Edge Cases

| Case | Behavior |
|---|---|
| `nums = [1]` | Loop never enters; returns `1` |
| `nums = [1, 1, 1, 1]` | All ties; `right` decrements down to `0`; returns `1` |
| `nums = [2, 2, 2, 0, 1]` | Standard case from Example 2 |
| `nums = [3, 1, 3]` | Tie at first step (`nums[1]=1`, `nums[2]=3` → `1 < 3`, not a tie). Returns `1` |
| Strictly sorted (no rotation visible) | `nums[mid] ≤ nums[right]` always (or `<` mostly); converges to `nums[0]` |
| All elements equal to the min | Returns that value |

---

## Approach Tags

`Binary Search` · `Rotated Sorted Array` · `Duplicates Handling` · `Worst-Case O(n)`

---

*Day 12 of the LeetCode Daily Challenge*
