# Day 38 — LeetCode Challenge

## 3558. Number of Ways to Assign Edge Weights I

| Field | Details |
|---|---|
| **Difficulty** | Medium |
| **Topics** | Tree · BFS · Math · Parity Counting |
| **LeetCode Link** | [3558. Number of Ways to Assign Edge Weights I](https://leetcode.com/problems/number-of-ways-to-assign-edge-weights-i/) |

---

## Problem Statement

An undirected tree with `n` nodes labeled `1..n` is rooted at node `1`, given as `edges` (length `n − 1`). Every edge must be assigned a weight of **1 or 2**.

The **cost** of a path is the sum of its edge weights. Select any one node `x` at the **maximum depth**. Return the number of ways to assign weights to the edges **on the path from node 1 to `x`** so that the total cost is **odd**, modulo `10⁹ + 7`.

> Edges not on that path are ignored.

---

## Examples

### Example 1

```
Input:  edges = [[1,2]]
Output: 1
```

One edge on the path. Weight `1` → odd ✓; weight `2` → even ✗. One way.

### Example 2

```
Input:  edges = [[1,2],[1,3],[3,4],[3,5]]
Output: 2
```

Max depth is `2` (nodes 4 and 5). The path `1 → 3 → 4` has two edges; assignments `(1,2)` and `(2,1)` give odd cost. Two ways.

---

## Constraints

- `2 <= n <= 10⁵`
- `edges.length == n − 1`
- `edges` is a valid tree.

---

## Intuition

### Only the path *length* matters

We pick a deepest node `x` and only weight the edges on the root→`x` path. Say that path has **`d` edges** (`d` = maximum depth). Nothing about the tree's shape matters beyond `d` — every weighting question reduces to: *how many of the `d` edges get weight 1 vs 2?*

### Only *parity* matters

- Weight **1** is odd → flips the running parity.
- Weight **2** is even → leaves parity unchanged.

So the total cost is **odd ⇔ an odd number of edges receive weight 1**.

### Counting odd-sized subsets

The number of ways to pick which edges get weight 1 such that the count is odd:

```
C(d,1) + C(d,3) + C(d,5) + …  =  2^(d−1)
```

**The bijection proof** (why it's exactly half of all `2^d` assignments): take any assignment and **flip the first edge's weight** (1 ↔ 2). This toggles the total parity, and flipping twice returns the original — a perfect pairing between odd-cost and even-cost assignments. So exactly half of `2^d` are odd: **`2^(d−1)`**.

### So the algorithm is just…

1. **BFS from node 1** to find the maximum depth `d`.
2. Return **`2^(d−1) mod (10⁹ + 7)`**.

Which deepest node we "select" is irrelevant — all deepest paths have the same length `d`, and the formula depends only on `d`.

---

## Algorithm

```
build adjacency list
BFS level-by-level from node 1 → d = number of levels below the root
return pow(2, d - 1, 10^9 + 7)
```

---

## Solution

```python
from collections import deque
from typing import List


class Solution:
    def assignEdgeWeights(self, edges: List[List[int]]) -> int:
        MOD = 10**9 + 7
        n = len(edges) + 1
        adj = [[] for _ in range(n + 1)]
        for u, v in edges:
            adj[u].append(v)
            adj[v].append(u)

        depth = 0
        visited = [False] * (n + 1)
        visited[1] = True
        queue = deque([1])
        while queue:
            for _ in range(len(queue)):
                node = queue.popleft()
                for nxt in adj[node]:
                    if not visited[nxt]:
                        visited[nxt] = True
                        queue.append(nxt)
            if queue:
                depth += 1

        return pow(2, depth - 1, MOD)
```

---

## Complexity Analysis

| | Complexity | Reason |
|---|---|---|
| **Time** | **O(n)** | BFS touches each node/edge once; `pow(2, d−1, MOD)` is O(log d) |
| **Space** | **O(n)** | Adjacency list, visited array, BFS queue |

---

## Full Trace — Example 2: `edges = [[1,2],[1,3],[3,4],[3,5]]`

**Tree:**
```
        1
       / \
      2   3
         / \
        4   5
```

**BFS levels:** `{1}` → `{2, 3}` → `{4, 5}` ⟹ `d = 2`.

**Counting for the path `1 → 3 → 4` (2 edges):**

| edge (1,3) | edge (3,4) | total | parity |
|:-:|:-:|:-:|:-:|
| 1 | 1 | 2 | even ✗ |
| 1 | 2 | 3 | **odd ✓** |
| 2 | 1 | 3 | **odd ✓** |
| 2 | 2 | 4 | even ✗ |

Exactly **2** of the 4 assignments are odd = `2^(2−1)`. ✓

---

## Why Exactly Half — The Flip Bijection

Pair every assignment `A` with `A′` = "same as `A`, but edge #1's weight flipped (1 ↔ 2)":

- The flip changes the total by `±1` → **toggles parity**.
- `(A′)′ = A` → pairing is an involution, no fixed points.

Every pair `{A, A′}` contains exactly one odd-cost and one even-cost assignment. With `2^d` total assignments in `2^(d−1)` pairs, the odd-cost count is **`2^(d−1)`**. ∎

This argument is independent of `d ≥ 1` and needs no binomial summation.

---

## Edge Cases

| Case | Behavior |
|---|---|
| Two nodes (`[[1,2]]`) | `d = 1` → `2⁰ = 1` |
| Star (`[[1,2],[1,3]]`) | `d = 1` → `1` |
| Chain of length 10 | `d = 10` → `2⁹ = 512` |
| Very deep tree (`d ≈ 10⁵`) | `pow(2, d−1, MOD)` handles it instantly |
| Multiple deepest nodes | All deepest paths share the same `d` — formula unchanged |

---

## Validation

`solution.py` includes a brute-force parity check: for every `d` from 1 to 11, it enumerates all `2^d` weight assignments via `itertools.product((1,2), repeat=d)` and confirms the count of odd totals equals `2^(d−1)`.

```
brute-force parity check passed ✓
```

---

## Key Insights

| Insight | Explanation |
|---|---|
| **Only `d` matters** | The answer depends solely on the number of edges on the root→deepest path. |
| **Weights → parity bits** | Weight 1 = parity flip, weight 2 = no-op; odd cost ⇔ odd number of 1s. |
| **Odd-subset count = `2^(d−1)`** | Half of all assignments, by the first-edge flip bijection. |
| **BFS level count gives `d`** | Level-order traversal naturally tracks depth. |
| **Modular `pow` for huge `d`** | `d` can reach `10⁵`; fast exponentiation keeps it O(log d). |

---

## Approach Tags

`BFS Depth` · `Parity Argument` · `Bijection Counting` · `Modular Exponentiation`

---

*Day 38 of the LeetCode Daily Challenge*
