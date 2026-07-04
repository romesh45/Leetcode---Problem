# Day 58 — LeetCode Challenge

## 2492. Minimum Score of a Path Between Two Cities

| Field | Details |
|---|---|
| **Difficulty** | Medium |
| **Topics** | Graph · BFS · Union-Find |
| **LeetCode Link** | [2492. Minimum Score of a Path Between Two Cities](https://leetcode.com/problems/minimum-score-of-a-path-between-two-cities/) |

---

## Problem Statement

Given `n` cities (numbered 1 to `n`) and a list of bidirectional roads `roads[i] = [ai, bi, distancei]`, find the **minimum possible score** of any path between cities 1 and `n`. The score of a path is its minimum edge distance. Roads may be traversed multiple times and cities may be revisited.

---

## Examples

### Example 1
```
Input:  n = 4, roads = [[1,2,9],[2,3,6],[2,4,5],[1,4,7]]
Output: 5
```
Path `1→2→4`, score = min(9, 5) = **5**.

### Example 2
```
Input:  n = 4, roads = [[1,2,2],[1,3,4],[3,4,7]]
Output: 2
```
Path `1→2→1→3→4`, score = min(2, 2, 4, 7) = **2**.

---

## Constraints

- `2 <= n <= 10⁵`
- `1 <= roads.length <= 10⁵`
- `1 <= distancei <= 10⁴`
- There is at least one path between city 1 and city n

---

## Intuition

The problem looks like a shortest-path variant, but the critical detail is:

> Roads can be traversed multiple times and cities can be revisited freely.

This single rule collapses the problem. If city 1 and city n are in the same connected component (guaranteed), then **any edge in that component is reachable on a valid path**. Here's why:

For any edge `(a, b, d)` in the component, we can always build:

```
1 → ... → a → b → a → ... → n
```

using known connections within the component and retracing roads as needed. So the minimum score is simply the **minimum edge weight in the connected component containing city 1** (which also contains city n by the problem guarantee).

No Dijkstra, no DP — just find the component, scan its edges.

---

## Solution

```python
from typing import List
from collections import deque


class Solution:
    def minScore(self, n: int, roads: List[List[int]]) -> int:
        adj = [[] for _ in range(n + 1)]
        for a, b, d in roads:
            adj[a].append((b, d))
            adj[b].append((a, d))

        # BFS from city 1 to find every node in its connected component
        visited = {1}
        queue = deque([1])
        while queue:
            node = queue.popleft()
            for neighbor, _ in adj[node]:
                if neighbor not in visited:
                    visited.add(neighbor)
                    queue.append(neighbor)

        # Minimum edge weight in the component
        return min(d for a, b, d in roads if a in visited)
```

---

## Complexity Analysis

| | Complexity | Reason |
|---|---|---|
| **Time** | **O(n + m)** | BFS visits each node and edge once; final scan is O(m) |
| **Space** | **O(n + m)** | Adjacency list + visited set + BFS queue |

---

## Edge Cases

| Case | Behaviour |
|---|---|
| Single edge `1 → n` | BFS visits both; that edge's distance is the answer |
| All nodes in one component | Minimum over all road distances |
| Disconnected graph | BFS only reaches the component of city 1; edges outside it are ignored (problem guarantees city n is reachable) |

---

## Alternative: Union-Find

DSU is another clean O(α · m) approach — union all edges, then scan roads whose root matches `find(1)`. BFS is chosen here for readability, but DSU is equally valid and marginally faster for large inputs.

---

## Approach Tags

`BFS` · `Connected Component` · `Graph`

---

*Day 58 of the LeetCode Daily Challenge*
