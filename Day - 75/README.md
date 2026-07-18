# Day 70 -- LeetCode Challenge

## 1979. Find Greatest Common Divisor of Array

| Field | Details |
|---|---|
| **Difficulty** | Easy |
| **Topics** | Array -- Math -- Number Theory |
| **LeetCode Link** | [1979. Find Greatest Common Divisor of Array](https://leetcode.com/problems/find-greatest-common-divisor-of-array/) |

---

## Problem Statement

Return the GCD of the smallest and largest elements in `nums`.

---

## Examples

### Example 1
```
Input:  nums = [2,5,6,9,10]
Output: 2
```
min=2, max=10, gcd(2,10)=2.

### Example 2
```
Input:  nums = [7,5,6,8,3]
Output: 1
```
min=3, max=8, gcd(3,8)=1.

### Example 3
```
Input:  nums = [3,3]
Output: 3
```
min=max=3, gcd(3,3)=3.

---

## Constraints

- `2 <= nums.length <= 1000`
- `1 <= nums[i] <= 1000`

---

## Solution

```python
from math import gcd
from typing import List


class Solution:
    def findGCD(self, nums: List[int]) -> int:
        return gcd(min(nums), max(nums))
```

---

## Complexity Analysis

| | Complexity | Reason |
|---|---|---|
| **Time** | **O(n)** | Single pass for min/max; gcd is O(log(min)) |
| **Space** | **O(1)** | No extra storage |

---

## Approach Tags

`Math` -- `GCD` -- `One-liner`

---

*Day 70 of the LeetCode Daily Challenge*
