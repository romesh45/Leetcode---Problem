# Day 59 — LeetCode Challenge

## 3754. Concatenate Non-Zero Digits and Multiply by Sum I

| Field | Details |
|---|---|
| **Difficulty** | Easy |
| **Topics** | Math · String |
| **LeetCode Link** | [3754. Concatenate Non-Zero Digits and Multiply by Sum I](https://leetcode.com/problems/concatenate-non-zero-digits-and-multiply-by-sum-i/) |

---

## Problem Statement

Given an integer `n`, form a new integer `x` by concatenating all its non-zero digits in their original order (if none exist, `x = 0`). Let `sum` be the digit sum of `x`. Return `x * sum`.

---

## Examples

### Example 1
```
Input:  n = 10203004
Output: 12340
```
Non-zero digits → `x = 1234`, `sum = 1+2+3+4 = 10`, result = `1234 × 10 = 12340`.

### Example 2
```
Input:  n = 1000
Output: 1
```
Non-zero digit → `x = 1`, `sum = 1`, result = `1 × 1 = 1`.

---

## Constraints

- `0 <= n <= 10⁹`

---

## Intuition

Convert `n` to a string, filter out `'0'` characters, then rebuild `x` and compute the digit sum from the same filtered list. The digit sum of `x` is just the sum of those same filtered digits — no need to decompose `x` again.

---

## Solution

```python
class Solution:
    def concatenateAndMultiply(self, n: int) -> int:
        digits = [d for d in str(n) if d != '0']

        if not digits:
            return 0

        x     = int(''.join(digits))
        total = sum(int(d) for d in digits)
        return x * total
```

---

## Complexity Analysis

| | Complexity | Reason |
|---|---|---|
| **Time** | **O(d)** | d = number of digits in n (≤ 10 for n ≤ 10⁹) |
| **Space** | **O(d)** | Filtered digit list |

Effectively O(1) given the fixed input range.

---

## Edge Cases

| Case | Behaviour |
|---|---|
| `n = 0` | No non-zero digits → `x = 0`, return `0` |
| All digits zero (e.g. `1000`) | Only the leading `1` survives → `x = 1`, `sum = 1` |
| Single non-zero digit (e.g. `9`) | `x = 9`, `sum = 9`, result = `81` |
| No zeros (e.g. `123456789`) | All digits kept, `sum = 45`, result = `5555555505` |

---

## Approach Tags

`String` · `Math` · `Simulation`

---

*Day 59 of the LeetCode Daily Challenge*
