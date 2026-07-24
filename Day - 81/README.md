# Day 75 -- LeetCode Challenge

## 3514. Number of Unique XOR Triplets II

| Field | Details |
|---|---|
| **Difficulty** | Medium |
| **Topics** | Array -- Bit Manipulation -- Hash Table |
| **LeetCode Link** | [3514. Number of Unique XOR Triplets II](https://leetcode.com/problems/number-of-unique-xor-triplets-ii/) |

---

## Problem Statement

Given any integer array `nums`, count distinct values of `nums[i] XOR nums[j] XOR nums[k]` for all `i <= j <= k`.

---

## Examples

### Example 1
```
Input:  nums = [1,3]
Output: 2
```
### Example 2
```
Input:  nums = [6,7,8,9]
Output: 4
```
All triple XORs from `{6,7,8,9}` land back in `{6,7,8,9}` (closed under this operation).

---

## Constraints

- `1 <= nums.length <= 1500`
- `1 <= nums[i] <= 1500`

---

## Intuition

Same triple analysis as Part I:

| Pattern | XOR result |
|---|---|
| `i = j = k` | `a` (single element) |
| `i = j < k` | `b` (single element) |
| `i < j = k` | `a` (single element) |
| `i < j < k` | `a XOR b XOR c` (new values) |

So the achievable set = `{a XOR b XOR c : a, b, c drawn from nums}` over all possible index combinations.

For distinct values `a, b, c` in `A = set(nums)`, each has its own index, so every such triple is formable. Triples with repeated values reduce to single elements already in `A`.

**Key bound:** `nums[i] <= 1500 < 2048 = 2^11`, so any XOR is at most 11 bits -- only 2048 possible values.

**Algorithm:**

```
A = set(nums)
pairs  = {a XOR b : a in A, b in A}   -- at most 2048 values
result = {p XOR c : p in pairs, c in A}  -- at most 2048 values
return len(result)
```

---

## Solution

```python
from typing import List


class Solution:
    def uniqueXorTriplets(self, nums: List[int]) -> int:
        A = set(nums)
        pairs = {a ^ b for a in A for b in A}
        return len({p ^ c for p in pairs for c in A})
```

---

## Complexity Analysis

| | Complexity | Reason |
|---|---|---|
| **Time** | **O(|A|^2 + M * |A|)** | |A|^2 for pairs; M = |pairs| <= 2048; M * |A| for triples |
| **Space** | **O(M)** | pairs and result sets each bounded by 2048 |

For `|A| = 1500`: ~2.25M + ~3M = ~5.3M iterations -- fast in Python.

---

## Why Part I and Part II differ

| | Part I | Part II |
|---|---|---|
| Input | Permutation of `[1,n]` | Any integers in `[1,1500]` |
| Distinct values | Exactly `{1,...,n}` | Arbitrary subset of `[1,1500]` |
| Solution | Closed-form `1 << n.bit_length()` | Set-based 2-pass computation |

Part I had a neat closed form because `{1,...,n}` always spans the full k-bit vector space. Part II can't rely on that -- e.g., `{6,7,8,9}` has only 4 values but is "closed" under 3-XOR (all results stay in the same set).

---

## Approach Tags

`Bit Manipulation` -- `XOR Set` -- `Two-Pass Computation`

---

*Day 75 of the LeetCode Daily Challenge*
