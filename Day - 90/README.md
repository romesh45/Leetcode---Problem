# Day 84 -- LeetCode Challenge

## 877. Stone Game

| Field | Details |
|---|---|
| **Difficulty** | Medium |
| **Topics** | Array -- Math -- Game Theory |
| **LeetCode Link** | [877. Stone Game](https://leetcode.com/problems/stone-game/) |

---

## Problem Statement

Alice and Bob alternate picking piles from either end (Alice first). There are an even number of piles and the total is odd. Return `true` if Alice wins.

---

## Examples

### Example 1
```
Input:  piles = [5,3,4,5]
Output: true
```
### Example 2
```
Input:  piles = [3,7,2,3]
Output: true
```

---

## Constraints

- `piles.length` is even
- `sum(piles)` is odd (no ties possible)

---

## Intuition

Alice **always wins** under these constraints -- `return True` is the correct solution.

**Why?** With an even number of piles, every position belongs to exactly one of two parity classes:

```
Even-indexed: piles[0], piles[2], piles[4], ...
Odd-indexed:  piles[1], piles[3], piles[5], ...
```

Since the total is odd, one class has a strictly larger sum. Before the game starts, Alice identifies the winning class and plays accordingly:

- If even-indexed piles sum more, Alice takes `piles[0]` on her first move.
- Whatever Bob does (he must take from one end), the two new ends are both odd-indexed. Alice takes another even-indexed pile. This repeats forever.

Alice ends up with every pile of her chosen parity, which is the larger half. She wins regardless of Bob's play.

---

## Solution

```python
from typing import List


class Solution:
    def stoneGame(self, piles: List[int]) -> bool:
        return True
```

---

## Complexity Analysis

| | Complexity | Reason |
|---|---|---|
| **Time** | **O(1)** | Closed-form result |
| **Space** | **O(1)** | |

---

## Contrast with Problem 486 (Predict the Winner)

Problem 486 is the general version: any number of piles, ties possible. That requires O(n^2) interval DP. Problem 877 adds two constraints (even piles, odd total) that guarantee Alice wins -- making the DP unnecessary.

The interval DP recurrence from 486 still works here and also returns `True` for all valid inputs, but it's overkill.

---

## Approach Tags

`Math` -- `Game Theory` -- `Parity Argument`

---

*Day 84 of the LeetCode Daily Challenge*
