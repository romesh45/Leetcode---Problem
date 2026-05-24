# Day 20 — LeetCode Challenge

## 1340. Jump Game V

| Field | Details |
|---|---|
| **Difficulty** | Hard |
| **Topics** | Dynamic Programming · DFS · Memoization · Implicit DAG · Sorting |
| **LeetCode Link** | [1340. Jump Game V](https://leetcode.com/problems/jump-game-v/) |

---

## Problem Statement

You're given an integer array `arr` and an integer `d`. From index `i` you may jump to index `j` if **all** of the following hold:

- `1 <= |i - j| <= d` (jump distance bounded by `d`)
- `j` stays in bounds (`0 <= j < n`)
- **`arr[i] > arr[j]`** (strictly higher → strictly lower)
- **`arr[i] > arr[k]` for every `k` strictly between `i` and `j`** (everything in the way must be lower than the launch height)

You may start at **any** index. Return the **maximum** number of indices you can visit (including the start).

---

## Examples

### Example 1

```
Input:  arr = [6, 4, 14, 6, 8, 13, 9, 7, 10, 6, 12], d = 2
Output: 4
```

Start at index `10` (value `12`): `10 → 8 → 6 → 7` visits 4 indices.

### Example 2

```
Input:  arr = [3, 3, 3, 3, 3], d = 3
Output: 1
```

Every jump requires a strict drop. All equal → no jumps possible from anywhere.

### Example 3

```
Input:  arr = [7, 6, 5, 4, 3, 2, 1], d = 1
Output: 7
```

Strictly decreasing — start at `0` and hop right through everything.

---

## Constraints

- `1 <= arr.length <= 1000`
- `1 <= arr[i] <= 10⁵`
- `1 <= d <= arr.length`

---

## Intuition

### Step 1: It's a DAG

Every legal jump goes from a higher value to a strictly lower one. Heights monotonically decrease along any path → **no cycles**. The implicit graph is a **directed acyclic graph**.

That instantly suggests:
- **Memoization** is safe (no infinite recursion possible).
- **Bottom-up DP** in increasing-height order is also possible.

### Step 2: Define the DP

Let `dfs(i)` = maximum number of indices reachable starting from `i` (counting `i` itself).

Recurrence:

```
dfs(i) = 1 + max(dfs(j))   over every legal j
       = 1   if no legal j exists
```

The final answer is `max(dfs(i))` over all `i`.

### Step 3: Enumerate neighbours cleanly

For each `i`, the legal `j`'s are at distance `1..d` to the **left and right**, with the strict-drop and clear-path rules.

Walk outward in each direction. The crucial observation:

> **If we hit any `arr[k] >= arr[i]` while extending in one direction, we can stop scanning that direction entirely.**

Why? Two reasons fire at once:
1. We can't land on `k` itself (needs `arr[i] > arr[k]`, strict).
2. We can't land on anything **past** `k` in that direction either — because that further `j` would have `k` strictly between `i` and `j`, and `arr[k] >= arr[i]` violates the "everything in between must be lower" rule.

So a single `break` correctly truncates the reachable range. The inner loop is `O(d)` worst case, not `O(d²)`.

### Step 4: Why the DAG view also gives a bottom-up solution

If we process indices in **ascending order of `arr` value**, then when we compute `dp[i]`, every `j` we might jump to has a **smaller** `arr[j]` — and so has already been processed. We can fill the table iteratively, no recursion needed. This avoids any recursion-limit concerns (chains can be up to `n` long).

---

## Algorithm (Top-Down DFS + Memo)

```
memo dfs(i):
    best = 1
    for j = i+1 .. min(i+d, n-1):
        if arr[j] >= arr[i]: break
        best = max(best, 1 + dfs(j))
    for j = i-1 .. max(i-d, 0):
        if arr[j] >= arr[i]: break
        best = max(best, 1 + dfs(j))
    return best

return max(dfs(i) for i in 0..n-1)
```

---

## Solution

```python
import sys
from functools import lru_cache
from typing import List


class Solution:
    def maxJumps(self, arr: List[int], d: int) -> int:
        n = len(arr)
        sys.setrecursionlimit(10_000)

        @lru_cache(maxsize=None)
        def dfs(i: int) -> int:
            best = 1
            for j in range(i + 1, min(i + d, n - 1) + 1):
                if arr[j] >= arr[i]:
                    break
                best = max(best, 1 + dfs(j))
            for j in range(i - 1, max(i - d, 0) - 1, -1):
                if arr[j] >= arr[i]:
                    break
                best = max(best, 1 + dfs(j))
            return best

        return max(dfs(i) for i in range(n))
```

---

## Complexity Analysis

| | Complexity | Reason |
|---|---|---|
| **Time** | **O(n · d)** | Each of `n` memoized states does up to `2d` work; each state computed once |
| **Space** | **O(n)** | Memo table; recursion depth up to `n` for strictly-decreasing chains |

For `n ≤ 1000, d ≤ 1000` this is at most `~10⁶` operations — trivial.

---

## Full Trace — Example 1: `arr = [6, 4, 14, 6, 8, 13, 9, 7, 10, 6, 12], d = 2`

We compute `dfs(i)` for each index; the answer is the max.

Let's expand the path the problem highlights: start at `i = 10` (value `12`).

**`dfs(10)`** — at index 10 (value 12)
- Right: out of bounds, nothing.
- Left, range `[8, 9]`:
  - `j = 9` (value 6): `6 < 12` ✓ → consider `1 + dfs(9)`
  - `j = 8` (value 10): `10 < 12` ✓ → consider `1 + dfs(8)`

**`dfs(8)`** — at index 8 (value 10)
- Right, range `[9, 10]`:
  - `j = 9` (value 6): `6 < 10` ✓ → `1 + dfs(9)`
  - `j = 10` (value 12): `12 >= 10` → **break**
- Left, range `[6, 7]`:
  - `j = 7` (value 7): `7 < 10` ✓ → `1 + dfs(7)`
  - `j = 6` (value 9): `9 < 10` ✓ → `1 + dfs(6)`

**`dfs(7)`** — at index 7 (value 7)
- Right, range `[8, 9]`:
  - `j = 8` (value 10): `10 >= 7` → **break**
- Left, range `[5, 6]`:
  - `j = 6` (value 9): `9 >= 7` → **break**
- → returns `1` (no jumps available)

**`dfs(6)`** — at index 6 (value 9)
- Right, range `[7, 8]`:
  - `j = 7` (value 7): `7 < 9` ✓ → `1 + dfs(7) = 2`
  - `j = 8` (value 10): `10 >= 9` → **break**
- Left, range `[4, 5]`:
  - `j = 5` (value 13): `13 >= 9` → **break**
- → returns `2`

**`dfs(9)`** — at index 9 (value 6)
- Right, range `[10]`: `12 >= 6` → break
- Left, range `[7, 8]`:
  - `j = 8` (value 10): `10 >= 6` → break
- → returns `1`

Back to **`dfs(8)`**: `max(1 + dfs(9), 1 + dfs(7), 1 + dfs(6)) = max(2, 2, 3) = 3`

Back to **`dfs(10)`**: `max(1 + dfs(9), 1 + dfs(8)) = max(2, 4) = 4` ✓

The DP correctly finds the optimal path `10 → 8 → 6 → 7` of length **4**.

---

## Full Trace — Example 3: `arr = [7, 6, 5, 4, 3, 2, 1], d = 1`

Strictly decreasing, `d = 1`. From any `i`, we can only step right to `i + 1` (strictly smaller).

- `dfs(6) = 1`
- `dfs(5) = 1 + dfs(6) = 2`
- `dfs(4) = 1 + dfs(5) = 3`
- ...
- `dfs(0) = 1 + dfs(1) = 7`

Answer: **7** ✓

---

## Bottom-Up Alternative (No Recursion)

Process indices in ascending order of `arr` value. When we compute `dp[i]`, every reachable `j` has already been computed (since `arr[j] < arr[i]`):

```python
def maxJumps(self, arr, d):
    n = len(arr)
    dp = [1] * n
    # Sort indices by ascending value
    order = sorted(range(n), key=lambda i: arr[i])
    for i in order:
        for j in range(i + 1, min(i + d, n - 1) + 1):
            if arr[j] >= arr[i]:
                break
            dp[i] = max(dp[i], 1 + dp[j])
        for j in range(i - 1, max(i - d, 0) - 1, -1):
            if arr[j] >= arr[i]:
                break
            dp[i] = max(dp[i], 1 + dp[j])
    return max(dp)
```

- **Time:** `O(n log n + n · d)`
- **Space:** `O(n)`
- **Recursion-free** — safer for deep DAG chains. Preferred for production code.

---

## Why the `break` Is Correct (Proof Sketch)

**Claim:** While extending from `i` in one direction, once we encounter index `k` with `arr[k] >= arr[i]`, no index past `k` (further from `i`) is reachable from `i`.

**Proof.** Suppose for contradiction some `j` past `k` were reachable from `i`. Then by the jump rule, every index strictly between `i` and `j` must satisfy `arr[i] > arr[m]`. But `k` is strictly between `i` and `j`, and `arr[k] >= arr[i]` — contradiction. So no such `j` exists, and we may break the loop. ∎

This is what reduces the per-state work from `O(d²)` (naive check-everything-between) to `O(d)`.

---

## Key Insights

| Insight | Explanation |
|---|---|
| **Strictly decreasing jumps ⇒ DAG** | No cycles → memoization safe and DP order is well-defined (sort by height). |
| **`break` on `arr[k] >= arr[i]`** | A single tall index blocks both itself and every further index in that direction. |
| **Try every starting index** | The starting choice is free — answer is `max(dfs(i))`. |
| **Bottom-up by ascending value** | Eliminates recursion-depth risk; same asymptotic complexity. |
| **Strict inequalities matter** | "Plateau" arrays like `[3,3,3,3,3]` allow zero jumps because `arr[i] > arr[j]` is **strict**. |

---

## Edge Cases

| Case | Behavior |
|---|---|
| `arr = [x]` (length 1) | No jumps possible → return `1` |
| All-equal array | No strict drops anywhere → answer `1` |
| Strictly decreasing array, `d = 1` | Walk it all → answer `n` |
| Strictly increasing array | Each start jumps nowhere except itself → answer `1` |
| `d` larger than `n` | Loops cap at array bounds — works unchanged |

---

## Approach Tags

`DP on DAG` · `Memoized DFS` · `Implicit Graph` · `Greedy Break` · `Sort-by-Height Bottom-Up`

---

*Day 20 of the LeetCode Daily Challenge*
