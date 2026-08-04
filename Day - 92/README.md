# Day 92 -- LeetCode Challenge

## 3731. Find Missing Elements

| Field | Details |
|---|---|
| **Difficulty** | Easy |
| **Topics** | Array -- Hash Table |
| **LeetCode Link** | [3731. Find Missing Elements](https://leetcode.com/problems/find-missing-elements/) |

---

## Problem Statement

Given an array of unique integers that originally covered a contiguous range (with the minimum and maximum still present), return the sorted list of missing integers in that range.

---

## Examples

### Example 1
```
Input:  nums = [1,4,2,5]
Output: [3]
```
### Example 2
```
Input:  nums = [7,8,6,9]
Output: []
```
### Example 3
```
Input:  nums = [5,1]
Output: [2,3,4]
```

---

## Constraints

- `2 <= nums.length <= 100`
- `1 <= nums[i] <= 100`

---

## Solution

```python
from typing import List


class Solution:
    def findMissingElements(self, nums: List[int]) -> List[int]:
        s = set(nums)
        return [x for x in range(min(nums), max(nums) + 1) if x not in s]
```

---

## Complexity Analysis

| | Complexity | Reason |
|---|---|---|
| **Time** | **O(n)** | min/max O(n); range scan O(max-min); set lookup O(1) |
| **Space** | **O(n)** | Set of nums |

---

## Approach Tags

`Hash Set` -- `Range Scan` -- `One-liner`

---

*Day 86 of the LeetCode Daily Challenge*
