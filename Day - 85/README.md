# Day 79 -- LeetCode Challenge

## 3517. Smallest Palindromic Rearrangement I

| Field | Details |
|---|---|
| **Difficulty** | Medium |
| **Topics** | String -- Sorting -- Counting |
| **LeetCode Link** | [3517. Smallest Palindromic Rearrangement I](https://leetcode.com/problems/smallest-palindromic-rearrangement-i/) |

---

## Problem Statement

Given a palindromic string `s`, return the lexicographically smallest palindromic permutation of `s`.

---

## Examples

### Example 1
```
Input:  s = "z"
Output: "z"
```
### Example 2
```
Input:  s = "babab"
Output: "abbba"
```
'a' twice, 'b' three times. Left half sorted: "ab". Middle: "b". Result: "ab" + "b" + "ba".

### Example 3
```
Input:  s = "daccad"
Output: "acddca"
```
Left half sorted: "acd". No middle. Result: "acd" + "" + "dca".

---

## Constraints

- `1 <= s.length <= 10^5`
- `s` is palindromic (at most one character with odd frequency)

---

## Intuition

A palindrome is uniquely determined by its left half (and optional middle character). To minimise it lexicographically, sort the left half in ascending order.

1. Count character frequencies.
2. For each character (sorted): contribute `count // 2` copies to the left half.
3. The character with an odd count (if any) goes in the middle.
4. Result = left half + middle + reverse(left half).

---

## Solution

```python
from collections import Counter


class Solution:
    def smallestPalindrome(self, s: str) -> str:
        freq = Counter(s)
        half, mid = [], ""
        for ch in sorted(freq):
            half.append(ch * (freq[ch] // 2))
            if freq[ch] % 2 == 1:
                mid = ch
        left = "".join(half)
        return left + mid + left[::-1]
```

---

## Complexity Analysis

| | Complexity | Reason |
|---|---|---|
| **Time** | **O(n)** | Count O(n), sort O(26 log 26) = O(1), build O(n) |
| **Space** | **O(n)** | Output string |

---

## Approach Tags

`Counting` -- `Sorting` -- `Palindrome Construction`

---

*Day 79 of the LeetCode Daily Challenge*
