# Day 62 — LeetCode Challenge

## 3534. Path Existence Queries in a Graph II

| Field | Details |
|---|---|
| **Difficulty** | Hard |
| **Topics** | Array · Binary Search · Graph · Binary Lifting |
| **LeetCode Link** | [3534. Path Existence Queries in a Graph II](https://leetcode.com/problems/path-existence-queries-in-a-graph-ii/) |

---

## Problem Statement

Given `n` nodes with values `nums[i]`, edges exist between `i` and `j` when `|nums[i] - nums[j]| <= maxDiff`. For each query `[u, v]`, return the minimum number of hops between `u` and `v`, or `-1` if no path exists.

---

## Examples

### Example 1
```
Input:  n = 5, nums = [1,8,3,4,2], maxDiff = 3, queries = [[0,3],[2,4]]
Output: [1, 1]
```

### Example 2
```
Input:  n = 5, nums = [5,3,1,9,10], maxDiff = 2, queries = [[0,1],[0,2],[2,3],[4,3]]
Output: [1, 2, -1, 1]
```

### Example 3
```
Input:  n = 3, nums = [3,6,1], maxDiff = 1, queries = [[0,0],[0,1],[1,2]]
Output: [0, -1, -1]
```

---

## Constraints

- `1 <= n <= 10⁵`
- `0 <= nums[i] <= 10⁵`
- `0 <= maxDiff <= 10⁵`
- `1 <= queries.length <= 10⁵`

---

## Intuition

Contrast with Part I (3532), where `nums` was pre-sorted and only reachability was needed. Here, `nums` is unsorted and we need actual **hop distances**. BFS per query would be O(n × q) = 10¹⁰ — too slow.

### Step 1 — Sort by value

Sort nodes by `nums` value. Let `pos[v]` be node `v`'s position in sorted order. Now the graph has a clean structure: position `k` connects to every position `j` with `|svals[k] - svals[j]| <= maxDiff`, which is a **contiguous window** in sorted order.

### Step 2 — Key theorem: leftward steps never help

`right[k]` = rightmost sorted position reachable from `k` in one hop.

Since `svals` is non-decreasing, `right[k]` is also **non-decreasing** — higher positions have windows that extend at least as far right. This means:

> If we step left from position `i` to `i' < i`, then `right[i'] <= right[i]`. Any rightward jump we can make from `i'` is also reachable directly from `i`. So leftward detours never reduce the hop count.

Therefore: **minimum hops = minimum rightward jumps from `pos[u]` to `pos[v]`**.

### Step 3 — Binary lifting for O(log n) per query

This is now a classic **jump game**: starting at position `a`, make the fewest jumps to reach position `b`, where from position `k` you can jump to any position in `[k, right[k]]`.

Build a sparse table: `jump[p][k]` = rightmost position reachable from `k` in exactly `2^p` hops. Recurrence: `jump[p][k] = jump[p-1][jump[p-1][k]]`.

For each query, greedily take the largest power-of-2 jump that doesn't yet reach `b`, accumulate the hop count, then check if one final hop closes the gap.

---

## Solution

```python
from typing import List


class Solution:
    def pathExistenceQueries(self, n: int, nums: List[int], maxDiff: int,
                             queries: List[List[int]]) -> List[int]:
        LOG = 17

        order = sorted(range(n), key=lambda i: nums[i])
        svals = [nums[v] for v in order]
        pos = [0] * n
        for k, v in enumerate(order):
            pos[v] = k

        # right[k]: rightmost position reachable in 1 hop (two-pointer, O(n))
        right = [0] * n
        r = 0
        for k in range(n):
            r = max(r, k)
            while r + 1 < n and svals[r + 1] - svals[k] <= maxDiff:
                r += 1
            right[k] = r

        # Binary lifting table
        jump = [right[:]]
        for _ in range(1, LOG):
            prev = jump[-1]
            jump.append([prev[prev[k]] for k in range(n)])

        results = []
        for u, v in queries:
            a, b = pos[u], pos[v]
            if a > b:
                a, b = b, a
            if a == b:
                results.append(0)
                continue

            steps, cur = 0, a
            for p in range(LOG - 1, -1, -1):
                if jump[p][cur] < b:
                    steps += 1 << p
                    cur = jump[p][cur]

            results.append(steps + 1 if right[cur] >= b else -1)

        return results
```

---

## Complexity Analysis

| | Complexity | Reason |
|---|---|---|
| **Time** | **O((n + q) log n)** | Sort + two-pointer O(n log n); jump table O(n log n); O(log n) per query |
| **Space** | **O(n log n)** | Jump table has LOG × n entries |

For `n = q = 10⁵` and `LOG = 17`, this is roughly **3.4 × 10⁶** operations.

---

## Versus Part I

| | Part I (3532) | Part II (3534) |
|---|---|---|
| `nums` | Pre-sorted | Unsorted |
| Query type | Reachability (bool) | Minimum hops (int) |
| Approach | Group ID in O(n) | Sort + binary lifting |
| Per-query | O(1) | O(log n) |

---

## Edge Cases

| Case | Behaviour |
|---|---|
| `u == v` | `a == b` after sorting → return `0` |
| Equal `nums[u]` and `nums[v]` | Direct edge exists; `right[a] >= b`, 1 hop |
| Disconnected pair | After lifting, `right[cur] < b` → return `-1` |
| `maxDiff = 0`, all values distinct | Every `right[k] = k`; all pairs disconnected |
| `maxDiff` very large | All nodes connected; each `right[k] = n-1`; distance = 1 for any pair |

---

## Approach Tags

`Binary Lifting` · `Sort by Value` · `Sparse Table` · `Greedy Jump`

---

*Day 62 of the LeetCode Daily Challenge*
