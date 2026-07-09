# Day 61 — LeetCode Challenge

## 3532. Path Existence Queries in a Graph I

| Field | Details |
|---|---|
| **Difficulty** | Medium |
| **Topics** | Array · Graph · Union-Find |
| **LeetCode Link** | [3532. Path Existence Queries in a Graph I](https://leetcode.com/problems/path-existence-queries-in-a-graph-i/) |

---

## Problem Statement

Given `n` nodes (0 to n-1) with a sorted array `nums`, an edge exists between nodes `i` and `j` when `|nums[i] - nums[j]| <= maxDiff`. For each query `[u, v]`, return whether a path between `u` and `v` exists.

---

## Examples

### Example 1
```
Input:  n = 2, nums = [1,3], maxDiff = 1, queries = [[0,0],[0,1]]
Output: [true, false]
```
`|1-3| = 2 > 1` — no edge, so node 0 and node 1 are in different components.

### Example 2
```
Input:  n = 4, nums = [2,5,6,8], maxDiff = 2, queries = [[0,1],[0,2],[1,3],[2,3]]
Output: [false, false, true, true]
```
Nodes 1,2,3 form one component (differences 1 and 2 ≤ 2). Node 0 is isolated (|2-5|=3 > 2).

---

## Constraints

- `1 <= n <= 10⁵`
- `0 <= nums[i] <= 10⁵`, sorted non-decreasing
- `0 <= maxDiff <= 10⁵`
- `1 <= queries.length <= 10⁵`

---

## Intuition

The problem looks like a general graph connectivity problem, but the **sorted `nums`** hides a powerful structure: **connected components are always contiguous index ranges**.

**Why?** For any indices `i < k < j`, the sorted order guarantees:
```
nums[i] <= nums[k] <= nums[j]
→ |nums[i] - nums[k]| <= |nums[i] - nums[j]|
```
So if nodes `i` and `j` are connected, every node `k` between them is reachable from `i` too. Components can never have "gaps".

**Consequence:** To determine all connected components, we only need to check **consecutive pairs**. Nodes `i` and `i+1` are in the same component if and only if `nums[i+1] - nums[i] <= maxDiff`. If this difference exceeds `maxDiff`, no node with index ≤ i can ever reach any node with index > i (all such gaps are at least as large).

This reduces the problem to one linear pass to assign group IDs, then O(1) per query.

---

## Solution

```python
from typing import List


class Solution:
    def pathExistenceQueries(self, n: int, nums: List[int], maxDiff: int,
                             queries: List[List[int]]) -> List[bool]:
        group = [0] * n
        for i in range(1, n):
            same = nums[i] - nums[i - 1] <= maxDiff
            group[i] = group[i - 1] if same else group[i - 1] + 1

        return [group[u] == group[v] for u, v in queries]
```

---

## Complexity Analysis

| | Complexity | Reason |
|---|---|---|
| **Time** | **O(n + q)** | One pass to build groups, O(1) per query |
| **Space** | **O(n)** | Group ID array |

---

## Edge Cases

| Case | Behaviour |
|---|---|
| `u == v` | Same group trivially → `true` |
| `maxDiff = 0` | Only nodes with identical values cluster together |
| All consecutive gaps ≤ maxDiff | All nodes in one component, all queries `true` |
| All consecutive gaps > maxDiff | Every node is isolated, queries `true` only when `u == v` |
| `n = 1` | Single node, only valid query is `[0,0]` → `true` |

---

## Why Not Union-Find?

Union-Find would also work here but it's overkill. Since components are contiguous ranges, a simple counter suffices — no need for parent arrays or path compression. The sorted input transforms a graph problem into a linear scan.

---

## Approach Tags

`Sorted Input` · `Contiguous Components` · `Linear Scan` · `Graph`

---

*Day 61 of the LeetCode Daily Challenge*
