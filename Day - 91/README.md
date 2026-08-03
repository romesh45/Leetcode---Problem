# Day 91 -- LeetCode Challenge

## 1406. Stone Game III

| Field | Details |
|---|---|
| **Difficulty** | Hard |
| **Topics** | Array -- Dynamic Programming -- Game Theory |
| **LeetCode Link** | [1406. Stone Game III](https://leetcode.com/problems/stone-game-iii/) |

---

## Problem Statement

Alice and Bob alternate turns (Alice first). Each turn the current player takes 1, 2, or 3 stones from the front of a row. Return `"Alice"`, `"Bob"`, or `"Tie"` based on optimal play.

---

## Examples

### Example 1
```
Input:  stoneValue = [1,2,3,7]
Output: "Bob"
```
Alice's best is to take all three (score 6); Bob takes 7 and wins.

### Example 2
```
Input:  stoneValue = [1,2,3,-9]
Output: "Alice"
```
Alice takes all three (score 6); Bob is stuck with -9.

### Example 3
```
Input:  stoneValue = [1,2,3,6]
Output: "Tie"
```
Alice takes all three (6); Bob takes 6. Or Alice takes 1, Bob takes 2+3, Alice takes 6. All paths tie.

---

## Constraints

- `1 <= stoneValue.length <= 5*10^4`
- `-1000 <= stoneValue[i] <= 1000`

---

## Intuition

Same score-difference trick as Problems 486 and 877. Define:

```
dp[i] = best score difference (current player - opponent) starting at index i
```

From index `i`, the current player picks k stones (k in {1,2,3}):

```
dp[i] = max over k: sum(stoneValue[i..i+k-1]) - dp[i+k]
```

The subtraction `- dp[i+k]` flips the opponent's advantage: whatever the opponent gains from `i+k` onward gets subtracted from our total.

Build the table right-to-left so `dp[i+k]` is always available.

---

## Solution

```python
from typing import List


class Solution:
    def stoneGameIII(self, stoneValue: List[int]) -> str:
        n = len(stoneValue)
        dp = [0] * (n + 1)
        for i in range(n - 1, -1, -1):
            best = float('-inf')
            total = 0
            for k in range(1, 4):
                if i + k > n:
                    break
                total += stoneValue[i + k - 1]
                best = max(best, total - dp[i + k])
            dp[i] = best

        if dp[0] > 0:
            return "Alice"
        if dp[0] < 0:
            return "Bob"
        return "Tie"
```

---

## Complexity Analysis

| | Complexity | Reason |
|---|---|---|
| **Time** | **O(n)** | One pass right-to-left; O(1) work per index (k in {1,2,3}) |
| **Space** | **O(n)** | dp array (reducible to O(1) with a rolling window of 4 values) |

---

## Stone Game Series Comparison

| Problem | Players pick | Constraint | Answer |
|---|---|---|---|
| 486 Predict the Winner | 1 from either end | None | Interval DP O(n^2) |
| 877 Stone Game | 1 from either end | Even piles, odd total | Always Alice (O(1)) |
| 1406 Stone Game III | 1-3 from front | Negatives allowed | Linear DP O(n) |

---

## Approach Tags

`Linear DP` -- `Score Difference` -- `Minimax`

---

*Day 85 of the LeetCode Daily Challenge*
