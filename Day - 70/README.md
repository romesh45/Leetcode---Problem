# Day 65 — LeetCode Challenge

## 1291. Sequential Digits

| Field | Details |
|---|---|
| **Difficulty** | Medium |
| **Topics** | Enumeration |
| **LeetCode Link** | [1291. Sequential Digits](https://leetcode.com/problems/sequential-digits/) |

---

## Problem Statement

Return a sorted list of all integers in `[low, high]` whose digits are strictly sequential (each digit is exactly one more than the previous).

---

## Examples

### Example 1
```
Input:  low = 100, high = 300
Output: [123, 234]
```

### Example 2
```
Input:  low = 1000, high = 13000
Output: [1234, 2345, 3456, 4567, 5678, 6789, 12345]
```

---

## Constraints

- `10 <= low <= high <= 10⁹`

---

## Intuition

Every sequential-digit number is a **contiguous substring of `"123456789"`**. There are at most 2+3+…+9 = 44 such numbers in total, so exhaustive enumeration is instant.

Iterating length-first (2 → 9), then start-position left-to-right, produces candidates in ascending order — no explicit sort needed.

---

## Solution

```python
from typing import List


class Solution:
    def sequentialDigits(self, low: int, high: int) -> List[int]:
        source = "123456789"
        result = []
        for length in range(2, 10):
            for start in range(9 - length + 1):
                num = int(source[start : start + length])
                if low <= num <= high:
                    result.append(num)
        return result
```

---

## Complexity Analysis

| | Complexity | Reason |
|---|---|---|
| **Time** | **O(1)** | At most 44 candidates regardless of input |
| **Space** | **O(1)** | Output aside, no auxiliary storage |

---

## All Sequential-Digit Numbers

| Digits | Numbers |
|---|---|
| 2 | 12, 23, 34, 45, 56, 67, 78, 89 |
| 3 | 123, 234, 345, 456, 567, 678, 789 |
| 4 | 1234, 2345, 3456, 4567, 5678, 6789 |
| 5 | 12345, 23456, 34567, 45678, 56789 |
| 6 | 123456, 234567, 345678, 456789 |
| 7 | 1234567, 2345678, 3456789 |
| 8 | 12345678, 23456789 |
| 9 | 123456789 |

---

## Edge Cases

| Case | Behaviour |
|---|---|
| Range covers no sequential number | Returns `[]` |
| Only 2-digit range | Returns subset of row 2 above |
| `high = 10⁹` | `123456789` (the only 9-digit one) included if `low <= 123456789` |

---

## Approach Tags

`Enumeration` · `String Sliding Window` · `Fixed Universe`

---

*Day 65 of the LeetCode Daily Challenge*
