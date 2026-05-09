# 13. Roman to Integer

**Difficulty:** Easy  
**Topic Tags:** Hash Table, Math, String  
**LeetCode Link:** [Problem 13](https://leetcode.com/problems/roman-to-integer/)

---

## Problem Statement

Convert a Roman numeral string to an integer.

| Symbol | Value |
|--------|-------|
| I | 1 |
| V | 5 |
| X | 10 |
| L | 50 |
| C | 100 |
| D | 500 |
| M | 1000 |

**Subtraction rule:** Six special cases where a smaller symbol placed **before** a larger one means subtract:
`IV=4`, `IX=9`, `XL=40`, `XC=90`, `CD=400`, `CM=900`

---

## The One Rule That Solves Everything

> **If the current symbol's value is less than the next symbol's value → subtract it.**  
> **Otherwise → add it.**

That's it. No need to memorize the 6 special pairs explicitly.

---

## Visual Walkthrough — `MCMXCIV = 1994`

```
 M     C     M     X     C     I     V
1000  100  1000   10   100    1     5

Scan left → right, compare current vs next:

M(1000) >= C(100)  → ADD    1000  | total = 1000
C(100)  <  M(1000) → SUB    -100  | total =  900   ← CM = 900
M(1000) >= X(10)   → ADD    1000  | total = 1900
X(10)   <  C(100)  → SUB     -10  | total = 1890   ← XC = 90
C(100)  >= I(1)    → ADD     100  | total = 1990
I(1)    <  V(5)    → SUB      -1  | total = 1989   ← IV = 4
V(5)    → last     → ADD       5  | total = 1994 ✓
```

---

## Algorithm

```
1. Build a map: symbol → value
2. Initialize result = 0
3. Scan i from 0 to len-1:
   - If i+1 exists AND value[i] < value[i+1]:
       result -= value[i]      ← subtraction case
   - Else:
       result += value[i]      ← normal addition
4. Return result
```

---

## Solution

```python
class Solution:
    def romanToInt(self, s: str) -> int:
        values = {
            'I': 1,   'V': 5,
            'X': 10,  'L': 50,
            'C': 100, 'D': 500,
            'M': 1000
        }

        result = 0

        for i in range(len(s)):
            curr = values[s[i]]
            # Peek at next character (if it exists)
            next_val = values[s[i + 1]] if i + 1 < len(s) else 0

            if curr < next_val:
                result -= curr   # subtraction case (e.g. IV, XC, CM)
            else:
                result += curr   # normal addition

        return result
```

---

## Dry Run — All Three Examples

**Example 1: `"III"` → 3**
```
I(1) >= I(1) → +1 = 1
I(1) >= I(1) → +1 = 2
I(1) → last  → +1 = 3  ✓
```

**Example 2: `"LVIII"` → 58**
```
L(50) >= V(5) → +50 = 50
V(5)  >= I(1) → + 5 = 55
I(1)  >= I(1) → + 1 = 56
I(1)  >= I(1) → + 1 = 57
I(1)  → last  → + 1 = 58  ✓
```

**Example 3: `"MCMXCIV"` → 1994**
```
M(1000) >= C(100)  → +1000 = 1000
C(100)  <  M(1000) →  -100 =  900
M(1000) >= X(10)   → +1000 = 1900
X(10)   <  C(100)  →   -10 = 1890
C(100)  >= I(1)    →  +100 = 1990
I(1)    <  V(5)    →    -1 = 1989
V(5)    → last     →    +5 = 1994  ✓
```

---

## Complexity Analysis

| | Complexity | Reason |
|---|---|---|
| **Time** | `O(n)` | Single pass through the string |
| **Space** | `O(1)` | Fixed-size map of 7 symbols |

---

## Alternative: Right-to-Left Scan

Another clean approach — scan **right to left** and compare with the previously seen value:

```python
class Solution:
    def romanToInt(self, s: str) -> int:
        values = {'I':1,'V':5,'X':10,'L':50,'C':100,'D':500,'M':1000}
        result = 0
        prev = 0

        for ch in reversed(s):
            curr = values[ch]
            if curr < prev:
                result -= curr   # smaller than what came after → subtract
            else:
                result += curr
            prev = curr

        return result
```

Same logic, no index arithmetic needed.

---

## Key Insights

| Insight | Explanation |
|---|---|
| One rule covers all 6 special cases | `curr < next` → subtract, else add |
| No need to detect pairs explicitly | `IV`, `IX`, `XL`, etc. all handled by the same comparison |
| Right-to-left is slightly cleaner | No need to peek ahead; compare with `prev` instead |
| Works because Roman numerals are valid | Constraints guarantee a well-formed input — no need for error handling |

---

## Related Problems

| Problem | Similarity |
|---|---|
| [12. Integer to Roman](https://leetcode.com/problems/integer-to-roman/) | Exact reverse — same symbol table, opposite direction |
| [273. Integer to English Words](https://leetcode.com/problems/integer-to-english-words/) | Number → string representation |
| [38. Count and Say](https://leetcode.com/problems/count-and-say/) | String scanning and pattern recognition |
