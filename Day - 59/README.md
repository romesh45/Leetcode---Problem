# Day 57 — LeetCode Challenge

## 3286. Find a Safe Walk Through a Grid

| Field | Details |
|---|---|
| **Difficulty** | Medium |
| **Topics** | 0-1 BFS · Shortest Path · Graph |
| **LeetCode Link** | [3286. Find a Safe Walk Through a Grid](https://leetcode.com/problems/find-a-safe-walk-through-a-grid/) |

---

## Problem Statement

Given an `m × n` binary grid and an integer `health`, start at `(0,0)` and reach `(m-1,n-1)`. Unsafe cells (`grid[i][j] = 1`) reduce health by 1 on entry. Return `true` if you can arrive with health ≥ 1.

---

## Examples

### Example 1
```
Input:  grid = [[0,1,0,0,0],[0,1,0,1,0],[0,0,0,1,0]], health = 1
Output: true
```
There exists a path that avoids all unsafe cells entirely.

### Example 2
```
Input:  grid = [[0,1,1,0,0,0],[1,0,1,0,0,0],[0,1,1,1,0,1],[0,0,1,0,1,0]], health = 3
Output: false
```
Minimum damage along any path is 4; health 3 is insufficient.

### Example 3
```
Input:  grid = [[1,1,1],[1,0,1],[1,1,1]], health = 5
Output: true
```
Only the center cell avoids damage; path through it costs 4 hits, leaving health = 1.

---

## Constraints

- `1 <= m, n <= 50`
- `1 <= health <= m + n`
- `grid[i][j]` is 0 or 1

---

## Intuition

### Reformulation

"Can I reach `(m-1,n-1)` with health ≥ 1?" is equivalent to:

> **Is the minimum total damage along any path strictly less than `health`?**

Each cell has an entry cost: `0` (safe) or `1` (unsafe). We want the minimum-cost path from `(0,0)` to `(m-1,n-1)`. This is a standard shortest-path problem.

### Why 0-1 BFS instead of Dijkstra

Edge weights are only 0 or 1 — a special case where **0-1 BFS** solves the problem in **O(m·n)** instead of Dijkstra's O(m·n·log(m·n)).

The key property: a deque maintains the BFS wavefront sorted by cost *for free*:
- Moving to a **safe cell** (cost 0) → push to **front** (no increase in cost)
- Moving to an **unsafe cell** (cost 1) → push to **back** (cost increases by 1)

`popleft()` always gives the cheapest unprocessed cell, exactly like Dijkstra but without a heap.

### The ` < health` condition

`cost[m-1][n-1]` = minimum hits taken on any path. We need to survive, so:

```
health - cost >= 1  ⟺  cost < health  ⟺  cost <= health - 1
```

---

## Algorithm

```
cost[0][0] = grid[0][0]    # starting cell may itself be unsafe
cost[all others] = ∞

deque = [(0, 0)]

while deque not empty:
    r, c = popleft()
    for each neighbour (nr, nc):
        new_cost = cost[r][c] + grid[nr][nc]
        if new_cost < cost[nr][nc]:
            cost[nr][nc] = new_cost
            if grid[nr][nc] == 1: append to BACK   (cost +1)
            else:                 appendleft FRONT  (cost +0)

return cost[m-1][n-1] < health
```

---

## Solution

```python
from typing import List
from collections import deque


class Solution:
    def findSafeWalk(self, grid: List[List[int]], health: int) -> bool:
        m, n = len(grid), len(grid[0])
        cost = [[float('inf')] * n for _ in range(m)]
        cost[0][0] = grid[0][0]

        dq = deque([(0, 0)])
        dirs = [(0,1),(0,-1),(1,0),(-1,0)]

        while dq:
            r, c = dq.popleft()
            for dr, dc in dirs:
                nr, nc = r + dr, c + dc
                if 0 <= nr < m and 0 <= nc < n:
                    new_cost = cost[r][c] + grid[nr][nc]
                    if new_cost < cost[nr][nc]:
                        cost[nr][nc] = new_cost
                        if grid[nr][nc] == 1:
                            dq.append((nr, nc))
                        else:
                            dq.appendleft((nr, nc))

        return cost[m - 1][n - 1] < health
```

---

## Complexity Analysis

| | Complexity | Reason |
|---|---|---|
| **Time** | **O(m·n)** | Each cell enters the deque at most twice (once per cost update); 0-1 BFS is linear |
| **Space** | **O(m·n)** | `cost` array + deque |

---

## Full Trace — Example 1: `grid = [[0,1,0,0,0],[0,1,0,1,0],[0,0,0,1,0]], health = 1`

Minimum-cost path (all zeros): `(0,0)→(1,0)→(2,0)→(2,1)→(2,2)→(2,3)→... `

One valid all-safe route: go down column 0, then right along row 2:
```
(0,0)→(1,0)→(2,0)→(2,1)→(2,2)→(1,2)→(0,2)→(0,3)→(0,4)→(1,4)→(2,4)
```
All cells are 0 → cost = 0. `0 < 1` → **True** ✓

---

## Full Trace — Example 3: `grid = [[1,1,1],[1,0,1],[1,1,1]], health = 5`

Every border cell is unsafe (cost 1). Only `(1,1)` is safe.
Minimum path: `(0,0)→(1,0)→(1,1)→(1,2)→(2,2)` — costs: 1+1+0+1+1 = 4.
`4 < 5` → **True** ✓

Any path avoiding `(1,1)` must cross more unsafe cells, costing ≥ 5.

---

## 0-1 BFS vs Dijkstra: Side-by-Side

| | 0-1 BFS | Dijkstra |
|---|---|---|
| Data structure | `deque` | `heapq` |
| Push (cost 0) | `appendleft` — O(1) | `heappush` — O(log n) |
| Push (cost 1) | `append` — O(1) | `heappush` — O(log n) |
| Total time | **O(V + E)** | O((V+E) log V) |
| Applicable when | Edge weights ∈ {0, 1} | Any non-negative weights |

For this problem, 0-1 BFS is always the right tool.

---

## Edge Cases

| Case | Behaviour |
|---|---|
| Start `(0,0)` is unsafe | `cost[0][0] = 1`; need `health ≥ 2` to even leave start |
| Single cell `[[0]]` | `cost[0][0] = 0 < health=1` → True |
| Single cell `[[1]]` | `cost[0][0] = 1`, need `1 < health` → False for health=1 |
| All cells safe | `cost[m-1][n-1] = 0 < health` → always True |
| All cells unsafe | Cost = path length = m+n-1; health ≤ m+n so barely feasible |

---

## Key Insights

| Insight | Explanation |
|---|---|
| **Reframe as min-cost path** | "Survive with ≥ 1 health" ↔ "absorb < health hits" ↔ shortest path |
| **0-1 BFS is optimal** | Binary edge weights → deque trick, O(mn) vs O(mn log mn) |
| **Front = free, back = cost** | Safe neighbour goes front (same cost level), unsafe goes back (+1 level) |
| **`cost < health` not `<=`** | Need 1 health remaining after damage, not 0 |

---

## Approach Tags

`0-1 BFS` · `Shortest Path` · `Deque` · `Grid Traversal`

---

*Day 57 of the LeetCode Daily Challenge*
