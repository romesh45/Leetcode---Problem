# Day 57 — LeetCode Challenge

## 3620. Network Recovery Pathways

| Field | Details |
|---|---|
| **Difficulty** | Hard |
| **Topics** | Graph · Topological Sort · Binary Search · Dynamic Programming |
| **LeetCode Link** | [3620. Network Recovery Pathways](https://leetcode.com/problems/network-recovery-pathways/) |

---

## Problem Statement

You are given a directed acyclic graph (DAG) of `n` nodes numbered 0 to `n − 1`. Edges are given as `edges[i] = [ui, vi, costi]`. Some nodes may be offline; `online[i]` indicates their status (`online[0]` and `online[n − 1]` are always `true`).

A path from 0 to `n − 1` is **valid** if:
- All **intermediate** nodes on the path are online.
- The **total recovery cost** of all edges does not exceed `k`.

For each valid path, its **score** is the minimum edge cost along that path. Return the **maximum path score** among all valid paths, or `-1` if none exist.

---

## Examples

### Example 1
```
Input:  edges = [[0,1,5],[1,3,10],[0,2,3],[2,3,4]], online = [true,true,true,true], k = 10
Output: 3
```
Path `0→1→3`: total cost 15 > 10, invalid. Path `0→2→3`: total cost 7 ≤ 10, score = min(3, 4) = **3**.

### Example 2
```
Input:  edges = [[0,1,7],[1,4,5],[0,2,6],[2,3,6],[3,4,2],[2,4,6]], online = [true,true,true,false,true], k = 12
Output: 6
```
Node 3 is offline, so `0→2→3→4` is invalid. Valid paths: `0→1→4` (score 5) and `0→2→4` (score 6). Max = **6**.

### Example 3
```
Input:  edges = [[0,1,5]], online = [true,true], k = 5
Output: 5
```
Single edge, total cost exactly equals `k`. Score = min(5) = **5**.

---

## Constraints

- `2 <= n <= 5 × 10⁴`
- `0 <= m == edges.length <= min(10⁵, n(n-1)/2)`
- `0 <= costi <= 10⁹`
- `0 <= k <= 5 × 10¹³`
- `online[0]` and `online[n-1]` are always `true`
- The graph is a directed acyclic graph

---

## Intuition

We want to **maximise the minimum edge cost** (bottleneck) while respecting a budget `k` and an offline-node constraint. Two ideas combine to solve this cleanly:

**1 — Binary search on the answer.**
The answer must be the cost of some actual edge (since it equals the minimum edge on some path). There are at most `m` unique costs, so we binary search over them. The key monotonicity property: if a valid path exists where every edge has cost ≥ `v`, it trivially also exists for any lower threshold `v' < v`. So `feasible(v)` is non-increasing in `v`, and binary search applies.

**2 — DAG DP as the feasibility check.**
Given a candidate minimum cost `v`, we need to answer: "Is there a path 0 → n-1 using only edges with cost ≥ `v`, through online intermediates, with total cost ≤ `k`?"

Since the graph is a DAG, we run one pass over its topological order:

```
dp[node] = minimum total cost to reach `node` from 0
            (using only allowed edges and online nodes)
```

Offline intermediate nodes are simply skipped — no cost is propagated through them. If `dp[n-1] ≤ k`, the candidate `v` is feasible.

The topological order is computed **once** and reused across all O(log m) binary search iterations.

---

## Solution

```python
from typing import List
from collections import deque


class Solution:
    def maxPathScore(self, n: int, edges: List[List[int]], online: List[bool], k: int) -> int:
        INF = float('inf')

        adj = [[] for _ in range(n)]
        in_deg = [0] * n
        for u, v, c in edges:
            adj[u].append((v, c))
            in_deg[v] += 1

        # Topological sort — computed once, reused in every feasibility check
        queue = deque(i for i in range(n) if in_deg[i] == 0)
        topo = []
        while queue:
            node = queue.popleft()
            topo.append(node)
            for v, _ in adj[node]:
                in_deg[v] -= 1
                if in_deg[v] == 0:
                    queue.append(v)

        last = n - 1

        def feasible(min_cost: int) -> bool:
            dp = [INF] * n
            dp[0] = 0
            for node in topo:
                if dp[node] == INF:
                    continue
                if node != 0 and node != last and not online[node]:
                    continue
                for v, c in adj[node]:
                    if c < min_cost:
                        continue
                    if v != last and not online[v]:
                        continue
                    new_cost = dp[node] + c
                    if new_cost < dp[v]:
                        dp[v] = new_cost
            return dp[last] <= k

        if not feasible(0):
            return -1

        costs = sorted(set(c for _, _, c in edges))
        lo, hi = 0, len(costs) - 1
        result = -1
        while lo <= hi:
            mid = (lo + hi) // 2
            if feasible(costs[mid]):
                result = costs[mid]
                lo = mid + 1
            else:
                hi = mid - 1

        return result
```

---

## Complexity Analysis

| | Complexity | Reason |
|---|---|---|
| **Time** | **O((n + m) log m)** | Topological sort O(n + m) once; binary search O(log m) iterations, each O(n + m) DAG DP |
| **Space** | **O(n + m)** | Adjacency list + DP array of size n |

For the given constraints (n ≤ 5 × 10⁴, m ≤ 10⁵, log m ≈ 17), this is roughly **2.5 × 10⁶ operations** — comfortably fast.

---

## Edge Cases

| Case | Behaviour |
|---|---|
| No edges | `feasible(0)` returns false immediately → `-1` |
| Single edge, total cost > k | `dp[n-1] > k` → returns `-1` |
| Single edge, total cost = k | Inclusive check `≤ k` passes → correct score returned |
| All intermediate nodes offline | Only direct 0→n-1 edge (if any) can form a valid path |
| Offline node with a bypass route | Offline node skipped in DP; cost propagated through the online bypass |
| Duplicate edge costs | `set(...)` deduplicates before binary search — no wasted iterations |

---

## Why Binary Search Is Exact

The answer is one of the edge costs in the graph (it is the minimum-cost edge on some valid path). We collect all unique edge costs, sort them, and binary search. The monotonicity proof:

> If `feasible(v)` is true, any path P that witnesses this uses only edges with cost ≥ v. Since v' < v implies those same edges have cost ≥ v', P also witnesses `feasible(v')`. ∴ `feasible` is non-increasing.

This guarantees we find the exact maximum feasible value.

---

## Approach Tags

`Binary Search on Answer` · `DAG DP` · `Topological Sort` · `Bottleneck Path`

---

*Day 57 of the LeetCode Daily Challenge*
