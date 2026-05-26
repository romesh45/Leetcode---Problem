# Day 21 — LeetCode Challenge

## 1871. Jump Game VII

| Field | Details |
|---|---|
| **Difficulty** | Medium |
| **Topics** | BFS · Sliding Window · Dynamic Programming · Prefix Sum |
| **LeetCode Link** | [1871. Jump Game VII](https://leetcode.com/problems/jump-game-vii/) |

---

## Problem Statement

You are given a 0-indexed binary string `s` and two integers `minJump` and `maxJump`. You start at index `0` (guaranteed to be `'0'`). From index `i` you may jump to index `j` if:

- `i + minJump <= j <= min(i + maxJump, s.length - 1)`, **and**
- `s[j] == '0'`.

Return `true` if you can reach index `s.length − 1`, else `false`.

---

## Examples

### Example 1

```
Input:  s = "011010", minJump = 2, maxJump = 3
Output: true
```

Path: `0 → 3 → 5`.

### Example 2

```
Input:  s = "01101110", minJump = 2, maxJump = 3
Output: false
```

No sequence of jumps lands on the final `'0'` at index `7` (which is actually `'0'`, but the windows can't reach it without landing on a `'1'`).

---

## Constraints

- `2 <= s.length <= 10⁵`
- `s[i]` is `'0'` or `'1'`.
- `s[0] == '0'`
- `1 <= minJump <= maxJump < s.length`

---

## Intuition

### Reframe as graph reachability

Each index is a node. From index `i`, edges go to every `'0'`-index `j` in the window `[i + minJump, i + maxJump]`. The question is: **can we reach index `n − 1` from index `0`?**

That's pure single-source reachability — BFS or DFS handles it.

### The performance trap

A naïve BFS enumerates `[i + minJump, i + maxJump]` from every dequeued `i`. Windows overlap heavily — for `minJump = 1, maxJump = 10⁵`, every dequeued index scans nearly the whole array. Total work: **O(n · maxJump) ≈ 10¹⁰** on the constraint limits. TLE.

### The fix — a sliding `farthest` pointer

**Key observation:** BFS dequeues indices in non-decreasing order. So the windows we scan also have non-decreasing right endpoints. Once we've scanned indices up to position `f`, no later dequeue needs to re-scan anything ≤ `f`.

Maintain `farthest = max index already scanned`. The next effective scan starts at:

```
lo = max(i + minJump, farthest + 1)
```

This guarantees every index in `s` is examined **at most once** across the entire BFS → **O(n)** total work.

### Why the early exit on `j == n − 1` is correct

The instant any scan finds `n − 1` as a valid jump target, we've established reachability. BFS layering means this is the first time it's reached, and "any path" suffices — return `True` immediately, no extra dequeue needed.

### Quick edge case

If `s[n − 1] != '0'`, no path can ever land on the last index (the rule requires `s[j] == '0'`). Reject immediately.

---

## Algorithm

```
if s[-1] != '0': return False

queue   = [0]
farthest = 0

while queue:
    i = popleft
    lo = max(i + minJump, farthest + 1)
    hi = min(i + maxJump, n - 1)
    for j in lo..hi:
        if s[j] == '0':
            if j == n - 1: return True
            queue.append(j)
    farthest = max(farthest, hi)

return False
```

---

## Solution

```python
from collections import deque


class Solution:
    def canReach(self, s: str, minJump: int, maxJump: int) -> bool:
        n = len(s)
        if s[-1] != '0':
            return False

        queue = deque([0])
        farthest = 0

        while queue:
            i = queue.popleft()
            lo = max(i + minJump, farthest + 1)
            hi = min(i + maxJump, n - 1)
            for j in range(lo, hi + 1):
                if s[j] == '0':
                    if j == n - 1:
                        return True
                    queue.append(j)
            farthest = max(farthest, hi)

        return False
```

---

## Complexity Analysis

| | Complexity | Reason |
|---|---|---|
| **Time** | **O(n)** | The `farthest` pointer guarantees every index is scanned at most once across the entire BFS |
| **Space** | **O(n)** | BFS queue (worst case holds many indices) |

This passes comfortably at `n = 10⁵` where a naïve O(n · maxJump) approach TLE's.

---

## Full Trace — Example 1: `s = "011010", minJump = 2, maxJump = 3`

Indices: `0  1  2  3  4  5`
Chars:   `0  1  1  0  1  0`

| Step | Dequeue `i` | `lo` | `hi` | Scan range | `'0'` indices found | `farthest` |
|:-:|:-:|:-:|:-:|---|---|:-:|
| 1 | 0 | `max(0+2, 0+1) = 2` | `min(0+3, 5) = 3` | `[2, 3]` | `3` (enqueue) | 3 |
| 2 | 3 | `max(3+2, 3+1) = 5` | `min(3+3, 5) = 5` | `[5, 5]` | `5 == n−1` → **return True** ✓ | — |

Just 2 iterations.

---

## Full Trace — Example 2: `s = "01101110", minJump = 2, maxJump = 3`

Indices: `0  1  2  3  4  5  6  7`
Chars:   `0  1  1  0  1  1  1  0`

| Step | Dequeue `i` | `lo` | `hi` | Scan range | `'0'` indices found | `farthest` |
|:-:|:-:|:-:|:-:|---|---|:-:|
| 1 | 0 | `max(2, 1) = 2` | `min(3, 7) = 3` | `[2, 3]` | `3` (enqueue) | 3 |
| 2 | 3 | `max(5, 4) = 5` | `min(6, 7) = 6` | `[5, 6]` | none | 6 |
| 3 | queue empty | — | — | — | — | — |

We never reached `7`. Note that even though `s[7] = '0'`, no valid jump lands there. **Return False** ✓

---

## Why the `farthest` Pointer Is Correct

**Claim:** Skipping indices `≤ farthest` in subsequent scans never misses a reachable `'0'`.

**Proof.** Suppose we want to enqueue some `'0'` at index `j` from a future dequeue `i'`. The window of `i'` is `[i' + minJump, i' + maxJump]`. If `j ≤ farthest`, then `j` was already inside the scan range of some earlier dequeue `i ≤ i'` (the previous scan extended to `farthest ≥ j`). At that earlier scan, `j` was a `'0'` if and only if it's a `'0'` now (the string doesn't change), so it was already enqueued (or rejected as `'1'`). Either way, no information is lost by skipping it. ∎

---

## Alternative — DP with Prefix Sums

A purely iterative DP using prefix sums runs in the same O(n) time:

```python
def canReach(self, s, minJump, maxJump):
    n = len(s)
    if s[-1] != '0':
        return False

    dp = [False] * n
    dp[0] = True
    pre = [0] * (n + 1)    # pre[i] = number of True dp values in dp[0..i-1]
    pre[1] = 1             # dp[0] is True

    for i in range(1, n):
        if s[i] == '0':
            lo = max(0, i - maxJump)
            hi = i - minJump
            if hi >= lo:
                # Any True dp in [lo, hi] means dp[i] is reachable.
                dp[i] = pre[hi + 1] - pre[lo] > 0
        pre[i + 1] = pre[i] + (1 if dp[i] else 0)

    return dp[n - 1]
```

- `dp[i]` = "can we reach index `i`?"
- The prefix sum over `dp` lets the "is there any reachable predecessor in window `[i − maxJump, i − minJump]`?" check run in O(1).
- **Time:** O(n); **Space:** O(n).

Same asymptotic cost — pick whichever style you find clearer.

---

## Why a Naïve BFS Without `farthest` TLEs

Consider the input `s = "0" * 10⁵`, `minJump = 1`, `maxJump = 10⁵`.

- From index `0`: scan `[1, 10⁵−1]` → enqueue ~10⁵ indices.
- Then dequeue index `1` and scan `[2, 10⁵]` — almost identical range, all already visited.
- And again for index `2`, `3`, …

Without `farthest`, each dequeue rescans ~10⁵ positions → `10⁵ × 10⁵ = 10¹⁰` operations. With `farthest`, the very first dequeue advances `farthest` to `n − 1`, and every subsequent dequeue does O(1) work because `lo > hi` immediately.

That's why the pointer turns a quadratic algorithm into a linear one.

---

## Key Insights

| Insight | Explanation |
|---|---|
| **Reframe as reachability** | Each index → edges to `'0'` indices in `[i + minJump, i + maxJump]`. BFS solves it. |
| **Overlapping windows cause O(n²)** | Naïve BFS rescans the same indices repeatedly when windows overlap. |
| **`farthest` pointer ⇒ O(n)** | BFS dequeues indices monotonically; track the rightmost scanned index and never go back. |
| **`s[-1] != '0'` is the only rejection shortcut** | The destination must itself be `'0'` to be a valid landing. |
| **Early exit on `j == n − 1`** | Saves one queue rotation; correctness preserved by BFS layering. |

---

## Edge Cases

| Case | Behavior |
|---|---|
| `s = "00"`, `min = max = 1` | Window `[1, 1]`; `s[1] == '0'` and is the target → **True** |
| `s[-1] == '1'` | Impossible to land on the destination → **False** immediately |
| `s = "0" + "1" * (n−2) + "0"`, narrow window | All intermediates are `'1'`; if window can leap them in one jump → True, else False |
| Single-step zero corridor (`"0000…0"`, `min=max=1`) | BFS walks all the way → **True** |
| Very wide window (`min=1, max=n-1`) | First scan reaches `n − 1` directly → **True** |

---

## Approach Tags

`BFS` · `Sliding Frontier Pointer` · `Implicit Graph` · `Linear-Time Reachability`

---

*Day 21 of the LeetCode Daily Challenge*
