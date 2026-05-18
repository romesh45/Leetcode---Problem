# Day 14 — LeetCode Challenge

## 1345. Jump Game IV

| Field | Details |
|---|---|
| **Difficulty** | Hard |
| **Topics** | BFS · Hash Map · Graph · Bucket Clearing |
| **LeetCode Link** | [1345. Jump Game IV](https://leetcode.com/problems/jump-game-iv/) |

---

## Problem Statement

You start at index `0` of an integer array `arr`. From index `i` you may jump to:

1. `i + 1` (if in bounds)
2. `i − 1` (if in bounds)
3. **Any** `j ≠ i` such that `arr[i] == arr[j]` — a "teleport" to any other index with the same value.

Return the **minimum** number of jumps to reach the last index `n − 1`. You may never jump outside the array.

---

## Examples

### Example 1

```
Input:  arr = [100, -23, -23, 404, 100, 23, 23, 23, 3, 404]
Output: 3
```

One optimal path: `0 → 4 → 3 → 9`
- `0 → 4` (teleport, both are `100`)
- `4 → 3` (i−1)
- `3 → 9` (teleport, both are `404`)

### Example 2

```
Input:  arr = [7]
Output: 0
```

Already at the last index.

### Example 3

```
Input:  arr = [7, 6, 9, 6, 9, 6, 9, 7]
Output: 1
```

Teleport `0 → 7` (both are `7`) in a single jump.

---

## Constraints

- `1 <= arr.length <= 5 · 10⁴`
- `-10⁸ <= arr[i] <= 10⁸`

---

## Intuition

### Shortest path on an implicit graph

Each index `i` is a node. Edges from `i`:

- `i ↔ i+1`
- `i ↔ i−1`
- `i ↔ j` for every `j ≠ i` with `arr[i] == arr[j]`

All edges have weight 1, so **BFS** finds the minimum number of jumps from `0` to `n − 1`.

### The pitfall: O(n²) blow-up

A naïve BFS that, at each dequeue, iterates all same-value indices runs into a wall:

```
arr = [7, 7, 7, …, 7]  (all 5·10⁴ sevens)
```

The first index visits all others (n − 1 work), and subsequent dequeues each re-walk that same list — total **O(n²) ≈ 2.5 · 10⁹ ops**. TLE.

### The fix: clear the bucket after first use

**Claim:** After we process the first index `i₀` with value `v = arr[i₀]`, BFS will have enqueued **every** other index sharing value `v`.

So when later we dequeue some other index `i₁` with `arr[i₁] = v`, iterating `buckets[v]` again would find every entry already visited — pure wasted work.

**Fix:** Clear `buckets[v]` after first use. Each value bucket is iterated at most **once**.

```python
buckets[arr[i]].clear()   # after enqueuing its neighbors
```

Total teleport-edge work across the whole BFS = sum of bucket sizes = **O(n)**.

### Goal-on-enqueue optimization

When generating neighbours, check `nxt == n − 1` **before** the visited test. Return `steps + 1` immediately — saves one queue rotation. Doesn't change the asymptotic complexity but is a clean micro-optimization.

---

## Algorithm

```
if n == 1: return 0

buckets = value → list of indices

queue = [(0, 0)]
visited = {0}

while queue:
    (i, steps) = pop_front
    for nxt in (i+1, i-1, *buckets[arr[i]]):
        if nxt == n - 1:        return steps + 1
        if nxt not visited:
            mark visited
            push (nxt, steps + 1)
    buckets[arr[i]].clear()     # ← the O(n) trick

return -1   # unreachable on valid inputs
```

---

## Solution

```python
from collections import defaultdict, deque
from typing import List


class Solution:
    def minJumps(self, arr: List[int]) -> int:
        n = len(arr)
        if n == 1:
            return 0

        buckets = defaultdict(list)
        for i, v in enumerate(arr):
            buckets[v].append(i)

        visited = [False] * n
        visited[0] = True
        queue = deque([(0, 0)])

        while queue:
            i, steps = queue.popleft()

            for nxt in self._neighbors(i, n, arr, buckets):
                if nxt == n - 1:
                    return steps + 1
                if not visited[nxt]:
                    visited[nxt] = True
                    queue.append((nxt, steps + 1))

            buckets[arr[i]].clear()

        return -1

    @staticmethod
    def _neighbors(i, n, arr, buckets):
        if i + 1 < n:
            yield i + 1
        if i - 1 >= 0:
            yield i - 1
        yield from buckets[arr[i]]
```

---

## Complexity Analysis

| | Complexity | Reason |
|---|---|---|
| **Time** | **O(n)** | Each index visited once; each bucket iterated once (cleared after first use). Linear moves contribute O(n) total. |
| **Space** | **O(n)** | `buckets` hash map, `visited` array, BFS queue |

The bucket-clear is what makes this linear instead of quadratic.

---

## Full Trace — Example 1: `arr = [100, -23, -23, 404, 100, 23, 23, 23, 3, 404]`

`n = 10`, target index = `9`.

**Buckets:**
```
100  → [0, 4]
-23  → [1, 2]
404  → [3, 9]
23   → [5, 6, 7]
3    → [8]
```

**BFS:**

| Step | Pop | Generated neighbors | Action |
|:-:|:-:|---|---|
| 1 | `(0, 0)` | `1` (i+1), `4` (teleport `100`) | enqueue `(1, 1)`, `(4, 1)`; clear `buckets[100]` |
| 2 | `(1, 1)` | `2`, `0` (visited), teleports `[1, 2]` (self + `2`) | enqueue `(2, 2)`; clear `buckets[-23]` |
| 3 | `(4, 1)` | `5`, `3`, teleports cleared | enqueue `(5, 2)`, `(3, 2)`; (bucket already empty) |
| 4 | `(2, 2)` | `3` (visited), `1` (visited), teleports cleared | — |
| 5 | `(5, 2)` | `6`, `4` (visited), teleports `[5,6,7]` | enqueue `(6,3)`, `(7,3)`; clear `buckets[23]` |
| 6 | `(3, 2)` | `4` (visited), `2` (visited), teleports `[3, 9]` → **`9` is target** | **return `2 + 1 = 3`** ✓ |

---

## Full Trace — Example 3: `arr = [7, 6, 9, 6, 9, 6, 9, 7]`

Target index = `7`.

**Buckets:**
```
7 → [0, 7]
6 → [1, 3, 5]
9 → [2, 4, 6]
```

**BFS:**

| Step | Pop | Neighbors |
|:-:|:-:|---|
| 1 | `(0, 0)` | `1` (i+1), teleports `[0, 7]` → **`7` is target** → **return `0 + 1 = 1`** ✓ |

A single jump suffices.

---

## What Breaks Without Bucket Clearing?

Consider `arr = [7, 7, 7, 7, 7, ..., 7]` of length `n`.

- BFS from index `0`: visits all `n − 1` other indices in one step.
- Then dequeues each of those `n − 1` indices, and for each, **re-walks the whole bucket** of size `n`.
- Total: **`n − 1` × `n` ≈ n² operations**.

With bucket clearing: the bucket is empty after the first dequeue → each subsequent dequeue does O(1) bucket work. Total: **O(n)**. The optimization is what moves this from TLE to AC.

---

## Why "Goal on Enqueue" Is Safe

We return as soon as `n − 1` appears as a neighbour. Could a *shorter* path exist that BFS would have found later? No — BFS explores in layers of increasing step count. The first time any layer touches `n − 1`, that's the minimum.

Returning on enqueue (vs. dequeue) only changes the constant — never the answer.

---

## Key Insights

| Insight | Explanation |
|---|---|
| **Each index → up to n−1 neighbors** | Same-value teleports can explode the edge count to `O(n²)` in adversarial cases. |
| **Bucket clearing → O(n) overall** | Each value's index list is iterated at most once across the whole BFS. |
| **BFS gives the shortest path for free** | All edges have weight 1; BFS layer = step count. |
| **Goal check on enqueue, not dequeue** | Tiny optimization: avoid one redundant pop. |
| **`n == 1` is the only "no jump needed" case** | Always handle it as an early return. |

---

## Alternative — Bidirectional BFS

For very tight time limits, bidirectional BFS (search from both `0` and `n − 1` simultaneously and meet in the middle) halves the effective layer depth. Same `O(n)` time, smaller constant. Code roughly doubles in size, so it's overkill here — the bucket-clear single-direction BFS is already comfortably within limits.

---

## Edge Cases

| Case | Behavior |
|---|---|
| `arr = [7]` | `n == 1` → return `0` immediately |
| `arr = [7, 7, ..., 7]` (all equal) | First step teleports to last → return `1` |
| `arr = [a, b]` (length 2) | `0 → 1` via `i+1` → return `1` |
| Last index has unique value | Reached only via `i ± 1` from a neighbour; BFS still finds shortest |
| Long stretch with no duplicates | Falls back to plain BFS over `i ± 1`; still O(n) |

---

## Approach Tags

`BFS` · `Hash Map` · `Bucket Clearing` · `Shortest Path` · `Implicit Graph`

---

*Day 14 of the LeetCode Daily Challenge*
