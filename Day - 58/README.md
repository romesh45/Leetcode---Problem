# Day 56 — LeetCode Challenge

## 2812. Find the Safest Path in a Grid

| Field | Details |
|---|---|
| **Difficulty** | Medium |
| **Topics** | BFS · Binary Search · Graph |
| **LeetCode Link** | [2812. Find the Safest Path in a Grid](https://leetcode.com/problems/find-the-safest-path-in-a-grid/) |

---

## Problem Statement

Given an `n × n` grid where `1` marks a thief and `0` is empty, find the path from `(0,0)` to `(n-1,n-1)` that **maximises the minimum Manhattan distance** from any cell on the path to any thief. Return that maximum minimum distance (the **safeness factor**).

---

## Examples

### Example 1
```
Input:  grid = [[1,0,0],[0,0,0],[0,0,1]]
Output: 0
```
Both start and end cells are thieves — every path touches them.

### Example 2
```
Input:  grid = [[0,0,1],[0,0,0],[0,0,0]]
Output: 2
```
Best path stays 2 steps away from the thief at `(0,2)`.

### Example 3
```
Input:  grid = [[0,0,0,1],[0,0,0,0],[0,0,0,0],[1,0,0,0]]
Output: 2
```

---

## Constraints

- `1 <= n <= 400`
- Each cell is `0` or `1`; at least one thief exists

---

## Intuition

This is a **bottleneck path** problem: maximise the minimum value along a path. Two clean sub-problems combine:

1. **How far is each cell from the nearest thief?** → Multi-source BFS.
2. **Is there a path that only uses cells at distance ≥ k?** → Reachability BFS.
3. **What is the largest such k?** → Binary search.

---

## Step 1 — Multi-source BFS for distances

Launch BFS **simultaneously** from every thief. The level at which BFS first reaches a cell equals its Manhattan distance to the nearest thief.

```
dist[r][c] = 0     if grid[r][c] == 1
           = dist of nearest thief  otherwise
```

This runs in **O(n²)** — each cell is visited exactly once.

Why BFS gives Manhattan distance here: on a grid with 4-directional moves, BFS level = shortest path length = Manhattan distance (no obstacles are blocking the BFS itself).

---

## Step 2 — Reachability check for threshold k

Given the `dist` map, can we walk from `(0,0)` to `(n-1,n-1)` using only cells where `dist[r][c] >= k`?

Simple BFS on the filtered subgraph. Early exits:
- If `dist[0][0] < k` or `dist[n-1][n-1] < k`: immediately `False`.

Each check is **O(n²)**.

---

## Step 3 — Binary search on k

- **k = 0** is always reachable (any cell qualifies).
- **k = n** is never reachable (no cell can be n steps from a thief in an n×n grid).
- The feasibility is **monotone**: if k works, all smaller k also work.

Binary search over `[0, n]` with **O(log n)** iterations.

**Upper-mid binary search** (`mid = (lo+hi+1)//2`) avoids infinite loops when `lo = hi − 1`.

---

## Algorithm

```
# --- Multi-source BFS ---
dist = all -1
queue = all thief positions at distance 0
BFS level-by-level, setting dist[nr][nc] = dist[r][c] + 1

# --- Binary search ---
lo = 0, hi = n
while lo < hi:
    mid = (lo + hi + 1) // 2
    if can_reach(mid):
        lo = mid
    else:
        hi = mid - 1
return lo

# --- Feasibility check ---
def can_reach(k):
    if dist[0][0] < k or dist[n-1][n-1] < k: return False
    BFS from (0,0), only stepping to cells with dist >= k
    return (n-1, n-1) was reached
```

---

## Solution

```python
from typing import List
from collections import deque


class Solution:
    def maximumSafenessFactor(self, grid: List[List[int]]) -> int:
        n = len(grid)
        dist = [[-1] * n for _ in range(n)]
        q = deque()

        for r in range(n):
            for c in range(n):
                if grid[r][c] == 1:
                    dist[r][c] = 0
                    q.append((r, c))

        dirs = [(0,1),(0,-1),(1,0),(-1,0)]
        while q:
            r, c = q.popleft()
            for dr, dc in dirs:
                nr, nc = r+dr, c+dc
                if 0<=nr<n and 0<=nc<n and dist[nr][nc] == -1:
                    dist[nr][nc] = dist[r][c] + 1
                    q.append((nr, nc))

        def can_reach(k):
            if dist[0][0] < k or dist[n-1][n-1] < k:
                return False
            visited = [[False]*n for _ in range(n)]
            visited[0][0] = True
            bfs = deque([(0, 0)])
            while bfs:
                r, c = bfs.popleft()
                if r == n-1 and c == n-1:
                    return True
                for dr, dc in dirs:
                    nr, nc = r+dr, c+dc
                    if (0<=nr<n and 0<=nc<n
                            and not visited[nr][nc]
                            and dist[nr][nc] >= k):
                        visited[nr][nc] = True
                        bfs.append((nr, nc))
            return False

        lo, hi = 0, n
        while lo < hi:
            mid = (lo + hi + 1) // 2
            if can_reach(mid):
                lo = mid
            else:
                hi = mid - 1
        return lo
```

---

## Complexity Analysis

| | Complexity | Reason |
|---|---|---|
| **Time** | **O(n² log n)** | BFS once O(n²) + log(n) checks each O(n²) |
| **Space** | **O(n²)** | `dist` array + BFS visited arrays |

Concrete: ~0.22s for `n = 400`.

---

## Full Trace — Example 2: `grid = [[0,0,1],[0,0,0],[0,0,0]]`

**Thief at (0,2). Multi-source BFS produces:**

```
dist:
2  1  0
3  2  1
4  3  2
```

**Binary search over [0, 3]:**

| mid | can_reach(mid) | lo / hi |
|:-:|:-:|:-:|
| 2 | True (path (0,0)→(1,0)→(2,0)→…→(2,2), all dist≥2) | lo=2 |
| 3 | False (dist[0][0]=2 < 3) | hi=2 |

**Answer: 2** ✓

---

## Why Not Dijkstra?

A "max-min path" (widest path / bottleneck path) can also be solved with a max-heap Dijkstra where the "cost" is the minimum dist along the path so far. It's also O(n² log n) and avoids binary search, but binary search + BFS is simpler to reason about and implement correctly.

Both are valid; binary search wins on clarity here.

---

## Edge Cases

| Case | Behaviour |
|---|---|
| Start `(0,0)` is a thief | `dist[0][0]=0`, `can_reach(1)` fails → answer 0 |
| End `(n-1,n-1)` is a thief | Same: answer 0 |
| Single thief far from any path | High answer; BFS distributes distance correctly |
| Dense thieves | dist values mostly 0 or 1; answer likely 0 or 1 |

---

## Key Insights

| Insight | Explanation |
|---|---|
| **Multi-source BFS** | Compute all distances in one O(n²) pass |
| **Monotone feasibility** | If k-safe path exists, (k-1)-safe path also exists → binary search applies |
| **Upper-mid in binary search** | `(lo+hi+1)//2` prevents infinite loop at `lo = hi−1` |
| **Early exit in can_reach** | Checking endpoints first avoids full BFS in obvious cases |

---

## Approach Tags

`Multi-source BFS` · `Binary Search` · `Bottleneck Path` · `Graph Reachability`

---

*Day 56 of the LeetCode Daily Challenge*
