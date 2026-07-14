# Day 66 — LeetCode Challenge

## 3336. Find the Number of Subsequences With Equal GCD

| Field | Details |
|---|---|
| **Difficulty** | Hard |
| **Topics** | Array · Dynamic Programming · Math |
| **LeetCode Link** | [3336. Find the Number of Subsequences With Equal GCD](https://leetcode.com/problems/find-the-number-of-subsequences-with-equal-gcd/) |

---

## Problem Statement

Count ordered pairs of **disjoint, non-empty** subsequences `(seq1, seq2)` of `nums` such that `gcd(seq1) == gcd(seq2)`. Return the count modulo `10⁹ + 7`.

---

## Examples

### Example 1
```
Input:  nums = [1,2,3,4]
Output: 10
```
All 10 valid pairs have GCD equal to 1.

### Example 2
```
Input:  nums = [10,20,30]
Output: 2
```
Two pairs, both with GCD 10.

### Example 3
```
Input:  nums = [1,1,1,1]
Output: 50
```
Total assignments = 3⁴ = 81. Subtract those where seq1 or seq2 is empty: 81 − 2·16 + 1 = 50.

---

## Constraints

- `1 <= nums.length <= 200`
- `1 <= nums[i] <= 200`

---

## Intuition

Every element has exactly three fates: go to **seq1**, go to **seq2**, or be **skipped**. We track the running GCDs of both groups as we process elements left to right.

### DP state

```
dp[(g1, g2)] = number of assignments of elements seen so far
               where seq1's running GCD is g1 and seq2's is g2
```

`g = 0` means the corresponding subsequence is still empty (using `gcd(0, x) = x` by convention so the first element added sets the GCD directly).

### Transition per element `x`

From state `(g1, g2)` with count `cnt`, generate three new states:

| Choice | New state |
|---|---|
| Skip `x` | `(g1, g2)` |
| Assign to seq1 | `(gcd(g1, x), g2)` |
| Assign to seq2 | `(g1, gcd(g2, x))` |

### Why this stays tractable

Any GCD value must divide some `nums[i] ≤ 200`, so there are at most 200 distinct g1 values and 200 distinct g2 values → at most 201² ≈ 40 000 active states. The defaultdict stores only non-zero entries, keeping the working set small.

### Answer

After processing all elements, sum `dp[(g, g)]` for all `g ≥ 1` (both subsequences non-empty, equal GCDs).

---

## Solution

```python
from math import gcd
from typing import List
from collections import defaultdict


class Solution:
    def subsequencePairCount(self, nums: List[int]) -> int:
        MOD = 10**9 + 7

        dp = defaultdict(int)
        dp[(0, 0)] = 1

        for x in nums:
            new_dp = defaultdict(int)
            for (g1, g2), cnt in dp.items():
                new_dp[g1, g2]          = (new_dp[g1, g2]          + cnt) % MOD
                new_dp[gcd(g1, x), g2]  = (new_dp[gcd(g1, x), g2]  + cnt) % MOD
                new_dp[g1, gcd(g2, x)]  = (new_dp[g1, gcd(g2, x)]  + cnt) % MOD
            dp = new_dp

        return sum(cnt for (g1, g2), cnt in dp.items() if g1 == g2 > 0) % MOD
```

---

## Complexity Analysis

| | Complexity | Reason |
|---|---|---|
| **Time** | **O(n · V²)** | n elements × up to V² ≈ 40 000 active states; each GCD call O(log V) |
| **Space** | **O(V²)** | At most 201² DP states (V = max(nums) = 200) |

For `n = V = 200`, this is roughly **200 × 40 000 = 8 × 10⁶** GCD operations — well within limits.

---

## Edge Cases

| Case | Behaviour |
|---|---|
| Single element | Can't form two disjoint non-empty seqs → `0` |
| All elements equal | All non-empty subsets share the same GCD; reduces to counting disjoint non-empty subset pairs |
| `[1,1,1,1]` | 3⁴ − 2·2⁴ + 1 = 50 (inclusion-exclusion on empty seqs) |

---

## Key Convention

`gcd(0, x) = x` — Python's `math.gcd` respects this. It allows `g = 0` to cleanly encode "empty subsequence": the first element added to seq1 or seq2 sets its GCD directly without special-casing.

---

## Approach Tags

`DP on GCD Pairs` · `Three-Way Element Assignment` · `Number Theory`

---

*Day 66 of the LeetCode Daily Challenge*
