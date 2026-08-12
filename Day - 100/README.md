# Day 91 -- LeetCode Challenge

## 2958. Length of Longest Subarray With at Most K Frequency

| Field | Details |
|---|---|
| **Difficulty** | Medium |
| **Topics** | Array -- Hash Table -- Sliding Window |
| **LeetCode Link** | [2958. Length of Longest Subarray With at Most K Frequency](https://leetcode.com/problems/length-of-longest-subarray-with-at-most-k-frequency/) |

---

## Problem Statement

Return the length of the longest subarray where every element appears at most `k` times.

---

## Examples

### Example 1
```
Input:  nums = [1,2,3,1,2,3,1,2], k = 2
Output: 6
```
### Example 2
```
Input:  nums = [1,2,1,2,1,2,1,2], k = 1
Output: 2
```
### Example 3
```
Input:  nums = [5,5,5,5,5,5,5], k = 4
Output: 4
```

---

## Constraints

- `1 <= nums.length <= 10^5`
- `1 <= k <= nums.length`

---

## Solution

```python
from typing import List
from collections import defaultdict


class Solution:
    def maxSubarrayLength(self, nums: List[int], k: int) -> int:
        freq = defaultdict(int)
        left = ans = 0
        for right, x in enumerate(nums):
            freq[x] += 1
            while freq[x] > k:
                freq[nums[left]] -= 1
                left += 1
            ans = max(ans, right - left + 1)
        return ans
```

---

## Complexity Analysis

| | Complexity | Reason |
|---|---|---|
| **Time** | **O(n)** | Each element enters and leaves the window at most once |
| **Space** | **O(n)** | Frequency map |

---

## Approach Tags

`Sliding Window` -- `Hash Map` -- `Two Pointers`

---

*Day 91 of the LeetCode Daily Challenge*
