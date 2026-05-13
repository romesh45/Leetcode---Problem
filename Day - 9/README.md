# Day 9 — LeetCode Daily Chllenge

## 1674. Minimum Moves to Make Array Complementary

| Field | Details |
|---|---|
| **Difficulty** | Medium |
| **Topics** | Difference Array · Prefix Sum · Greedy · Range Updates |
| **LeetCode Link** | [1674. Minimum Moves to Make Array Complementary](https://leetcode.com/problems/minimum-moves-to-make-array-complementary/) |

---

## Problem Statement

You are given an integer array `nums` of **even** length `n` and an integer `limit`. In one move, you can replace any integer in `nums` with another integer in `[1, limit]`.

The array is **complementary** when, for every index `i`:

```
nums[i] + nums[n − 1 − i] = same constant T
```

Return the **minimum number of moves** required to make `nums` complementary.

---

## Examples

### Example 1

```
Input:  nums = [1,2,4,3], limit = 4
Output: 1
```

Change `nums[2] = 4 → 2` to get `[1,2,2,3]`. Now every pair sums to `4`.

### Example 2

```
Input:  nums = [1,2,2,1], limit = 2
Output: 2
```

Convert to `[2,2,2,2]`. Two changes needed — we can't use `3` since `3 > limit`.

### Example 3

```
Input:  nums = [1,2,1,2], limit = 2
Output: 0
```

Already complementary (every pair sums to `3`).

---

## Constraints

- `n == nums.length`
- `2 <= n <= 10^5`
- `1 <= nums[i] <= limit <= 10^5`
- `n` is even.

---

## Intuition

### Reframe the problem around the **target sum** `T`

We don't know what value the common sum should be. But it lives in a known finite range:

```
T ∈ [2, 2 · limit]
```

For every candidate `T`, compute the total cost of fixing all pairs, then take the minimum.

Naïvely that's `O(n · limit)` — too slow. The trick is to realize **each pair has only three cost zones** as `T` varies. We can encode those zones with a **difference array** and sweep in `O(n + limit)`.

### What does one pair `(a, b)` cost for a given `T`?

Let `lo = min(a, b)` and `hi = max(a, b)`.

| Case | Range of `T` | Cost |
|---|---|:---:|
| Both stay (already sums to `T`) | `T == a + b` (single point) | **0** |
| Change exactly one of the two | `T ∈ [1 + lo, limit + hi]` | **1** |
| Must change both | everywhere else in `[2, 2·limit]` | **2** |

**Why the 1-move window is `[1 + lo, limit + hi]`?**
- Keep `hi` fixed, replace `lo` with any value in `[1, limit]` → reachable sums `[1 + hi, limit + hi]`.
- Keep `lo` fixed, replace `hi` with any value in `[1, limit]` → reachable sums `[1 + lo, limit + lo]`.
- Union of those two intervals (they overlap because `lo ≤ hi`) is **`[1 + lo, limit + hi]`**.

### The difference-array stamp

For each pair, we apply three range updates on a 1D cost function over `T`:

```
+2  on  [2, 2·limit]            ← baseline: assume worst case (2 moves)
−1  on  [1 + lo, limit + hi]    ← inside the 1-move window, save one move
−1  on  [a + b, a + b]          ← exact-match point, save one more
```

After stamping all pairs, take a prefix sum to get `cost(T)` for every `T`, then return `min cost(T)`.

---

## Algorithm

```
1. Allocate diff[] of size 2·limit + 2 (zero-initialized).

2. For each pair (a, b) with lo = min(a,b), hi = max(a,b):
       diff[2]              += 2
       diff[2·limit + 1]    -= 2
       diff[1 + lo]         -= 1
       diff[limit + hi + 1] += 1
       diff[a + b]          -= 1
       diff[a + b + 1]      += 1

3. ans = +∞;  cur = 0
   For T in [2, 2·limit]:
       cur += diff[T]
       ans = min(ans, cur)

4. Return ans.
```

---

## Solution

```python
from typing import List


class Solution:
    def minMoves(self, nums: List[int], limit: int) -> int:
        n = len(nums)
        # Difference array over all possible target sums T ∈ [2, 2*limit].
        diff = [0] * (2 * limit + 2)

        for i in range(n // 2):
            a, b = nums[i], nums[n - 1 - i]
            lo, hi = min(a, b), max(a, b)

            # Baseline: 2 moves for every T in [2, 2*limit].
            diff[2]              += 2
            diff[2 * limit + 1]  -= 2

            # 1-move window: [1 + lo, limit + hi] — save one move.
            diff[1 + lo]         -= 1
            diff[limit + hi + 1] += 1

            # 0-move point: T == a + b — save one more move.
            diff[a + b]          -= 1
            diff[a + b + 1]      += 1

        ans = float("inf")
        cur = 0
        for T in range(2, 2 * limit + 1):
            cur += diff[T]
            if cur < ans:
                ans = cur

        return ans
```

---

## Complexity Analysis

| | Complexity | Reason |
|---|---|---|
| **Time** | **O(n + limit)** | `n/2` constant-time stamps + one linear sweep over `2·limit + 1` targets |
| **Space** | **O(limit)** | The difference array |

This beats the naive `O(n · limit)` enumerate-every-T approach by a factor of `n`.

---

## Full Trace — Example 1: `nums = [1,2,4,3], limit = 4`

Pairs: `(1, 3)` and `(2, 4)`.

**Pair (1, 3)** — `lo=1, hi=3, sum=4`:
- 2-move baseline: `[2, 8]` gets `+2`
- 1-move window: `[1+1, 4+3] = [2, 7]` gets `−1`
- 0-move point: `T = 4` gets `−1`

**Pair (2, 4)** — `lo=2, hi=4, sum=6`:
- 2-move baseline: `[2, 8]` gets `+2`
- 1-move window: `[1+2, 4+4] = [3, 8]` gets `−1`
- 0-move point: `T = 6` gets `−1`

**Resulting cost per `T`:**

| T | Pair (1,3) | Pair (2,4) | Total cost |
|:-:|:-:|:-:|:-:|
| 2 | 1 (in 1-move window) | 2 | 3 |
| 3 | 1 | 1 | 2 |
| **4** | **0** ✓ | **1** | **1** ← minimum |
| 5 | 1 | 1 | 2 |
| 6 | 1 | 0 ✓ | 1 |
| 7 | 1 | 1 | 2 |
| 8 | 2 | 1 | 3 |

Minimum is **1**, achieved at `T = 4` (or `T = 6`). ✓

---

## Full Trace — Example 2: `nums = [1,2,2,1], limit = 2`

Pairs: `(1, 1)` and `(2, 2)`.

| T | Pair (1,1) cost | Pair (2,2) cost | Total |
|:-:|:-:|:-:|:-:|
| 2 | **0** ✓ | 2 | 2 |
| 3 | 1 | 1 | **2** ← min |
| 4 | 2 | **0** ✓ | 2 |

Every `T` costs `2`. **Answer: 2** ✓ (matches `[2,2,2,2]`.)

---

## Why the 1-Move Window Formula Works

The two intervals from changing one element are:

```
keep hi, change lo:    [1 + hi, limit + hi]
keep lo, change hi:    [1 + lo, limit + lo]
```

Since `lo ≤ hi`, the second interval starts at or before the first, and `limit + lo ≤ limit + hi`. They overlap (or touch) at `1 + hi ≤ limit + lo` iff `hi − lo ≤ limit − 1`, which is always true because both are in `[1, limit]`.

So their union is the single interval **`[1 + lo, limit + hi]`** — that's the entire region where **one move suffices**.

---

## Key Insights

| Insight | Explanation |
|---|---|
| **Iterate over targets, not over moves** | The unknown is `T` — bounded by `[2, 2·limit]`. Fix `T`, sum costs. |
| **Each pair has 3 cost zones** | `0`, `1`, or `2` moves, defined by simple intervals around `(a+b)`. |
| **Difference array beats brute force** | Range updates + one sweep recover the full cost curve in linear time. |
| **No need to track *which* element to change** | We only count moves — the actual replacement value is implied by `T`. |

---

## Edge Cases

| Case | Behavior |
|---|---|
| Already complementary | Some `T` lies in every pair's 0-move point → answer `0` |
| All elements equal | Every pair has identical `0`-move point at `2·val`; answer `0` |
| Extreme `limit = 1` | Only `T = 2` is valid; cost is `2 · (#pairs not already summing to 2)` |
| Pair with `lo == hi` | 1-move window still valid; degenerate but handled |

---

## Approach Tags

`Difference Array` · `Prefix Sum` · `Range Updates` · `Greedy over Targets`

---

*Day 9 of the LeetCode Daily Challenge*
