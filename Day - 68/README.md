# Day 63 — LeetCode Challenge

## 2685. Count the Number of Complete Components

| Field | Details |
|---|---|
| **Difficulty** | Medium |
| **Topics** | Graph · Union-Find · DFS/BFS |
| **LeetCode Link** | [2685. Count the Number of Complete Components](https://leetcode.com/problems/count-the-number-of-complete-components/) |

---

## Problem Statement

Given `n` vertices and a list of undirected edges, return the number of **complete** connected components — components where every pair of vertices shares a direct edge.

---

## Examples

### Example 1
```
Input:  n = 6, edges = [[0,1],[0,2],[1,2],[3,4]]
Output: 3
```
Components: `{0,1,2}` (K₃, 3 edges ✓), `{3,4}` (K₂, 1 edge ✓), `{5}` (K₁, 0 edges ✓).

### Example 2
```
Input:  n = 6, edges = [[0,1],[0,2],[1,2],[3,4],[3,5]]
Output: 1
```
`{3,4,5}` has 2 edges but needs 3 for K₃ — not complete.

---

## Constraints

- `1 <= n <= 50`
- No repeated edges, no self-loops

---

## Intuition

A connected component with `k` nodes is complete (a clique K_k) if and only if it has exactly `k*(k-1)/2` edges. We just need to count nodes and edges per component, then check the formula.

Union-Find groups all nodes by component in O(α·m) ≈ O(1) per operation, after which one scan of nodes and one scan of edges tallies both counts simultaneously.

---

## Solution

```python
from typing import List
from collections import defaultdict


class Solution:
    def countCompleteComponents(self, n: int, edges: List[List[int]]) -> int:
        parent = list(range(n))
        rank   = [0] * n

        def find(x: int) -> int:
            while parent[x] != x:
                parent[x] = parent[parent[x]]
                x = parent[x]
            return x

        def union(x: int, y: int) -> None:
            px, py = find(x), find(y)
            if px == py:
                return
            if rank[px] < rank[py]:
                px, py = py, px
            parent[py] = px
            if rank[px] == rank[py]:
                rank[px] += 1

        for a, b in edges:
            union(a, b)

        node_cnt = defaultdict(int)
        edge_cnt = defaultdict(int)
        for i in range(n):
            node_cnt[find(i)] += 1
        for a, b in edges:
            edge_cnt[find(a)] += 1

        return sum(
            1
            for root, k in node_cnt.items()
            if edge_cnt[root] == k * (k - 1) // 2
        )
```

---

## Complexity Analysis

| | Complexity | Reason |
|---|---|---|
| **Time** | **O(n + m)** | Union-Find builds in O(m·α), two linear scans for tallying |
| **Space** | **O(n)** | Parent/rank arrays + two counter dicts |

Effectively O(n + m) given n ≤ 50 and m ≤ n(n-1)/2.

---

## Edge Cases

| Case | Behaviour |
|---|---|
| Single isolated node | k=1, needs 0 edges → always complete |
| No edges at all | Every node is its own K₁ → answer = n |
| Complete graph Kₙ | One component, n*(n-1)/2 edges → answer = 1 |
| Two disjoint K₂s | Two components, each with 1 edge → answer = 2 |

---

## Approach Tags

`Union-Find` · `Clique Check` · `Graph`

---

*Day 63 of the LeetCode Daily Challenge*
