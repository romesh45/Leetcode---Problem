# Day 69 -- LeetCode Challenge

## 3312. Sorted GCD Pair Queries

| Field | Details |
|---|---|
| **Difficulty** | Hard |
| **Topics** | Array -- Number Theory -- Binary Search -- Counting |
| **LeetCode Link** | [3312. Sorted GCD Pair Queries](https://leetcode.com/problems/sorted-gcd-pair-queries/) |

---

## Problem Statement

Given `nums` and `queries`, build `gcdPairs` (sorted GCDs of all pairs i<j). For each query, return `gcdPairs[query]`.

---

## Examples

### Example 1
```
Input:  nums = [2,3,4], queries = [0,2,2]
Output: [1,2,2]
```
`gcdPairs = [1,1,2]`. `gcdPairs[0]=1`, `gcdPairs[2]=2`.

### Example 2
```
Input:  nums = [4,4,2,1], queries = [5,3,1,0]
Output: [4,2,1,1]
```
`gcdPairs = [1,1,1,2,2,4]`.

---

## Constraints

- `2 <= n <= 10^5`, `1 <= nums[i] <= 5*10^4`
- `1 <= queries.length <= 10^5`, `0 <= queries[i] < n*(n-1)/2`

---

## Intuition

n can reach 10^5, so there are up to ~5*10^9 pairs -- we cannot enumerate them.

Instead, compute a **prefix count**: `prefix[g]` = number of pairs with GCD <= g. Then each query is answered by `bisect_right(prefix, q)` -- the smallest g where `prefix[g] > q`.

### How to build prefix efficiently

Let:
- `freq[v]` = count of `v` in nums.
- `cnt[d]` = count of elements divisible by `d` (sieve in O(V log V)).
- `C(cnt[d], 2)` = pairs where **both** elements are divisible by d (GCD is *some multiple* of d).

To isolate pairs with GCD **exactly** d, apply an inclusion-exclusion sieve top-down:

```
exact[d] = C(cnt[d],2) - sum_{k>=2, k*d < V} exact[k*d]
```

Processing d from high to low ensures all multiples are already computed. Then `prefix[g] = prefix[g-1] + exact[g]`.

---

## Solution

```python
from typing import List
from bisect import bisect_right


class Solution:
    def gcdValues(self, nums: List[int], queries: List[int]) -> List[int]:
        MAX_VAL = max(nums) + 1

        freq = [0] * MAX_VAL
        for x in nums:
            freq[x] += 1

        cnt = [0] * MAX_VAL
        for d in range(1, MAX_VAL):
            for k in range(d, MAX_VAL, d):
                cnt[d] += freq[k]

        exact = [0] * MAX_VAL
        for d in range(MAX_VAL - 1, 0, -1):
            exact[d] = cnt[d] * (cnt[d] - 1) // 2
            for k in range(2 * d, MAX_VAL, d):
                exact[d] -= exact[k]

        prefix = [0] * MAX_VAL
        for d in range(1, MAX_VAL):
            prefix[d] = prefix[d - 1] + exact[d]

        return [bisect_right(prefix, q) for q in queries]
```

---

## Complexity Analysis

| | Complexity | Reason |
|---|---|---|
| **Time** | **O(V log V + Q log V)** | Two sieves each O(V log V); Q binary searches each O(log V) |
| **Space** | **O(V)** | freq/cnt/exact/prefix arrays, V = max(nums) <= 50000 |

---

## Why the sieve works

`C(cnt[d], 2)` counts all pairs both divisible by d -- these have GCD that is *any* multiple of d (d, 2d, 3d, ...). Subtracting `exact[2d] + exact[3d] + ...` strips out pairs whose GCD is strictly a larger multiple of d, leaving only GCD exactly d. The top-down order guarantees each `exact[k*d]` is fully settled before it is used.

---

## Edge Cases

| Case | Behaviour |
|---|---|
| All elements equal to v | Only one distinct GCD = v; `exact[v] = C(n,2)` |
| All elements = 1 | All pairs have GCD 1; `prefix[1] = C(n,2)` |
| Two elements | One pair, one query: `gcdPairs[0] = gcd(nums[0], nums[1])` |

---

## Approach Tags

`Sieve` -- `Inclusion-Exclusion` -- `Binary Search` -- `Number Theory`

---

*Day 69 of the LeetCode Daily Challenge*
