# Day 68 — LeetCode Challenge

## 3867. Sum of GCD of Formed Pairs

| Field | Details |
|---|---|
| **Difficulty** | Medium |
| **Topics** | Array · Math · Sorting |
| **LeetCode Link** | [3867. Sum of GCD of Formed Pairs](https://leetcode.com/problems/sum-of-gcd-of-formed-pairs/) |

---

## Problem Statement

Given `nums`, build `prefixGcd` where `prefixGcd[i] = gcd(nums[i], max(nums[0..i]))`. Sort `prefixGcd`, then repeatedly pair the smallest remaining element with the largest remaining element. Return the sum of GCDs of all pairs (middle element ignored if `n` is odd).

---

## Examples

### Example 1
```
Input:  nums = [2,6,4]
Output: 2
```
`prefixGcd = [2,6,2]` → sorted `[2,2,6]` → pair `(2,6)`, `gcd=2`. Middle `2` ignored.

### Example 2
```
Input:  nums = [3,6,2,8]
Output: 5
```
`prefixGcd = [3,6,2,8]` → sorted `[2,3,6,8]` → pairs `(2,8)` and `(3,6)` → `gcd(2,8)+gcd(3,6) = 2+3 = 5`.

---

## Constraints

- `1 <= n <= 10⁵`
- `1 <= nums[i] <= 10⁹`

---

## Intuition

Three independent steps, each straightforward:

1. **Build `prefixGcd`**: Maintain a running maximum. `prefixGcd[i] = gcd(nums[i], running_max)`. O(n).
2. **Sort**: Standard sort on the resulting array. O(n log n).
3. **Pair and sum**: Two-pointer from both ends toward the centre. O(n).

No clever tricks needed — the problem is entirely about faithfully executing the spec.

---

## Solution

```python
from math import gcd
from typing import List


class Solution:
    def sumOfGcdPairs(self, nums: List[int]) -> int:
        prefix_gcd = []
        running_max = 0
        for x in nums:
            running_max = max(running_max, x)
            prefix_gcd.append(gcd(x, running_max))

        prefix_gcd.sort()

        result = 0
        lo, hi = 0, len(prefix_gcd) - 1
        while lo < hi:
            result += gcd(prefix_gcd[lo], prefix_gcd[hi])
            lo += 1
            hi -= 1

        return result
```

---

## Complexity Analysis

| | Complexity | Reason |
|---|---|---|
| **Time** | **O(n log n)** | O(n) to build + O(n log n) sort + O(n) pairing |
| **Space** | **O(n)** | `prefix_gcd` array |

---

## Edge Cases

| Case | Behaviour |
|---|---|
| `n = 1` | No pairs formed → `0` |
| All elements equal | All `prefixGcd[i] = x`; all pairwise GCDs = x |
| Strictly increasing input | `prefixGcd[i] = gcd(nums[i], nums[i]) = nums[i]` |
| New max at every step (strictly increasing) | `prefixGcd` = `nums` itself |

---

## Approach Tags

`Simulation` · `Prefix Maximum` · `Two Pointer` · `GCD`

---

*Day 68 of the LeetCode Daily Challenge*
