# Day 99 -- LeetCode Challenge

## 2996. Smallest Missing Integer Greater Than Sequential Prefix Sum

| Field | Details |
|---|---|
| **Difficulty** | Easy |
| **Topics** | Array -- Hash Table |
| **LeetCode Link** | [2996. Smallest Missing Integer Greater Than Sequential Prefix Sum](https://leetcode.com/problems/smallest-missing-integer-greater-than-sequential-prefix-sum/) |

---

## Problem Statement

Find the longest sequential prefix of `nums` (where each element is exactly 1 more than the previous), compute its sum, then return the smallest integer >= that sum which is absent from `nums`.

---

## Examples

### Example 1
```
Input:  nums = [1,2,3,2,5]
Output: 6   (prefix [1,2,3] sums to 6; 6 not in nums)
```
### Example 2
```
Input:  nums = [3,4,5,1,12,14,13]
Output: 15  (prefix [3,4,5] sums to 12; 12,13,14 in nums; 15 is missing)
```

---

## Constraints

- `1 <= nums.length <= 50`
- `1 <= nums[i] <= 50`

---

## Solution

```python
from typing import List


class Solution:
    def missingInteger(self, nums: List[int]) -> int:
        prefix_sum = nums[0]
        for i in range(1, len(nums)):
            if nums[i] == nums[i - 1] + 1:
                prefix_sum += nums[i]
            else:
                break

        s = set(nums)
        x = prefix_sum
        while x in s:
            x += 1
        return x
```

---

## Complexity Analysis

| | Complexity | Reason |
|---|---|---|
| **Time** | **O(n)** | Prefix scan + set lookup loop (bounded by n <= 50) |
| **Space** | **O(n)** | Set of nums |

---

## Approach Tags

`Array` -- `Hash Set` -- `Prefix Scan`

---

*Day 89 of the LeetCode Daily Challenge*
