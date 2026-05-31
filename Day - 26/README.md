# Day 26 — LeetCode Challenge

## 3161. Block Placement Queries

| Field | Details |
|---|---|
| **Difficulty** | Hard |
| **Topics** | Segment Tree · Sorted Set · Offline/Online Queries · Binary Indexed Tree |
| **LeetCode Link** | [3161. Block Placement Queries](https://leetcode.com/problems/block-placement-queries/) |

---

## Problem Statement

There is an infinite number line starting at origin `0`, extending toward `+∞`. You're given a 2D array `queries` of two types:

- **Type 1** — `[1, x]`: build an obstacle at distance `x`. Guaranteed no obstacle already exists at `x`.
- **Type 2** — `[2, x, sz]`: check whether a block of size `sz` can be placed somewhere in `[0, x]` such that it lies **entirely** within `[0, x]` and does **not intersect** any obstacle. Touching an obstacle is allowed. The block is not actually placed — queries are independent.

Return a boolean array `results` where `results[i]` is the answer to the `i`-th **type-2** query.

---

## Examples

### Example 1

```
Input:  queries = [[1,2], [2,3,3], [2,3,1], [2,2,2]]
Output: [false, true, true]
```

- Build obstacle at `2`.
- `[2,3,3]`: largest free run in `[0,3]` is `[0,2]` (size 2) — can't fit size 3 → **false**.
- `[2,3,1]`: size 1 fits in `[0,2]` → **true**.
- `[2,2,2]`: `[0,2]` is size 2 → **true**.

### Example 2

```
Input:  queries = [[1,7], [2,7,6], [1,2], [2,7,5], [2,7,6]]
Output: [true, true, false]
```

- Build obstacle at `7`. `[2,7,6]`: `[0,7]` free (size 7) → **true**.
- Build obstacle at `2`. Now gaps are `[0,2]` (2) and `[2,7]` (5).
  - `[2,7,5]`: max gap `5 ≥ 5` → **true**.
  - `[2,7,6]`: max gap `5 < 6`, and the partial `7−7 = 0` → **false**.

---

## Constraints

- `1 <= queries.length <= 15·10⁴`
- `2 <= queries[i].length <= 3`
- `1 <= queries[i][0] <= 2`
- `1 <= x, sz <= min(5·10⁴, 3·queries.length)`
- Type-1 queries never duplicate an obstacle.
- At least one type-2 query exists.

---

## Intuition

### Obstacles carve the line into gaps

Obstacles partition `[0, ∞)` into intervals (gaps). A block of size `sz` fits in `[0, x]` iff some usable gap of length `≥ sz` lies inside `[0, x]`.

Add an **implicit obstacle at 0** (the left wall) so every gap has a left endpoint.

### Two kinds of usable gaps for a query `(x, sz)`

```
obstacles:  0 ........ o1 ...... o2 ...... o3 .......... x .... o4
            └── full ──┘└─ full ─┘└─ full ─┘└── partial ──┘
                                            (o3 → x, bounded by x not o4)
```

1. **Full gaps** — between two consecutive obstacles **both ≤ x**. These are entirely inside `[0, x]`.
2. **The trailing partial gap** — from the last obstacle `≤ x` up to the boundary `x` itself. Its right edge is `x`, not an obstacle.

**Answer = `max(largest full gap inside [0,x], partial gap) ≥ sz`.**

### Encoding full gaps in a segment tree

Store each full gap at its **right endpoint position**:

```
seg[p] = p − prev(p)     (gap ending at obstacle p)
```

Then a prefix max-query `seg.query(0, x)` returns the largest full gap whose right endpoint is `≤ x`. Crucially, gaps whose right endpoint exceeds `x` are **automatically excluded** — they're not fully inside `[0, x]`, and the trailing partial term handles whatever portion of them is usable.

### The trailing partial gap

```
last = largest obstacle ≤ x   (via the sorted set)
partial = x − last
```

This is the one piece the segment tree can't model, because its right boundary is the query limit `x`, not a stored obstacle.

### Insertion is a gap "split"

Building an obstacle at `x` lands inside an existing gap `(prev, nxt)` and **splits it in two**:

```
before:           prev ─────────── nxt        seg[nxt] = nxt − prev
after:  prev ──── x ──────── nxt               seg[x]   = x   − prev   (new)
                                               seg[nxt] = nxt − x      (shrunk)
```

Two point updates. Note that `seg[nxt]` **decreases** — that's exactly why a plain Fenwick (BIT) max tree doesn't work here (it only supports monotonic increases for prefix max). A **segment tree** with point assignment handles arbitrary updates.

---

## Algorithm

```
implicit obstacle at 0
seg = max-segment-tree over positions [0, MAXX]

for each query:
    type 1 [1, x]:
        prev = predecessor(x)
        seg[x] = x - prev
        if successor(x) = nxt exists:
            seg[nxt] = nxt - x
        insert x

    type 2 [2, x, sz]:
        full    = seg.query(0, x)
        last    = largest obstacle ≤ x
        partial = x - last
        answer  = max(full, partial) >= sz
```

---

## Solution

```python
from sortedcontainers import SortedList
from typing import List


class SegTree:
    def __init__(self, n):
        self.size = 1
        while self.size < n:
            self.size <<= 1
        self.tree = [0] * (2 * self.size)

    def update(self, i, val):
        i += self.size
        self.tree[i] = val
        i >>= 1
        while i:
            self.tree[i] = max(self.tree[2 * i], self.tree[2 * i + 1])
            i >>= 1

    def query(self, l, r):              # inclusive [l, r]
        res = 0
        l += self.size
        r += self.size + 1
        while l < r:
            if l & 1:
                res = max(res, self.tree[l]); l += 1
            if r & 1:
                r -= 1; res = max(res, self.tree[r])
            l >>= 1; r >>= 1
        return res


class Solution:
    def getResults(self, queries: List[List[int]]) -> List[bool]:
        MAXX = max(q[1] for q in queries)
        seg = SegTree(MAXX + 1)
        obstacles = SortedList([0])
        res = []

        for q in queries:
            if q[0] == 1:
                x = q[1]
                idx = obstacles.bisect_left(x)
                prev = obstacles[idx - 1]
                seg.update(x, x - prev)
                if idx < len(obstacles):
                    nxt = obstacles[idx]
                    seg.update(nxt, nxt - x)
                obstacles.add(x)
            else:
                x, sz = q[1], q[2]
                best = seg.query(0, x)
                last = obstacles[obstacles.bisect_right(x) - 1]
                partial = x - last
                res.append(max(best, partial) >= sz)

        return res
```

---

## Complexity Analysis

Let `n = len(queries)` and `M = max position`.

| | Complexity | Reason |
|---|---|---|
| **Time** | **O(n log M + n log n)** | Each query: O(log M) segment-tree op + O(log n) sorted-set op |
| **Space** | **O(n + M)** | Sorted set of obstacles + segment tree over positions |

With `n ≤ 1.5·10⁵` and `M ≤ 5·10⁴`, this is a few million operations — comfortably fast.

---

## Full Trace — Example 2: `[[1,7], [2,7,6], [1,2], [2,7,5], [2,7,6]]`

Start: `obstacles = {0}`, all `seg` zero.

| Query | Action | State after | Result |
|---|---|---|---|
| `[1,7]` | prev=0; `seg[7] = 7−0 = 7`; no successor | `{0, 7}`, seg[7]=7 | — |
| `[2,7,6]` | full = `query(0,7)` = `seg[7]=7`; last=7, partial=0; `max(7,0)=7 ≥ 6` | — | **true** |
| `[1,2]` | prev=0, nxt=7; `seg[2]=2−0=2`; `seg[7]=7−2=5` | `{0,2,7}`, seg[2]=2, seg[7]=5 | — |
| `[2,7,5]` | full = `query(0,7)` = max(2,5)=5; last=7, partial=0; `max(5,0)=5 ≥ 5` | — | **true** |
| `[2,7,6]` | full=5; partial=0; `max(5,0)=5 < 6` | — | **false** |

Output: `[true, true, false]` ✓

---

## Full Trace — Example 1: `[[1,2], [2,3,3], [2,3,1], [2,2,2]]`

| Query | Action | Result |
|---|---|---|
| `[1,2]` | prev=0; `seg[2]=2`; obstacles `{0,2}` | — |
| `[2,3,3]` | full=`query(0,3)`=seg[2]=2; last≤3 is 2, partial=3−2=1; `max(2,1)=2 < 3` | **false** |
| `[2,3,1]` | full=2, partial=1; `max(2,1)=2 ≥ 1` | **true** |
| `[2,2,2]` | full=`query(0,2)`=seg[2]=2; last≤2 is 2, partial=0; `max(2,0)=2 ≥ 2` | **true** |

Output: `[false, true, true]` ✓

---

## Why a Segment Tree, Not a Fenwick (BIT) Max?

A Fenwick tree for **prefix max** supports point updates and prefix queries — but only when updates are **monotonically increasing** (you can never lower a stored value, because the BIT max structure can't "un-propagate" a decrease).

Here, inserting an obstacle at `x` **shrinks** the successor's gap (`seg[nxt]` drops from `nxt−prev` to `nxt−x`). That's a decrease. A segment tree with arbitrary point assignment handles it cleanly; a Fenwick max would silently keep the stale larger value and produce wrong answers.

---

## Why "Right-Endpoint Storage + Partial Term" Is Correct

**Claim:** For query `(x, sz)`, the maximum usable gap inside `[0, x]` equals `max(seg.query(0, x), x − last(x))`.

**Proof sketch.**
- Any full gap between consecutive obstacles `o_{i-1} < o_i ≤ x` is stored at `seg[o_i]` with value `o_i − o_{i-1}`, and `o_i ≤ x` ⇒ it's counted by `query(0, x)`.
- A gap whose right obstacle `o > x` is **not** fully in `[0, x]`. The only usable portion is `[last, x]` where `last` is the largest obstacle `≤ x` — exactly the `partial` term.
- These two cases are exhaustive: every point in `[0, x]` belongs either to a full gap with right endpoint `≤ x`, or to the final `[last, x]` stretch.

Hence the maximum over both terms is the largest placeable block, and comparing to `sz` answers the query. ∎

---

## Key Insights

| Insight | Explanation |
|---|---|
| **Obstacles ⇒ gaps; the answer is the biggest gap ≤ x** | Reframes placement as a max-gap query bounded by `x`. |
| **Store gaps at their right endpoint** | Lets a prefix max-query naturally exclude gaps extending past `x`. |
| **The trailing `x − last` term** | Captures the partial gap the segment tree can't, since its right edge is `x`. |
| **Insertion splits one gap into two** | Two point updates — one new, one *decreased*. |
| **Decrease ⇒ segment tree, not Fenwick** | Fenwick max only supports increasing updates; the shrink rules it out. |

---

## Edge Cases

| Case | Behavior |
|---|---|
| No obstacles before a query | `last = 0`, `partial = x`; whole `[0, x]` is free |
| Obstacle exactly at boundary `x` | `partial = x − x = 0`; only full gaps count |
| Query before any type-1 query | Free space is `[0, x]` → fits iff `sz ≤ x` |
| `sz` larger than any gap and `> x` | Always **false** |
| Dense obstacles | Each gap small; `max` over them still O(log M) per query |

---

## Approach Tags

`Segment Tree (Point-Assign / Range-Max)` · `Sorted Set` · `Gap Modeling` · `Online Queries`

---

*Day 26 of the LeetCode Daily Challenge*
