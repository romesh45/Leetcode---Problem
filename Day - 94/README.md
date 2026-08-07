# Day 94 -- LeetCode Challenge

## 3345. Smallest Divisible Digit Product I

| Field | Details |
|---|---|
| **Difficulty** | Easy |
| **Topics** | Math -- Brute Force |
| **LeetCode Link** | [3345. Smallest Divisible Digit Product I](https://leetcode.com/problems/smallest-divisible-digit-product-i/) |

---

## Problem Statement

Return the smallest integer >= `n` whose digit product is divisible by `t`.

---

## Examples

### Example 1
```
Input:  n=10, t=2
Output: 10   (digit product = 0, divisible by 2)
```
### Example 2
```
Input:  n=15, t=3
Output: 16   (digit product = 6, divisible by 3)
```

---

## Constraints

- `1 <= n <= 100`, `1 <= t <= 10`

---

## Solution

```python
from math import prod


class Solution:
    def smallestNumber(self, n: int, t: int) -> int:
        while prod(int(d) for d in str(n)) % t != 0:
            n += 1
        return n
```

The loop always terminates quickly: any number containing a `0` digit has product `0`, which is divisible by every `t`. The next multiple of 10 is at most 9 steps away from any starting point.

---

## Complexity Analysis

| | Complexity | Reason |
|---|---|---|
| **Time** | **O(1)** | At most ~10 iterations given n<=100, t<=10 |
| **Space** | **O(1)** | |

---

## Approach Tags

`Brute Force` -- `Math` -- `One-liner`

---

*Day 88 of the LeetCode Daily Challenge*
