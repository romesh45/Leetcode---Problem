# Day 82 -- LeetCode Challenge

## 3536. Maximum Product of Two Digits

| Field | Details |
|---|---|
| **Difficulty** | Easy |
| **Topics** | Math -- Sorting |
| **LeetCode Link** | [3536. Maximum Product of Two Digits](https://leetcode.com/problems/maximum-product-of-two-digits/) |

---

## Problem Statement

Return the maximum product of any two digits of `n` (the same digit may be used twice if it appears more than once).

---

## Examples

### Example 1
```
Input:  n = 31
Output: 3    (3 * 1)
```
### Example 2
```
Input:  n = 22
Output: 4    (2 * 2)
```
### Example 3
```
Input:  n = 124
Output: 8    (2 * 4)
```

---

## Constraints

- `10 <= n <= 10^9`

---

## Solution

```python
class Solution:
    def maxProduct(self, n: int) -> int:
        digits = sorted(int(d) for d in str(n))
        return digits[-1] * digits[-2]
```

---

## Complexity Analysis

| | Complexity | Reason |
|---|---|---|
| **Time** | **O(d log d)** | d = number of digits (at most 10); sort is trivial |
| **Space** | **O(d)** | Digit list |

Effectively O(1) given the input bound.

---

## Approach Tags

`Sorting` -- `Math` -- `One-liner`

---

*Day 76 of the LeetCode Daily Challenge*
