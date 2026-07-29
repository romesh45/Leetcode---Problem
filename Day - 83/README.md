# Day 83 -- LeetCode Challenge

## 628. Maximum Product of Three Numbers

| Field | Details |
|---|---|
| **Difficulty** | Easy |
| **Topics** | Array -- Math -- Sorting |
| **LeetCode Link** | [628. Maximum Product of Three Numbers](https://leetcode.com/problems/maximum-product-of-three-numbers/) |

---

## Problem Statement

Return the maximum product of any three numbers in `nums`.

---

## Examples

### Example 1
```
Input:  nums = [1,2,3]
Output: 6
```
### Example 2
```
Input:  nums = [1,2,3,4]
Output: 24
```
### Example 3
```
Input:  nums = [-1,-2,-3]
Output: -6
```

---

## Constraints

- `3 <= nums.length <= 10^4`
- `-1000 <= nums[i] <= 1000`

---

## Intuition

After sorting, only two candidates can be the answer:

**A.** Three largest: `nums[-3] * nums[-2] * nums[-1]`

**B.** Two smallest (most negative) times the largest: `nums[0] * nums[1] * nums[-1]`

Candidate B matters when the two smallest numbers are both negative -- their product is a large positive, which can beat three positives.

No other combination (e.g. one small and two large) can beat these two.

---

## Solution

```python
from typing import List


class Solution:
    def maximumProduct(self, nums: List[int]) -> int:
        nums.sort()
        return max(nums[-1] * nums[-2] * nums[-3],
                   nums[0]  * nums[1]  * nums[-1])
```

---

## Complexity Analysis

| | Complexity | Reason |
|---|---|---|
| **Time** | **O(n log n)** | Dominated by sort |
| **Space** | **O(1)** | In-place sort |

---

## Edge Cases

| Case | Behaviour |
|---|---|
| All negative | Candidate A wins (least negative triple) |
| Two large negatives | Candidate B wins (`neg * neg * max_pos`) |
| All same value | Both candidates equal; either wins |

---

## Approach Tags

`Sorting` -- `Two Candidates` -- `Greedy`

---

*Day 77 of the LeetCode Daily Challenge*
