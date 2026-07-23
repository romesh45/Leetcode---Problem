# Day 74 -- LeetCode Challenge

## 3513. Number of Unique XOR Triplets I

| Field | Details |
|---|---|
| **Difficulty** | Medium |
| **Topics** | Array -- Bit Manipulation -- Math |
| **LeetCode Link** | [3513. Number of Unique XOR Triplets I](https://leetcode.com/problems/number-of-unique-xor-triplets-i/) |

---

## Problem Statement

Given a permutation `nums` of `[1, n]`, count distinct values of `nums[i] XOR nums[j] XOR nums[k]` for all `i <= j <= k`.

---

## Examples

### Example 1
```
Input:  nums = [1,2]
Output: 2
```
### Example 2
```
Input:  nums = [3,1,2]
Output: 4
```
Achievable values: `{0, 1, 2, 3}`.

---

## Constraints

- `1 <= n <= 10^5`
- `nums` is a permutation of `[1, n]`

---

## Intuition

Since `nums` is a permutation of `{1,...,n}`, the answer depends only on `n`, not the order.

Three cases for a triplet `(i, j, k)`:

| Pattern | XOR result |
|---|---|
| `i = j = k` | `a XOR a XOR a = a` (single element) |
| `i = j < k` | `a XOR a XOR b = b` (single element) |
| `i < j = k` | `a XOR b XOR b = a` (single element) |
| `i < j < k` | `a XOR b XOR c` (3 distinct elements) |

So achievable values = `{1,...,n}` union `{a XOR b XOR c : a,b,c distinct in {1,...,n}}`.

**For n >= 3:** `{1,...,n}` contains the powers of 2: `1, 2, 4, ..., 2^(k-1)` where `k = n.bit_length()`. These span all `k`-bit values over GF(2). Using triplets, we can reach every value in `{0,...,2^k - 1}` (including 0 via `1 XOR 2 XOR 3 = 0`). Count = `2^k`.

**For n <= 2:** No triple of distinct elements exists, so only single elements are reachable. Count = `n`.

---

## Solution

```python
from typing import List


class Solution:
    def uniqueXorTriplets(self, nums: List[int]) -> int:
        n = len(nums)
        if n <= 2:
            return n
        return 1 << n.bit_length()
```

---

## Complexity Analysis

| | Complexity | Reason |
|---|---|---|
| **Time** | **O(1)** | Direct formula on `n` |
| **Space** | **O(1)** | No storage |

---

## Output Pattern

| n | k = n.bit_length() | Output |
|---|---|---|
| 1 | -- | 1 |
| 2 | -- | 2 |
| 3 | 2 | 4 |
| 4..7 | 3 | 8 |
| 8..15 | 4 | 16 |
| 16..31 | 5 | 32 |

---

## Approach Tags

`Bit Manipulation` -- `GF(2) Span` -- `Closed Form`

---

*Day 74 of the LeetCode Daily Challenge*
