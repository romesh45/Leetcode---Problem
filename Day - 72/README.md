# Day 67 — LeetCode Challenge

## 3658. GCD of Odd and Even Sums

| Field | Details |
|---|---|
| **Difficulty** | Easy |
| **Topics** | Math |
| **LeetCode Link** | [3658. GCD of Odd and Even Sums](https://leetcode.com/problems/gcd-of-odd-and-even-sums/) |

---

## Problem Statement

Given `n`, compute `GCD(sumOdd, sumEven)` where `sumOdd` is the sum of the first `n` positive odd numbers and `sumEven` is the sum of the first `n` positive even numbers.

---

## Examples

### Example 1
```
Input:  n = 4
Output: 4
```
`sumOdd = 1+3+5+7 = 16`, `sumEven = 2+4+6+8 = 20`, `GCD(16,20) = 4`.

### Example 2
```
Input:  n = 5
Output: 5
```
`sumOdd = 1+3+5+7+9 = 25`, `sumEven = 2+4+6+8+10 = 30`, `GCD(25,30) = 5`.

---

## Constraints

- `1 <= n <= 1000`

---

## Derivation

Two closed forms from arithmetic-series summation:

```
sumOdd  = 1 + 3 + 5 + … + (2n-1)  =  n²
sumEven = 2 + 4 + 6 + … + 2n      =  n(n+1)
```

Then:

```
GCD(n², n(n+1))
  = n · GCD(n, n+1)     ← factor out n
  = n · 1               ← consecutive integers are always coprime
  = n
```

The answer is always **n**.

---

## Solution

```python
class Solution:
    def gcdOfSums(self, n: int) -> int:
        return n
```

---

## Complexity Analysis

| | Complexity | Reason |
|---|---|---|
| **Time** | **O(1)** | Direct formula |
| **Space** | **O(1)** | No storage |

---

## Approach Tags

`Math` · `Closed Form` · `GCD`

---

*Day 67 of the LeetCode Daily Challenge*
