# Day 60 — LeetCode Challenge

## 3756. Concatenate Non-Zero Digits and Multiply by Sum II

| Field | Details |
|---|---|
| **Difficulty** | Medium |
| **Topics** | Array · String · Prefix Sum |
| **LeetCode Link** | [3756. Concatenate Non-Zero Digits and Multiply by Sum II](https://leetcode.com/problems/concatenate-non-zero-digits-and-multiply-by-sum-ii/) |

---

## Problem Statement

Given a digit string `s` of length `m` and queries `[li, ri]`, for each query extract `s[li..ri]`, form integer `x` by concatenating its non-zero digits (or `x = 0` if none), and return `(x × digit_sum(x)) mod (10⁹ + 7)`.

---

## Examples

### Example 1
```
Input:  s = "10203004", queries = [[0,7],[1,3],[4,6]]
Output: [12340, 4, 9]
```

### Example 2
```
Input:  s = "1000", queries = [[0,3],[1,1]]
Output: [1, 0]
```

### Example 3
```
Input:  s = "9876543210", queries = [[0,9]]
Output: [444444137]
```
`987654321 × 45 = 44444444445`, and `44444444445 mod (10⁹+7) = 444444137`.

---

## Constraints

- `1 <= m == s.length <= 10⁵`
- `1 <= queries.length <= 10⁵`
- `s` consists of digits only

---

## Intuition

Part I (3754) was O(d) per query — fine for a single integer up to 10⁹ (≤ 10 digits). Here `s` can be 10⁵ characters and there can be 10⁵ queries, making O(m × q) = 10¹⁰ operations — far too slow.

The fix is prefix arrays that let us answer each query in **O(1)** after an O(m) build phase.

### Three prefix arrays

| Array | `prefix[i]` meaning |
|---|---|
| `nz[i]` | Count of non-zero digits in `s[0..i-1]` |
| `px[i]` | Value of the concatenated non-zero digits of `s[0..i-1]` (mod MOD) |
| `ps[i]` | Digit sum of those non-zero digits (plain int) |

### Extracting `x` for query `[l, r]`

The non-zero digits of `s[0..r]` are those of `s[0..l-1]` followed by those of `s[l..r]`. In terms of integer value:

```
px[r+1]  =  px[l] × 10^cnt  +  x        (mathematically)
```

where `cnt = nz[r+1] - nz[l]` is the count of non-zero digits in `s[l..r]`. Rearranging:

```
x  =  px[r+1] − px[l] × 10^cnt   (mod MOD)
```

The digit sum is just `ps[r+1] - ps[l]` — no modular arithmetic needed (max value is `9 × 10⁵`).

Precomputing `pow10[0..m]` means each query is three table lookups and two multiplications.

---

## Solution

```python
from typing import List


class Solution:
    def concatenateAndMultiply(self, s: str, queries: List[List[int]]) -> List[int]:
        MOD = 10**9 + 7
        m = len(s)

        nz = [0] * (m + 1)
        px = [0] * (m + 1)
        ps = [0] * (m + 1)

        for i, ch in enumerate(s):
            d = int(ch)
            nz[i+1] = nz[i]
            px[i+1] = px[i]
            ps[i+1] = ps[i]
            if d:
                nz[i+1] = nz[i] + 1
                px[i+1] = (px[i] * 10 + d) % MOD
                ps[i+1] = ps[i] + d

        pow10 = [1] * (m + 1)
        for i in range(1, m + 1):
            pow10[i] = pow10[i-1] * 10 % MOD

        result = []
        for l, r in queries:
            cnt = nz[r+1] - nz[l]
            x   = (px[r+1] - px[l] * pow10[cnt]) % MOD
            tot = ps[r+1] - ps[l]
            result.append(x * tot % MOD)

        return result
```

---

## Complexity Analysis

| | Complexity | Reason |
|---|---|---|
| **Time** | **O(m + q)** | O(m) prefix build + O(1) per query |
| **Space** | **O(m)** | Three prefix arrays of length m+1 |

---

## Versus Part I (3754)

| | Part I | Part II |
|---|---|---|
| Input | Single integer `n` | String `s` + query list |
| Constraints | `n ≤ 10⁹` (≤ 10 digits) | `m, q ≤ 10⁵` |
| Approach | Direct string scan | Prefix arrays |
| Per-query cost | O(d) | O(1) |
| Modular arithmetic | Not needed | Required (answers can exceed 10¹⁸) |

---

## Edge Cases

| Case | Behaviour |
|---|---|
| All zeros in range | `cnt = 0`, `x = 0`, result `0` |
| Single non-zero digit | `x = d`, `sum = d`, result `d²` |
| `cnt = 0` with `pow10[0] = 1` | `x = px[r+1] - px[l] × 1 = 0` — correct |
| Subtraction wraps negative mod | Python `%` always returns non-negative — safe |

---

## Approach Tags

`Prefix Sum` · `Modular Arithmetic` · `String`

---

*Day 60 of the LeetCode Daily Challenge*
