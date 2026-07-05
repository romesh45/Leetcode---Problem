# Day 59 — LeetCode Challenge

## 1301. Number of Paths with Max Score

| Field | Details |
|---|---|
| **Difficulty** | Hard |
| **Topics** | Array · Dynamic Programming · Matrix |
| **LeetCode Link** | [1301. Number of Paths with Max Score](https://leetcode.com/problems/number-of-paths-with-max-score/) |

---

## Problem Statement

Given an `n × n` character board, start at `'S'` (bottom-right) and reach `'E'` (top-left). Moves: **up**, **left**, **up-left (diagonal)**. Obstacles `'X'` block movement. Cells `'1'–'9'` yield their digit value; `'E'` and `'S'` yield 0.

Return `[maximum_score, number_of_paths_achieving_that_score]` modulo `10⁹ + 7`. If unreachable return `[0, 0]`.

---

## Examples

### Example 1
```
Input:  board = ["E23","2X2","12S"]
Output: [7, 1]
```

### Example 2
```
Input:  board = ["E12","1X1","21S"]
Output: [4, 2]
```
Two paths tie at score 4.

### Example 3
```
Input:  board = ["E11","XXX","11S"]
Output: [0, 0]
```
Middle row is all obstacles — no path exists.

---

## Constraints

- `2 <= board.length == board[i].length <= 100`

---

## Intuition

### Direction of DP

We travel from `S = (n-1, n-1)` toward `E = (0, 0)` using moves: up `(-1,0)`, left `(0,-1)`, diagonal `(-1,-1)`.

Flip the perspective: cell `(r,c)` can be reached **from** cells `(r+1,c)`, `(r,c+1)`, `(r+1,c+1)`. Process cells from **bottom-right to top-left** so all predecessors are computed before the current cell.

### Two-value DP

Track two quantities simultaneously for each cell:

```
dp_score[r][c] = maximum score on any path from S to (r, c)
dp_count[r][c] = number of paths achieving that maximum
```

**Transition:** for each predecessor `(pr, pc)` in `{(r+1,c), (r,c+1), (r+1,c+1)}`:

```
candidate = dp_score[pr][pc] + val(r, c)

if candidate > dp_score[r][c]:
    dp_score[r][c] = candidate
    dp_count[r][c] = dp_count[pr][pc]
elif candidate == dp_score[r][c]:
    dp_count[r][c] += dp_count[pr][pc]   (mod 10^9+7)
```

This is the standard "count paths achieving optimal value" pattern.

### Base case and answer

- `dp_score[n-1][n-1] = 0`, `dp_count[n-1][n-1] = 1` — one way to stand at `S` with score 0.
- Answer: `[dp_score[0][0], dp_count[0][0]]`, or `[0, 0]` if `dp_score[0][0]` is still `−∞`.

---

## Algorithm

```
dp_score = all −∞  (unreachable)
dp_count = all 0
dp_score[n-1][n-1] = 0
dp_count[n-1][n-1] = 1

for r from n-1 downto 0:
    for c from n-1 downto 0:
        skip if (r,c) == (n-1,n-1) or board[r][c] == 'X'
        val = digit value of board[r][c]  (0 for E and S)
        
        for (pr,pc) in {(r+1,c),(r,c+1),(r+1,c+1)}:
            if in bounds and dp_score[pr][pc] != −∞:
                merge (dp_score[pr][pc] + val, dp_count[pr][pc])

if dp_score[0][0] == −∞: return [0,0]
return [dp_score[0][0], dp_count[0][0]]
```

---

## Solution

```python
from typing import List

MOD = 10**9 + 7


class Solution:
    def pathsWithMaxScore(self, board: List[str]) -> List[int]:
        n = len(board)
        NEG_INF = float('-inf')

        dp_score = [[NEG_INF] * n for _ in range(n)]
        dp_count = [[0] * n for _ in range(n)]
        dp_score[n - 1][n - 1] = 0
        dp_count[n - 1][n - 1] = 1

        for r in range(n - 1, -1, -1):
            for c in range(n - 1, -1, -1):
                if r == n - 1 and c == n - 1:
                    continue
                if board[r][c] == 'X':
                    continue

                val = 0 if board[r][c] in ('E', 'S') else int(board[r][c])
                best_score = NEG_INF
                best_count = 0

                for dr, dc in [(1, 0), (0, 1), (1, 1)]:
                    pr, pc = r + dr, c + dc
                    if 0 <= pr < n and 0 <= pc < n:
                        if dp_score[pr][pc] == NEG_INF:
                            continue
                        s = dp_score[pr][pc] + val
                        cnt = dp_count[pr][pc]
                        if s > best_score:
                            best_score = s
                            best_count = cnt
                        elif s == best_score:
                            best_count = (best_count + cnt) % MOD

                if best_score != NEG_INF:
                    dp_score[r][c] = best_score
                    dp_count[r][c] = best_count % MOD

        if dp_score[0][0] == NEG_INF:
            return [0, 0]
        return [dp_score[0][0], dp_count[0][0]]
```

---

## Complexity Analysis

| | Complexity | Reason |
|---|---|---|
| **Time** | **O(n²)** | Each of the n² cells processed once with O(1) work (3 predecessors) |
| **Space** | **O(n²)** | Two n×n DP arrays |

Runs in ~0.01s for n=100 (max constraint).

---

## Full Trace — Example 2: `board = ["E12","1X1","21S"]`

```
(0,0)=E  (0,1)=1  (0,2)=2
(1,0)=1  (1,1)=X  (1,2)=1
(2,0)=2  (2,1)=1  (2,2)=S
```

| Cell | val | Predecessors used | dp_score | dp_count |
|:-:|:-:|:-:|:-:|:-:|
| (2,2)=S | base | — | 0 | 1 |
| (2,1)=1 | 1 | (2,2)→0+1=1 | 1 | 1 |
| (2,0)=2 | 2 | (2,1)→1+2=3 | 3 | 1 |
| (1,2)=1 | 1 | (2,2)→0+1=1 | 1 | 1 |
| (1,1)=X | — | blocked | −∞ | 0 |
| (1,0)=1 | 1 | (2,0)→3+1=4, (2,1)→1+1=2, (1,1)=X | 4 | 1 |
| (0,2)=2 | 2 | (1,2)→1+2=3 | 3 | 1 |
| (0,1)=1 | 1 | (1,2)→1+1=2, (0,2)→3+1=4 | 4 | 1 |
| (0,0)=E | 0 | (1,0)→4+0=4 ✓, (0,1)→4+0=4 ✓, (1,1)=X | **4** | **2** |

**Answer: [4, 2]** ✓

---

## The Merging Pattern

This two-value DP is a standard template when you need "maximum value + count of maximums":

```python
if candidate_score > best_score:
    best_score = candidate_score
    best_count = candidate_count        # reset: new winner
elif candidate_score == best_score:
    best_count += candidate_count       # tie: accumulate
# else: strictly worse, ignore
```

The modulo only applies to counts, never to scores.

---

## Edge Cases

| Case | Behaviour |
|---|---|
| All obstacles between S and E | dp_score[0][0] stays −∞ → `[0, 0]` |
| Direct diagonal path only | Single path counted once |
| Multiple tied paths | Counts accumulate correctly via `elif` branch |
| `'E'` and `'S'` cells | Contribute val=0; don't affect score, do affect reachability |
| 2×2 board | All three moves possible from (1,1); up/left both reach E via (0,1) and (1,0), diagonal reaches E directly |

---

## Key Insights

| Insight | Explanation |
|---|---|
| **Reverse direction** | Process bottom-right → top-left so predecessors are always ready |
| **Three predecessors only** | Moves are up/left/diagonal → came from below/right/below-right |
| **Two-value DP** | Track (max_score, count) together; update count only when score ties or beats |
| **NEG_INF sentinel** | Cleanly distinguishes unreachable cells from zero-score cells |
| **Mod only on count** | Score is at most 9 × 100 = 900; no overflow risk |

---

## Approach Tags

`Dynamic Programming` · `Matrix DP` · `Count Optimal Paths` · `Two-value State`

---

*Day 59 of the LeetCode Daily Challenge*
