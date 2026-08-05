# Day 93 -- LeetCode Challenge

## 3310. Remove Methods From Project

| Field | Details |
|---|---|
| **Difficulty** | Medium |
| **Topics** | Graph -- BFS -- DFS |
| **LeetCode Link** | [3310. Remove Methods From Project](https://leetcode.com/problems/remove-methods-from-project/) |

---

## Problem Statement

Method `k` is buggy. A method is "suspicious" if it is `k` or reachable from `k` via the invocation graph. Remove the suspicious group only if no method outside it calls into it; otherwise return all methods unchanged.

---

## Examples

### Example 1
```
Input:  n=4, k=1, invocations=[[1,2],[0,1],[3,2]]
Output: [0,1,2,3]
```
Method 3 (not suspicious) calls method 2 (suspicious), blocking removal.

### Example 2
```
Input:  n=5, k=0, invocations=[[1,2],[0,2],[0,1],[3,4]]
Output: [3,4]
```
Methods 0,1,2 form an isolated suspicious group; safely removed.

### Example 3
```
Input:  n=3, k=2, invocations=[[1,2],[0,1],[2,0]]
Output: []
```
All methods are suspicious (cycle through k); all removed.

---

## Constraints

- `1 <= n <= 10^5`
- `0 <= invocations.length <= 2*10^5`

---

## Intuition

Two steps:

1. **Find the suspicious set** via BFS from `k` in the call graph (directed edges `a -> b` mean "a calls b").

2. **Check the boundary**: scan every edge. If any edge runs from a non-suspicious node to a suspicious node, removal is blocked (an outside method depends on the group). Return all methods unchanged.

3. **Otherwise**: return all non-suspicious methods.

---

## Solution

```python
from typing import List
from collections import deque, defaultdict


class Solution:
    def remainingMethods(self, n: int, k: int, invocations: List[List[int]]) -> List[int]:
        adj = defaultdict(list)
        for a, b in invocations:
            adj[a].append(b)

        suspicious = {k}
        queue = deque([k])
        while queue:
            node = queue.popleft()
            for nb in adj[node]:
                if nb not in suspicious:
                    suspicious.add(nb)
                    queue.append(nb)

        for a, b in invocations:
            if a not in suspicious and b in suspicious:
                return list(range(n))

        return [m for m in range(n) if m not in suspicious]
```

---

## Complexity Analysis

| | Complexity | Reason |
|---|---|---|
| **Time** | **O(n + m)** | BFS O(n+m); edge scan O(m); output O(n) |
| **Space** | **O(n + m)** | Adjacency list + visited set |

---

## Approach Tags

`BFS` -- `Graph Reachability` -- `Boundary Check`

---

*Day 87 of the LeetCode Daily Challenge*
