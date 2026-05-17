# Day 13 — LeetCode Challenge

## 1306. Jump Game III

| Field | Details |
|---|---|
| **Difficulty** | Medium |
| **Topics** | BFS · DFS · Graph · Array |
| **LeetCode Link** | [1306. Jump Game III](https://leetcode.com/problems/jump-game-iii/) |

---

## Problem Statement

Given an array of non-negative integers `arr` and a starting index `start`, from any index `i` you may jump to either:

- `i + arr[i]`, or
- `i − arr[i]`

— provided the destination is **in bounds**.

Return `true` if you can reach **any** index whose value is `0`, otherwise `false`.

---

## Examples

### Example 1

```
Input:  arr = [4, 2, 3, 0, 3, 1, 2], start = 5
Output: true
```

One path: `5 → 4 → 1 → 3` (and `arr[3] = 0`).

### Example 2

```
Input:  arr = [4, 2, 3, 0, 3, 1, 2], start = 0
Output: true
```

Path: `0 → 4 → 1 → 3`.

### Example 3

```
Input:  arr = [3, 0, 2, 1, 2], start = 2
Output: false
```

The component reachable from index `2` never touches index `1` (where the zero lives).

---

## Constraints

- `1 <= arr.length <= 5 · 10⁴`
- `0 <= arr[i] < arr.length`
- `0 <= start < arr.length`

---

## Intuition

### This is a graph reachability problem in disguise

Model each index as a **node**. Each node `i` has at most **two outgoing edges**:

```
i ──► i + arr[i]
i ──► i − arr[i]
```

(both edges exist only when their destinations land in `[0, n)`).

The question becomes: **"Starting from node `start`, can we reach any node whose value is 0?"**

This is classic single-source reachability — BFS or DFS solves it in linear time.

### Why each index is visited at most once

Without a `visited` check, the search could loop forever (e.g., `arr = [1, 1]` would oscillate between indices `0 ↔ 1`). A single `visited[n]` boolean array fixes this and bounds the total work:

- `n` nodes, each enqueued at most once → `O(n)` node operations
- Each node fires at most 2 edges → `O(n)` edge operations

Total: **O(n) time, O(n) space**.

### Why BFS over DFS

Both work. Picking BFS because:
- **Iterative** — avoids Python's recursion depth limit at `n = 5·10⁴`.
- **Symmetric** — no asymmetry in edge ordering; the answer is just yes/no, so we don't need DFS's "explore one branch deeply" property.

A recursive DFS is equally valid (just guard depth or convert to iterative).

### When do we stop?

The moment we dequeue an index `i` with `arr[i] == 0`, we've found a path → return `True`. If the queue drains, every reachable index has been explored and none was zero → return `False`.

---

## Algorithm

```
visited = [False] * n
queue   = [start]
visited[start] = True

while queue not empty:
    i = pop front
    if arr[i] == 0:           return True
    for nxt in (i + arr[i], i - arr[i]):
        if in bounds and not visited[nxt]:
            visited[nxt] = True
            push nxt

return False
```

---

## Solution

```python
from collections import deque
from typing import List


class Solution:
    def canReach(self, arr: List[int], start: int) -> bool:
        n = len(arr)
        visited = [False] * n
        queue = deque([start])
        visited[start] = True

        while queue:
            i = queue.popleft()
            if arr[i] == 0:
                return True
            for nxt in (i + arr[i], i - arr[i]):
                if 0 <= nxt < n and not visited[nxt]:
                    visited[nxt] = True
                    queue.append(nxt)

        return False
```

---

## Complexity Analysis

| | Complexity | Reason |
|---|---|---|
| **Time** | **O(n)** | Each index enqueued/processed at most once; constant work per index |
| **Space** | **O(n)** | `visited` array + queue (worst case holds many indices) |

Well within limits for `n = 5·10⁴`.

---

## Full Trace — Example 1: `arr = [4, 2, 3, 0, 3, 1, 2], start = 5`

Indices: `0  1  2  3  4  5  6`
Values:  `4  2  3  0  3  1  2`

| Step | Dequeued `i` | `arr[i]` | Neighbors (`i+arr[i]`, `i−arr[i]`) | Enqueued | Visited |
|:-:|:-:|:-:|---|---|---|
| 1 | 5 | 1 | `6`, `4` | `[6, 4]` | `{5, 6, 4}` |
| 2 | 6 | 2 | `8` (oob), `4` (visited) | — | `{5, 6, 4}` |
| 3 | 4 | 3 | `7` (oob), `1` | `[1]` | `{5, 6, 4, 1}` |
| 4 | 1 | 2 | `3`, `−1` (oob) | `[3]` | `{5, 6, 4, 1, 3}` |
| 5 | 3 | **0** | — | — | **return True** ✓ |

---

## Full Trace — Example 3: `arr = [3, 0, 2, 1, 2], start = 2`

Indices: `0  1  2  3  4`
Values:  `3  0  2  1  2`

| Step | Dequeued `i` | `arr[i]` | Neighbors | Enqueued | Visited |
|:-:|:-:|:-:|---|---|---|
| 1 | 2 | 2 | `4`, `0` | `[4, 0]` | `{2, 4, 0}` |
| 2 | 4 | 2 | `6` (oob), `2` (visited) | — | `{2, 4, 0}` |
| 3 | 0 | 3 | `3`, `−3` (oob) | `[3]` | `{2, 4, 0, 3}` |
| 4 | 3 | 1 | `4` (visited), `2` (visited) | — | `{2, 4, 0, 3}` |
| 5 | — | queue empty | — | — | **return False** ✓ |

Index `1` (the only zero) was never reachable from the component containing `2`.

---

## DFS Alternative (Iterative)

```python
def canReach(self, arr, start):
    n = len(arr)
    visited = [False] * n
    stack = [start]
    while stack:
        i = stack.pop()
        if visited[i]:
            continue
        visited[i] = True
        if arr[i] == 0:
            return True
        for nxt in (i + arr[i], i - arr[i]):
            if 0 <= nxt < n and not visited[nxt]:
                stack.append(nxt)
    return False
```

Same `O(n)` time and space; LIFO instead of FIFO.

---

## Recursive DFS (compact but watch recursion depth)

```python
def canReach(self, arr, start):
    n = len(arr)
    def dfs(i):
        if not (0 <= i < n) or arr[i] < 0:
            return False
        if arr[i] == 0:
            return True
        step = arr[i]
        arr[i] = -arr[i]                        # mark visited in-place
        return dfs(i + step) or dfs(i - step)
    return dfs(start)
```

Clever trick: negate `arr[i]` in place to mark visited (saves the `visited` array). For `n` up to `5·10⁴`, raise the recursion limit if using Python.

---

## Key Insights

| Insight | Explanation |
|---|---|
| **It's just graph reachability** | Each index → at most 2 neighbors. Standard BFS/DFS solves it. |
| **`visited` is essential** | Without it, simple oscillations like `[1, 1]` loop forever. |
| **Goal check on dequeue** | Cleaner than checking before enqueue — and "starting on a zero" still works (`start` is enqueued first, dequeued first). |
| **Linear time matches the structure** | n nodes, ≤ 2n edges → BFS/DFS is `O(n)`. |
| **Negating-in-place is a neat optimization** | Marks visited without an extra array; only works because values are non-negative. |

---

## Edge Cases

| Case | Behavior |
|---|---|
| `arr = [0]`, `start = 0` | Dequeue `0`, `arr[0] == 0` → **True** |
| `start` already on a zero | Same as above — immediate return |
| `arr = [1, 1]`, `start = 0` | Visit `0 → 1`; both nonzero, queue drains → **False** |
| Single component with no zero | Drains the queue → **False** |
| All elements zero | First dequeue returns **True** |

---

## Approach Tags

`BFS` · `DFS` · `Graph Reachability` · `Visited Set`

---

*Day 13 of the LeetCode Daily Challenge*
