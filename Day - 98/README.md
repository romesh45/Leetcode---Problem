# Day 90 -- LeetCode Challenge

## 1510. Stone Game IV

| Field | Details |
|---|---|
| **Difficulty** | Hard |
| **Topics** | Math -- Dynamic Programming -- Game Theory |
| **LeetCode Link** | [1510. Stone Game IV](https://leetcode.com/problems/stone-game-iv/) |

---

## Problem Statement

Alice and Bob alternate removing any non-zero perfect square number of stones. The player who cannot move loses. Return `true` if Alice wins (both play optimally).

---

## Examples

### Example 1
```
Input:  n = 1
Output: true   (Alice takes 1, Bob has nothing)
```
### Example 2
```
Input:  n = 2
Output: false  (Alice must take 1; Bob takes 1; Alice has nothing)
```
### Example 3
```
Input:  n = 4
Output: true   (Alice takes 4 immediately)
```

---

## Constraints

- `1 <= n <= 10^5`

---

## Intuition

Standard game-theory DP with Sprague-Grundy logic:

- `dp[0] = False` (current player has no move, loses).
- `dp[i] = True` if there exists at least one perfect square `s^2 <= i` such that `dp[i - s^2] = False` (opponent faces a losing position).
- `dp[i] = False` if all such moves leave the opponent in a winning state.

---

## Solution

```python
class Solution:
    def winnerSquareGame(self, n: int) -> bool:
        dp = [False] * (n + 1)
        for i in range(1, n + 1):
            s = 1
            while s * s <= i:
                if not dp[i - s * s]:
                    dp[i] = True
                    break
                s += 1
        return dp[n]
```

---

## Complexity Analysis

| | Complexity | Reason |
|---|---|---|
| **Time** | **O(n * sqrt(n))** | For each i, try all perfect squares up to i |
| **Space** | **O(n)** | dp array |

---

## Approach Tags

`Game Theory` -- `DP` -- `Sprague-Grundy`

---

*Day 90 of the LeetCode Daily Challenge*
