# Day 55 — LeetCode Challenge

## 1967. Number of Strings That Appear as Substrings in Word

| Field | Details |
|---|---|
| **Difficulty** | Easy |
| **Topics** | Array · String |
| **LeetCode Link** | [1967. Number of Strings That Appear as Substrings in Word](https://leetcode.com/problems/number-of-strings-that-appear-as-substrings-in-word/) |

---

## Problem Statement

Given an array of strings `patterns` and a string `word`, return the number of strings in `patterns` that exist as a **substring** in `word`.

---

## Examples

### Example 1
```
Input:  patterns = ["a","abc","bc","d"], word = "abc"
Output: 3
```
`"a"`, `"abc"`, `"bc"` are all substrings of `"abc"`. `"d"` is not.

### Example 2
```
Input:  patterns = ["a","b","c"], word = "aaaaabbbbb"
Output: 2
```
`"a"` and `"b"` appear; `"c"` does not.

### Example 3
```
Input:  patterns = ["a","a","a"], word = "ab"
Output: 3
```
Duplicates in `patterns` count independently — each `"a"` is checked separately.

---

## Constraints

- `1 <= patterns.length <= 100`
- `1 <= patterns[i].length <= 100`
- `1 <= word.length <= 100`
- All strings consist of lowercase English letters.

---

## Intuition

Python's `in` operator checks substring membership directly. For each pattern, `p in word` returns `True` if `p` appears anywhere in `word`. Sum over all patterns.

Worst-case work: `100 patterns × 100 chars each × 100 char word = 10⁶` operations — no optimisation needed.

---

## Solution

```python
from typing import List


class Solution:
    def numOfStrings(self, patterns: List[str], word: str) -> int:
        return sum(p in word for p in patterns)
```

---

## Complexity Analysis

| | Complexity | Reason |
|---|---|---|
| **Time** | **O(n · m · w)** | n patterns, each substring check O(m × w); here all ≤ 100 |
| **Space** | **O(1)** | No extra storage |

---

## Edge Cases

| Case | Behaviour |
|---|---|
| Pattern longer than word | `p in word` returns `False` — correct |
| Duplicate patterns | Each checked independently, counted separately |
| No matches | Returns `0` |
| All match | Returns `len(patterns)` |

---

## Approach Tags

`String` · `Substring Check` · `One-liner`

---

*Day 55 of the LeetCode Daily Challenge*
