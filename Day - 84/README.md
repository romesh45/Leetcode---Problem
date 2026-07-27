# Day 78 -- LeetCode Challenge

## 1464. Maximum Product of Two Elements in an Array

| Field | Details |
|---|---|
| **Difficulty** | Easy |
| **Topics** | Array -- Sorting |
| **LeetCode Link** | [1464. Maximum Product of Two Elements in an Array](https://leetcode.com/problems/maximum-product-of-two-elements-in-an-array/) |

---

## Problem Statement

Return the maximum value of `(nums[i]-1) * (nums[j]-1)` for any two distinct indices `i` and `j`.

---

## Examples

### Example 1
```
Input:  nums = [3,4,5,2]
Output: 12    ((5-1)*(4-1) = 4*3)
```
### Example 2
```
Input:  nums = [1,5,4,5]
Output: 16    ((5-1)*(5-1) = 4*4)
```
### Example 3
```
Input:  nums = [3,7]
Output: 12    ((7-1)*(3-1) = 6*2)
```

---

## Constraints

- `2 <= nums.length <= 500`
- `1 <= nums[i] <= 10^3`

---

## Solution

```python
from typing import List


class Solution:
    def maxProduct(self, nums: List[int]) -> int:
        nums.sort()
        return (nums[-1] - 1) * (nums[-2] - 1)
```

---

## Complexity Analysis

| | Complexity | Reason |
|---|---|---|
| **Time** | **O(n log n)** | Sort |
| **Space** | **O(1)** | In-place |

---

## Approach Tags

`Sorting` -- `Greedy` -- `One-liner`

---

*Day 78 of the LeetCode Daily Challenge*
