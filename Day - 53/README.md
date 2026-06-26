# Day 52 — LeetCode Challenge

## 3739. Count Subarrays With Majority Element II

| Field | Details |
|---|---|
| **Difficulty** | Hard |
| **Topics** | Array · Prefix Sum · Binary Indexed Tree · Coordinate Compression |
| **LeetCode Link** | [3739. Count Subarrays With Majority Element II](https://leetcode.com/problems/count-subarrays-with-majority-element-ii/) |

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

### Example 2
```
Input:  nums = [1,1,1,1], target = 1
Output: 10
```

### Example 3
```
Input:  nums = [1,2,3], target = 4
Output: 0
```

---

## Constraints

- `1 <= nums.length <= 10⁵`
- `1 <= nums[i] <= 10⁹`
- `1 <= target <= 10⁹`

---

## The Critical Difference from Part I

| | Part I | Part II |
|---|---|---|
| `n` | ≤ 1,000 | ≤ **100,000** |
| Viable strategy | O(n²) double loop | **O(n log n)** BIT |

The same prefix-sum reduction applies. What changes is how we count the valid pairs.

---

## Intuition

### Step 1 — ±1 reduction (same as Part I)

Map `nums[i]` → `+1` if it equals `target`, `−1` otherwise. Let:

```
prefix[0] = 0
prefix[k] = prefix[k-1] + mapped[k-1]
```

Then:
```
target is majority in nums[i..j]
  ⟺  sum(mapped[i..j]) > 0
  ⟺  prefix[j+1] - prefix[i] > 0
  ⟺  prefix[j+1] > prefix[i]
```

**Answer = number of index pairs (i, k) with `i < k` and `prefix[i] < prefix[k]`.**

This is exactly **counting non-inversions** in the prefix array.

### Step 2 — Why O(n²) fails here

With `n = 10⁵`, checking all pairs directly requires `n²/2 = 5 × 10⁹` operations. That's roughly 5 seconds — TLE.

### Step 3 — O(n log n) with a Fenwick Tree

Process prefix values **left to right** (index `k = 0` to `n`). Before inserting `prefix[k]`:

> **Query:** how many already-inserted prefix values are **strictly less than** `prefix[k]`?

Each such value corresponds to a valid left endpoint `i < k`, contributing to valid subarrays ending at `j = k − 1`.

A **Fenwick Tree (BIT)** over the value axis answers this in `O(log n)` per query and supports `O(log n)` point updates. Total: **O(n log n)**.

### Step 4 — Coordinate compression

Prefix values lie in `[−n, n]` (at most `2n + 1` distinct values). We can't index a BIT by raw value (up to `10⁵`). Instead:

1. Collect all `n + 1` prefix values.
2. Sort and deduplicate → `sorted_vals`.
3. Assign rank `1, 2, 3, …` to each unique value.
4. BIT operates on ranks (size ≤ `n + 1`).

"Count of prefix values < `prefix[k]`" = "count of ranks in `[1, rank(prefix[k]) − 1]`" = `BIT.query(rank − 1)`.

---

## Algorithm

```
Build prefix[0..n]  (±1 mapped sums)

Coordinate-compress prefix values → ranks 1..m

BIT of size m, initially all zeros

count = 0
for k = 0 to n:
    r = rank[prefix[k]]
    if k > 0:
        count += BIT.query(r - 1)   // # of seen prefixes < prefix[k]
    BIT.update(r)                   // insert prefix[k]

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

        sorted_vals = sorted(set(prefix))
        rank = {v: i + 1 for i, v in enumerate(sorted_vals)}
        m = len(sorted_vals)

        bit = [0] * (m + 1)

        def update(i: int) -> None:
            while i <= m:
                bit[i] += 1
                i += i & (-i)

        def query(i: int) -> int:
            s = 0
            while i > 0:
                s += bit[i]
                i -= i & (-i)
            return s

        count = 0
        for k in range(n + 1):
            r = rank[prefix[k]]
            if k > 0:
                count += query(r - 1)
            update(r)

        return count
```

---

## Complexity Analysis

| | Complexity | Reason |
|---|---|---|
| **Time** | **O(n log n)** | `n+1` iterations × O(log n) BIT query + update; compression sort O(n log n) |
| **Space** | **O(n)** | Prefix array + rank dict + BIT, all size O(n) |

Concrete: ~0.2s for `n = 10⁵`.

---

## Full Trace — Example 1: `nums = [1,2,2,3], target = 2`

**Mapped:** `[−1, +1, +1, −1]`

**Prefix:** `[0, −1, 0, 1, 0]`

**Sorted unique values:** `[−1, 0, 1]` → ranks: `{−1:1, 0:2, 1:3}`

| k | prefix[k] | rank r | query(r−1) | count | BIT after update |
|:-:|:-:|:-:|:-:|:-:|:-:|
| 0 | 0 | 2 | — (skip) | 0 | {2:1} |
| 1 | −1 | 1 | query(0)=0 | 0 | {1:1, 2:1} |
| 2 | 0 | 2 | query(1)=1 | 1 | {1:1, 2:2} |
| 3 | 1 | 3 | query(2)=3 | 4 | {1:1, 2:2, 3:1} |
| 4 | 0 | 2 | query(1)=1 | 5 | {1:1, 2:3, 3:1} |

**Answer: 5** ✓

*Reading the trace:* at `k=3` (prefix=1, rank=3), `query(2)` counts BIT positions 1 and 2 = `1 + 2 = 3`. This corresponds to the three left endpoints where prefix was `−1`, `0`, `0` — all strictly less than `1`.

---

## Full Trace — Example 2: `nums = [1,1,1,1], target = 1`

**Prefix:** `[0, 1, 2, 3, 4]`

**Ranks:** `{0:1, 1:2, 2:3, 3:4, 4:5}`

| k | prefix[k] | query(r−1) | count |
|:-:|:-:|:-:|:-:|
| 0 | 0 | — | 0 |
| 1 | 1 | query(1)=1 | 1 |
| 2 | 2 | query(2)=2 | 3 |
| 3 | 3 | query(3)=3 | 6 |
| 4 | 4 | query(4)=4 | 10 |

**Answer: 10** ✓ (Every subarray of an all-target array qualifies.)

---

## How the Fenwick Tree Works

A Fenwick Tree (BIT) stores counts at positions `1..m` and supports:

**Update `i`:** add 1 to position `i`, propagating up via `i += i & (-i)`.

**Query `i`:** sum positions `1..i`, accumulating via `i -= i & (-i)`.

Both operations touch at most `O(log m)` nodes. The key property: `i & (-i)` isolates the lowest set bit, giving the tree its efficient branching structure.

```
m = 5, after inserting ranks 2, 1, 2, 3, 2:

Rank:  1   2   3   4   5
Count: 1   3   1   0   0

BIT:   1   4   1   4   0   (internal representation, not raw counts)
```

`query(2)` = BIT[2] = 4 = count of values with rank ≤ 2. ✓

---

## Key Insights

| Insight | Explanation |
|---|---|
| **Same ±1 reduction** | Majority ↔ mapped sum > 0 ↔ prefix[j+1] > prefix[i] |
| **Count non-inversions** | Pairs (i,k) with i<k, prefix[i]<prefix[k] = standard BIT pattern |
| **Coordinate compression** | Prefix values in [−n,n]; compress to ranks for BIT indexing |
| **BIT over ranks** | O(log n) per query/update; total O(n log n) |
| **query(r−1) not query(r)** | Strict inequality: count values with rank < r, not ≤ r |

---

## Comparison: Part I vs Part II

| Aspect | Part I | Part II |
|---|---|---|
| n range | ≤ 1,000 | ≤ 100,000 |
| Core reduction | ±1 prefix sum | ±1 prefix sum (identical) |
| Counting method | O(n²) double loop | O(n log n) Fenwick Tree |
| Extra structure | None | Coordinate compression + BIT |

---

## Approach Tags

`Prefix Sum` · `±1 Encoding` · `Fenwick Tree` · `Coordinate Compression` · `Count Inversions`

---

*Day 52 of the LeetCode Daily Challenge*
