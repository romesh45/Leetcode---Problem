# Day 37 — LeetCode Challenge

## 3691. Maximum Total Subarray Value II

| Field | Details |
|---|---|
| **Difficulty** | Hard |
| **Topics** | Heap · Sparse Table · Monotonicity · K-Largest from Sorted Lists |
| **LeetCode Link** | [3691. Maximum Total Subarray Value II](https://leetcode.com/problems/maximum-total-subarray-value-ii/) |

---

## Problem Statement

Given an integer array `nums` of length `n` and an integer `k`, select **exactly `k` distinct** subarrays `nums[l..r]`. Subarrays may overlap, but the **same** `(l, r)` pair **cannot** be chosen twice.

The **value** of a subarray is `max(nums[l..r]) − min(nums[l..r])`. Return the **maximum** possible sum of values over the `k` chosen subarrays.

---

## Examples

### Example 1

```
Input:  nums = [1,3,2], k = 2
Output: 4
```

Pick `[0..1]` (value `3−1=2`) and `[0..2]` (value `3−1=2`) → total `4`.

### Example 2

```
Input:  nums = [4,2,5,1], k = 3
Output: 12
```

Pick `[0..3]`, `[1..3]`, `[2..3]` — three *distinct* subarrays, each spanning both the `5` and the `1`, each worth `4` → total `12`.

---

## Constraints

- `1 <= n == nums.length <= 5·10⁴`
- `0 <= nums[i] <= 10⁹`
- `1 <= k <= min(10⁵, n(n+1)/2)`  ← **distinctness is the difference from "I"**

---

## Intuition

### Why Day 36's one-liner dies

In [the "I" version (Day 36)](https://leetcode.com/problems/maximum-total-subarray-value-i/), repeats were allowed, so the answer was just `k × (globalMax − globalMin)`. Now every pick must be a **distinct** `(l, r)` — we genuinely need the **k largest subarray values**.

But there are `n(n+1)/2 ≈ 1.25·10⁹` subarrays at `n = 5·10⁴`. Enumerating and sorting them all is hopeless. We need the k largest **without materializing the rest**.

### The monotonicity that saves us

Fix the left end `l` and grow the right end `r`. The window only gains elements, so:

- `max(l..r)` is **non-decreasing** in `r`
- `min(l..r)` is **non-increasing** in `r`
- ⟹ `value(l, r) = max − min` is **non-decreasing** in `r`

So for each `l`, the subarrays starting at `l` form a chain already **sorted descending** when read from `r = n−1` down to `r = l`:

```
value(l, n-1) ≥ value(l, n-2) ≥ … ≥ value(l, l) = 0
```

### k largest from n sorted lists — the classic heap pattern

We have `n` descending-sorted chains and want the k largest elements overall:

1. **Seed** a max-heap with each chain's head: `(value(l, n−1), l, n−1)` for every `l`.
2. **Pop** the global maximum — that's the next-largest subarray value anywhere.
3. **Push** the popped chain's successor `(l, r−1)` (the next-best subarray starting at `l`).
4. Repeat `k` times, summing the popped values.

Distinctness is automatic: every `(l, r)` enters the heap at most once (chain `l` only ever steps from `r` to `r−1`).

**Early exit:** values are `≥ 0`, so the moment the heap's top is `0`, everything remaining contributes nothing — break.

### O(1) range max/min — sparse tables

Each push needs `value(l, r−1)` instantly. Build **sparse tables** for range max and range min once (`O(n log n)`); any query is then two overlapping power-of-two blocks → `O(1)`.

---

## Algorithm

```
build sparse tables for range max / range min          O(n log n)

heap ← { (-value(l, n-1), l, n-1) : l = 0..n-1 }       O(n)
total ← 0
repeat k times:
    (v, l, r) ← pop max
    if v == 0: break                                   ← all remaining are 0
    total += v
    if r-1 ≥ l: push (-value(l, r-1), l, r-1)
return total
```

---

## Solution

```python
import heapq
from typing import List


class Solution:
    def maxTotalValue(self, nums: List[int], k: int) -> int:
        n = len(nums)

        # Sparse tables for O(1) range max / min.
        max_st = [nums[:]]
        min_st = [nums[:]]
        j = 1
        while (1 << j) <= n:
            half = 1 << (j - 1)
            pm, pn = max_st[-1], min_st[-1]
            size = n - (1 << j) + 1
            max_st.append([max(pm[i], pm[i + half]) for i in range(size)])
            min_st.append([min(pn[i], pn[i + half]) for i in range(size)])
            j += 1

        def value(l: int, r: int) -> int:
            j = (r - l + 1).bit_length() - 1
            hi = max(max_st[j][l], max_st[j][r - (1 << j) + 1])
            lo = min(min_st[j][l], min_st[j][r - (1 << j) + 1])
            return hi - lo

        heap = [(-value(l, n - 1), l, n - 1) for l in range(n)]
        heapq.heapify(heap)

        total = 0
        for _ in range(k):
            v, l, r = heapq.heappop(heap)
            if v == 0:
                break
            total += -v
            if r - 1 >= l:
                heapq.heappush(heap, (-value(l, r - 1), l, r - 1))

        return total
```

---

## Complexity Analysis

| | Complexity | Reason |
|---|---|---|
| **Time** | **O((n + k) log n)** | Sparse-table build `O(n log n)`; heapify `O(n)`; `k` pops/pushes at `O(log n)` each, `O(1)` value query |
| **Space** | **O(n log n)** | Two sparse tables (~16 levels at `n = 5·10⁴`); heap holds ≤ `n` entries |

Measured: `n = 5·10⁴, k = 10⁵` completes in **~0.3 s** in Python.

> **Overflow note:** the total can reach `10⁵ × 10⁹ = 10¹⁴` — fine in Python, needs `long` elsewhere.

---

## Full Trace — Example 2: `nums = [4,2,5,1], k = 3`

**Seed the heap** (each `l`'s widest subarray):

| chain `l` | subarray | value |
|:-:|:-:|:-:|
| 0 | `[4,2,5,1]` | `5−1 = 4` |
| 1 | `[2,5,1]` | `5−1 = 4` |
| 2 | `[5,1]` | `5−1 = 4` |
| 3 | `[1]` | `0` |

**Pops:**

| Pop # | Popped | Value | Successor pushed | Running total |
|:-:|:-:|:-:|:-:|:-:|
| 1 | `(0, 3)` | 4 | `(0, 2)` value `5−2=3` | 4 |
| 2 | `(1, 3)` | 4 | `(1, 2)` value `5−2=3` | 8 |
| 3 | `(2, 3)` | 4 | `(2, 2)` value `0` | **12** |

**Answer: 12** ✓ — and note the three picks are exactly the distinct subarrays from the official explanation.

---

## Full Trace — Example 1: `nums = [1,3,2], k = 2`

Seeds: `(0,2)` value `2`, `(1,2)` value `1`, `(2,2)` value `0`.

| Pop # | Popped | Value | Successor | Total |
|:-:|:-:|:-:|:-:|:-:|
| 1 | `(0, 2)` | 2 | `(0, 1)` value `3−1=2` | 2 |
| 2 | `(0, 1)` | 2 | `(0, 0)` value `0` | **4** |

**Answer: 4** ✓

---

## Why the Heap Pattern Is Correct

**Claim:** the `k` popped values are exactly the `k` largest subarray values.

This is the standard merge-of-sorted-lists invariant: at every moment, the heap contains the **largest not-yet-popped element of every chain** (each chain is visited head-first, and we push the successor immediately after popping). The global maximum of all un-popped elements is therefore always present in the heap — so each pop takes the true next-largest. Induction over `k` pops gives the claim. ∎

Distinctness: a pair `(l, r)` is pushed only once — either as a seed (`r = n−1`) or as the unique successor of `(l, r+1)`. No duplicates can enter.

---

## Alternative — Binary Search on the Threshold

Another route: binary-search a threshold `T`, counting subarrays with `value ≥ T` via a **two-pointer + monotonic deque** sliding window in `O(n)` per check (the same monotonicity makes the count tractable). Then sum the values above the final threshold. It avoids sparse tables but computing the *sum* (not just count) above a threshold adds real complexity — contribution-counting with monotonic stacks. The heap approach is shorter, easier to prove, and comfortably fast at these constraints.

---

## Comparison with Day 36 (LC 3689, "I")

| Aspect | Day 36 ("I", Medium) | Day 37 ("II", Hard) |
|---|---|---|
| Repeats | Allowed | **Forbidden** — k distinct `(l, r)` |
| Best strategy | Whole array × k | k largest subarray values |
| Key insight | `value ≤ globalMax − globalMin` | `value(l, r)` monotone in `r` ⇒ n sorted chains |
| Machinery | One line of arithmetic | Max-heap + sparse tables |
| Complexity | O(n) | O((n + k) log n) |

The single word *distinct* turns a one-liner into a heap-on-sorted-chains problem — exactly the escalation predicted in Day 36's "Looking Ahead" section.

---

## Key Insights

| Insight | Explanation |
|---|---|
| **`value(l, r)` is monotone in `r`** | Widening a window can only raise the max and lower the min. |
| **n sorted chains, not 10⁹ candidates** | Each left end yields a descending sequence — k-largest-from-sorted-lists applies. |
| **Lazy expansion** | Only `n + k` subarrays are ever evaluated, out of ~1.25·10⁹. |
| **Sparse table = O(1) value queries** | Two overlapping power-of-two blocks answer range max/min instantly. |
| **Early exit at 0** | Values are non-negative; a zero at the heap top means nothing left matters. |

---

## Edge Cases

| Case | Behavior |
|---|---|
| All elements equal (`[7,7,7]`) | Every value is 0 → early exit → `0` |
| Single element, `k = 1` | Only `[l..l]`, value `0` |
| `k = n(n+1)/2` (take everything) | Heap drains every chain; sum of all values |
| Two elements (`[0, 10⁹]`, `k = 3`) | Values `0, 0, 10⁹` → total `10⁹` |
| Max constraints (`n=5·10⁴, k=10⁵`) | ~0.3 s in Python |

---

## Approach Tags

`Max-Heap` · `K Largest from Sorted Lists` · `Sparse Table` · `Lazy Expansion` · `Monotonicity`

---

*Day 37 of the LeetCode Daily Challenge*
