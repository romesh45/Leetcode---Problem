# Day 3 — LeetCode Challenge

## 3660. Jump Game IX

| Field | Details |
|---|---|
| **Difficulty** | Medium |
| **Topics** | Array, Stack, Union-Find, Monotonic Stack |
| **LeetCode Link** | [3660. Jump Game IX](https://leetcode.com/problems/jump-game-ix/) |

---

## Problem Statement

You are given an integer array `nums`.

From any index `i`, you can jump to another index `j` under these rules:

- **Forward jump** (`j > i`): allowed only if `nums[j] < nums[i]` (jump to a smaller value)
- **Backward jump** (`j < i`): allowed only if `nums[j] > nums[i]` (jump to a larger value)

For each index `i`, find the **maximum value** in `nums` reachable from `i` via any sequence of valid jumps.

Return an array `ans` where `ans[i]` is the maximum value reachable starting from index `i`.

---

## Examples

### Example 1

```
Input:  nums = [2, 1, 3]
Output: [2, 2, 3]
```

- `i = 0` (value 2): Forward jump needs value < 2. Only index 1 (value 1). From there, can go back to index 0. Can't reach index 2 (value 3 > 2, can't jump forward). **Max = 2**
- `i = 1` (value 1): Backward jump to index 0 (value 2 > 1). **Max = 2**
- `i = 2` (value 3): Global maximum, nothing to improve. **Max = 3**

### Example 2

```
Input:  nums = [2, 3, 1]
Output: [3, 3, 3]
```

- `i = 0` (value 2): Jump forward to index 2 (value 1 < 2), then backward to index 1 (value 3 > 1). **Max = 3**
- `i = 1` (value 3): Global maximum. **Max = 3**
- `i = 2` (value 1): Jump backward to index 1 (value 3 > 1). **Max = 3**

---

## Constraints

- `1 <= nums.length <= 10^5`
- `1 <= nums[i] <= 10^9`

---

## Intuition & Key Insight

### Step 1 — Model it as a graph

Two indices `a < b` can **directly reach each other** if and only if `nums[a] > nums[b]`:
- `a` can forward-jump to `b` since `nums[b] < nums[a]`
- `b` can backward-jump to `a` since `nums[a] > nums[b]`

Since every single jump is **reversible**, reachability is **symmetric** — this forms an **undirected graph**.

The answer for each index = **maximum value in its connected component**.

### Step 2 — Avoid O(n²) edges

Instead of checking every pair, we only need **two nearest-neighbor connections per index**:

| Connection | Description | How to find |
|---|---|---|
| **Previous Greater Element (PGE)** | Nearest `j < i` with `nums[j] > nums[i]` | Decreasing monotonic stack (left to right) |
| **Next Smaller Element (NSE)** | Nearest `j > i` with `nums[j] < nums[i]` | Increasing monotonic stack (right to left) |

These two edges per node are sufficient to reproduce **all** connected components.

### Step 3 — Union-Find

Merge components using Union-Find with:
- **Union by size** for balanced trees
- **Path compression** for fast lookups
- **Max value tracking** at each component root

---

## Solution

```python
from typing import List

class Solution:
    def maxValue(self, nums: List[int]) -> List[int]:
        n = len(nums)
        parent = list(range(n))
        size   = [1] * n
        mx     = nums[:]

        def find(x):
            while parent[x] != x:
                parent[x] = parent[parent[x]]
                x = parent[x]
            return x

        def union(x, y):
            rx, ry = find(x), find(y)
            if rx == ry:
                return
            if size[rx] < size[ry]:
                rx, ry = ry, rx
            parent[ry] = rx
            size[rx]  += size[ry]
            mx[rx]     = max(mx[rx], mx[ry])

        # Each entry = [component_root, MAX value in that entire component]
        # Key fix: we track component MAX, not just the element's own value
        # Stack stays non-decreasing in comp_max (bottom to top)
        stack = []

        for i in range(n):
            comp_max = nums[i]

            # Pop any component whose MAX > nums[i]
            # Reason: that component contains SOME element to the LEFT of i
            # with a LARGER value → direct connection → same component
            while stack and stack[-1][1] > nums[i]:
                rep, m = stack.pop()
                union(i, rep)
                comp_max = max(comp_max, m)   # absorb the popped component's max

            # Push merged component with its true maximum
            stack.append([find(i), comp_max])

        return [mx[find(i)] for i in range(n)]
```

---

## Complexity Analysis

| | Complexity |
|---|---|
| **Time** | O(n · α(n)) ≈ **O(n)** — two linear stack passes + near-constant Union-Find |
| **Space** | **O(n)** — parent, size, and max arrays + stack |

> α(n) is the inverse Ackermann function, effectively constant for all practical n.

---

## Dry Run — Example 2: `[2, 3, 1]`

**Pass 1 — PGE unions:**

| i | Value | Stack (before) | Action | Union |
|---|---|---|---|---|
| 0 | 2 | [] | No PGE | — |
| 1 | 3 | [0] | Pop 0 (2 ≤ 3), stack empty | — |
| 2 | 1 | [1] | 3 > 1, PGE = index 1 | union(2, 1) |

**Pass 2 — NSE unions:**

| i | Value | Stack (before) | Action | Union |
|---|---|---|---|---|
| 2 | 1 | [] | No NSE | — |
| 1 | 3 | [2] | 1 < 3, NSE = index 2 | union(1, 2) → already same |
| 0 | 2 | [2,1] | Pop 1 (3 ≥ 2), then 1 < 2, NSE = index 2 | union(0, 2) |

**Final components:** `{0, 1, 2}` → max = 3 → output `[3, 3, 3]` ✓

---

## Why Nearest Neighbors Are Enough

For any "long-range" edge `(a, b)` where `a < b` and `nums[a] > nums[b]`:
- Either `a` is the direct PGE of `b` → directly unioned
- Or there's an intermediate `c` with `a < c < b` where `nums[c] < nums[a]` and `c` is the PGE of `b`. Then `a` is connected to `c` (via NSE of `a`), and `c` is connected to `b` → same component transitively

The Cartesian-tree structure of the array guarantees this coverage is complete.

---

## Approach Tags

`Monotonic Stack` · `Union-Find` · `Graph Components` · `Greedy`

---

*Day 3 of the LeetCode Daily Challenge*
