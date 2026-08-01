# Day 83 -- LeetCode Challenge

## 486. Predict the Winner

| Field | Details |
|---|---|
| **Difficulty** | Medium |
| **Topics** | Array -- Dynamic Programming -- Game Theory |
| **LeetCode Link** | [486. Predict the Winner](https://leetcode.com/problems/predict-the-winner/) |

---

## Problem Statement

Two players alternate picking numbers from either end of `nums` (Player 1 goes first). Return `true` if Player 1 can achieve a score >= Player 2 (optimal play from both).

---

## Examples

### Example 1
```
Input:  nums = [1,5,2]
Output: false
```
### Example 2
```
Input:  nums = [1,5,233,7]
Output: true
```
Player 1 takes 1, then 233 regardless of Player 2's choice.

---

## Constraints

- `1 <= nums.length <= 20`
- `0 <= nums[i] <= 10^7`

---

## Intuition

Track the **score difference** (current player minus opponent) rather than absolute scores. From any subarray `nums[i..j]`, the current player picks one end and the opponent then plays optimally on what remains. The opponent's gain from the rest is the negative of the current player's perspective.

Define `dp[i][j]` = best score difference (current player - opponent) achievable from `nums[i..j]` with optimal play.

**Transitions:**

```
dp[i][j] = max(
    nums[i] - dp[i+1][j],   # take left end; opponent gets dp[i+1][j] advantage on rest
    nums[j] - dp[i][j-1]    # take right end; opponent gets dp[i][j-1] advantage on rest
)
```

**Answer:** Player 1 wins if `dp[0][n-1] >= 0` (Player 1's net advantage is non-negative).

---

## Solution

```python
from typing import List


class Solution:
    def predictTheWinner(self, nums: List[int]) -> bool:
        n = len(nums)
        dp = [[0] * n for _ in range(n)]
        for i in range(n):
            dp[i][i] = nums[i]
        for length in range(2, n + 1):
            for i in range(n - length + 1):
                j = i + length - 1
                dp[i][j] = max(nums[i] - dp[i + 1][j],
                               nums[j] - dp[i][j - 1])
        return dp[0][n - 1] >= 0
```

---

## Complexity Analysis

| | Complexity | Reason |
|---|---|---|
| **Time** | **O(n^2)** | All subarrays, each in O(1) |
| **Space** | **O(n^2)** | DP table |

---

## Key Insight

The "score difference" trick avoids tracking two separate scores. When the current player gains `v` and the opponent then gets the best outcome from the rest (`dp[rest]` from their perspective), the net contribution is `v - dp[rest]`. This sign flip happens naturally at every layer of recursion.

---

## Approach Tags

`Interval DP` -- `Minimax` -- `Game Theory`

---

*Day 83 of the LeetCode Daily Challenge*
