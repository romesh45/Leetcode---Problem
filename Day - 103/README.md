# Day 94 -- LeetCode Challenge

## 3702. Longest Subsequence With Non-Zero Bitwise XOR

| Field | Details |
|---|---|
| **Difficulty** | Medium |
| **Topics** | Array -- Bit Manipulation |
| **LeetCode Link** | [3702. Longest Subsequence With Non-Zero Bitwise XOR](https://leetcode.com/problems/longest-subsequence-with-non-zero-bitwise-xor/) |

---

## Problem Statement

Return the length of the longest subsequence of `nums` whose XOR is non-zero. Return 0 if none exists.

---

## Examples

### Example 1
```
Input:  nums = [1,2,3]
Output: 2    (1^2^3 = 0; remove one, e.g. [2,3] gives XOR 1)
```
### Example 2
```
Input:  nums = [2,3,4]
Output: 3    (2^3^4 = 5 != 0; take all)
```

---

## Constraints

- `1 <= nums.length <= 10^5`
- `0 <= nums[i] <= 10^9`

---

## Intuition

Since XOR is commutative and associative, the result depends only on *which* elements are selected, not their order. This reduces the problem to: find the largest **subset** with non-zero XOR.

Three cases:

1. **XOR of all elements != 0**: take everything. Answer = `n`.

2. **XOR of all elements == 0, but some element is non-zero**: removing any non-zero element `x` gives a subset with XOR = `0 ^ x = x != 0`. Answer = `n - 1`.

3. **All elements are 0**: every subset XORs to 0. Answer = `0`.

---

## Solution

```python
from typing import List
from functools import reduce
from operator import xor


class Solution:
    def longestSubsequence(self, nums: List[int]) -> int:
        total = reduce(xor, nums)
        if total != 0:
            return len(nums)
        if any(x != 0 for x in nums):
            return len(nums) - 1
        return 0
```

---

## Complexity Analysis

| | Complexity | Reason |
|---|---|---|
| **Time** | **O(n)** | One pass for total XOR; one pass for any-nonzero check |
| **Space** | **O(1)** | No extra storage |

---

## Approach Tags

`Bit Manipulation` -- `XOR` -- `Greedy`

---

*Day 94 of the LeetCode Daily Challenge*
