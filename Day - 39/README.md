# Day 39 — LeetCode Challenge

## 3559. Number of Ways to Assign Edge Weights II

| Field | Details |
|---|---|
| **Difficulty** | Hard |
| **Topics** | Tree · LCA · Binary Lifting · BFS · Parity Counting |
| **LeetCode Link** | [3559. Number of Ways to Assign Edge Weights II](https://leetcode.com/problems/number-of-ways-to-assign-edge-weights-ii/) |

---

## Problem Statement

Same setup as [version I (Day 38)](https://leetcode.com/problems/number-of-ways-to-assign-edge-weights-i/): an undirected tree with `n` nodes rooted at node `1`; every edge must get weight **1 or 2**; a path's cost is the sum of its edge weights.

**The twist:** you're given up to `10⁵` **queries** `[u, v]`. For each, count the ways to assign weights to the edges **on the path between `u` and `v`** so that the path cost is **odd**, modulo `10⁹ + 7`.

> Per query, edges off that path are ignored.

---

## Examples

### Example 1

```
Input:  edges = [[1,2]], queries = [[1,1],[1,2]]
Output: [0, 1]
```

- `[1,1]`: zero edges → cost `0` (even) → **0** ways.
- `[1,2]`: one edge → weight `1` works → **1** way.

### Example 2

```
Input:  edges = [[1,2],[1,3],[3,4],[3,5]], queries = [[1,4],[3,4],[2,5]]
Output: [2, 1, 4]
```

- `[1,4]`: 2 edges → `(1,2), (2,1)` → **2**.
- `[3,4]`: 1 edge → **1**.
- `[2,5]`: 3 edges (`2→1→3→5`) → `(1,2,2), (2,1,2), (2,2,1), (1,1,1)` → **4**.

---

## Constraints

- `2 <= n <= 10⁵`
- `edges.length == n − 1`; valid tree
- `1 <= queries.length <= 10⁵`  ← **the difference from "I"**

---

## Intuition

### The counting half is already solved

From Day 38: a path with `d` edges has an odd cost ⇔ an **odd number** of its edges receive weight 1, and the first-edge flip bijection shows exactly half of all `2^d` assignments qualify:

```
ways(d) = 2^(d−1)     for d ≥ 1
ways(0) = 0           (u == v: empty path, cost 0 is even)
```

Note the answers check out: `ways(2) = 2`, `ways(1) = 1`, `ways(3) = 4` — matching Example 2 exactly.

### The new problem: path length for arbitrary pairs, fast

Version I needed one path length (root → deepest). Now every query asks for the path length between **any** `u` and `v`. In a tree the path is unique and routes through the **lowest common ancestor**:

```
d(u, v) = depth[u] + depth[v] − 2 · depth[LCA(u, v)]
```

With `10⁵` queries, per-query BFS (O(n) each) would be `10¹⁰` work. We need LCA in **O(log n)** → **binary lifting**.

### Binary lifting in one paragraph

Precompute `up[j][v]` = the `2^j`-th ancestor of `v` (so `up[0]` is the parent, `up[1]` the grandparent's table, …) using `up[j][v] = up[j−1][up[j−1][v]]`. To find `LCA(u, v)`: (1) lift the deeper node up by the depth difference, decomposed into powers of two; (2) if they've met, done; otherwise lift **both** nodes by decreasing powers whenever their ancestors differ — they stop one step below the LCA, whose parent is the answer.

The root's parent is set to itself so over-lifting saturates harmlessly at the root.

### Precompute the powers of 2

`d` can reach `n − 1` and there are up to `10⁵` queries — precompute `pow2[i] = 2^i mod p` once instead of calling `pow()` per query.

---

## Algorithm

```
BFS from root → depth[], parent up[0][]
build up[j][v] = up[j-1][up[j-1][v]]            (LOG ≈ 17 levels)
precompute pow2[0..n-1]

for each query (u, v):
    w = LCA(u, v)                                O(log n)
    d = depth[u] + depth[v] − 2·depth[w]
    answer = 0 if d == 0 else pow2[d−1]
```

---

## Solution

```python
from collections import deque
from typing import List


class Solution:
    def assignEdgeWeights(self, edges: List[List[int]], queries: List[List[int]]) -> List[int]:
        MOD = 10**9 + 7
        n = len(edges) + 1
        adj = [[] for _ in range(n + 1)]
        for u, v in edges:
            adj[u].append(v)
            adj[v].append(u)

        LOG = max(1, n.bit_length())
        depth = [0] * (n + 1)
        up = [[0] * (n + 1) for _ in range(LOG)]

        visited = [False] * (n + 1)
        visited[1] = True
        up[0][1] = 1
        queue = deque([1])
        while queue:
            node = queue.popleft()
            for nxt in adj[node]:
                if not visited[nxt]:
                    visited[nxt] = True
                    depth[nxt] = depth[node] + 1
                    up[0][nxt] = node
                    queue.append(nxt)

        for j in range(1, LOG):
            upj, upj1 = up[j], up[j - 1]
            for v in range(1, n + 1):
                upj[v] = upj1[upj1[v]]

        def lca(u, v):
            if depth[u] < depth[v]:
                u, v = v, u
            diff = depth[u] - depth[v]
            j = 0
            while diff:
                if diff & 1:
                    u = up[j][u]
                diff >>= 1
                j += 1
            if u == v:
                return u
            for j in range(LOG - 1, -1, -1):
                if up[j][u] != up[j][v]:
                    u, v = up[j][u], up[j][v]
            return up[0][u]

        pow2 = [1] * n
        for i in range(1, n):
            pow2[i] = pow2[i - 1] * 2 % MOD

        ans = []
        for u, v in queries:
            d = depth[u] + depth[v] - 2 * depth[lca(u, v)]
            ans.append(0 if d == 0 else pow2[d - 1])
        return ans
```

---

## Complexity Analysis

| | Complexity | Reason |
|---|---|---|
| **Time** | **O((n + q) log n)** | BFS O(n); lifting table O(n log n); each query O(log n) |
| **Space** | **O(n log n)** | The `up` table (≈17 levels × 10⁵ nodes) |

Measured: a `10⁵`-node chain (worst depth) with `10⁵` queries finishes in **~0.25 s**.

---

## Full Trace — Example 2, Query `[2, 5]`

**Tree** (depths in parentheses):
```
        1 (0)
       / \
      2   3 (1)
     (1) / \
        4   5 (2)
```

1. `depth[2] = 1`, `depth[5] = 2` → swap so `u = 5, v = 2`; lift `u` by `diff = 1` → `u = 3`.
2. `3 ≠ 2` → scan powers downward: `up[j][3]` vs `up[j][2]` differ nowhere except at the end; both step to… `up[0][3] = 1`, `up[0][2] = 1` — equal, so no lift. **LCA = `up[0][3]` = 1**.
3. `d = 1 + 2 − 2·0 = 3` → `pow2[2] = 4`. ✓

Matches the official explanation's four assignments `(1,2,2), (2,1,2), (2,2,1), (1,1,1)` — all with an **odd number of 1s**.

---

## Why `d = depth[u] + depth[v] − 2·depth[LCA]`

The unique tree path `u → v` climbs from `u` up to the LCA, then descends to `v`:

- Climb: `depth[u] − depth[LCA]` edges.
- Descent: `depth[v] − depth[LCA]` edges.

Sum = `depth[u] + depth[v] − 2·depth[LCA]`. The LCA is precisely where the two root-paths fork, so no edge is counted twice and none missed. ∎

---

## Comparison with Day 38 (LC 3558, "I")

| Aspect | Day 38 ("I", Medium) | Day 39 ("II", Hard) |
|---|---|---|
| Paths asked | One — root to a deepest node | Up to `10⁵` arbitrary `(u, v)` pairs |
| Path length | One BFS, take max depth | `depth[u]+depth[v]−2·depth[LCA]` per query |
| Machinery | BFS only | BFS + binary-lifting LCA + pow2 table |
| Counting formula | `2^(d−1)` | Same — plus the `d = 0 → 0` case |
| Complexity | O(n) | O((n + q) log n) |

The parity insight is untouched; all the new difficulty is in answering **path-length queries** fast — a pure LCA exercise.

---

## Validation

`solution.py` cross-checks against a brute-force reference (per-query BFS distance) on **200 random trees × 20 queries each**, and times the adversarial chain case:

```
randomized cross-check passed ✓
n=1e5 chain, q=1e5 → 0.24s
```

---

## Key Insights

| Insight | Explanation |
|---|---|
| **`ways(d) = 2^(d−1)`, `ways(0) = 0`** | The Day-38 parity bijection, plus the empty-path special case. |
| **`d` via LCA** | Tree paths are unique and fork at the LCA: `d = depth[u]+depth[v]−2·depth[LCA]`. |
| **Binary lifting = O(log n) LCA** | `2^j`-ancestor table; lift to equal depth, then descend powers together. |
| **Root parent = itself** | Saturating lifts at the root removes all bounds-checking. |
| **Precompute `pow2`** | `10⁵` queries shouldn't each pay a modular exponentiation. |

---

## Edge Cases

| Case | Behavior |
|---|---|
| `u == v` | `d = 0` → answer `0` (the official Example 1 case) |
| `u` is an ancestor of `v` | LCA = `u`; `d = depth[v] − depth[u]` |
| Query endpoints in different branches | Path routes through the fork (LCA) |
| Chain tree (depth `n−1`) | Deepest lifting chains; still O(log n) per query |
| Repeated identical queries | Each computed independently (could memoize, unnecessary here) |

---

## Approach Tags

`LCA` · `Binary Lifting` · `Parity Argument` · `Modular Arithmetic` · `Tree Queries`

---

*Day 39 of the LeetCode Daily Challenge*
