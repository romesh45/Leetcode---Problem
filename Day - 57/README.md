# Day 56 — LeetCode Challenge

## 1358. Number of Substrings Containing All Three Characters

| Field | Details |
|---|---|
| **Difficulty** | Medium |
| **Topics** | Hash Table · String · Sliding Window |
| **LeetCode Link** | [1358. Number of Substrings Containing All Three Characters](https://leetcode.com/problems/number-of-substrings-containing-all-three-characters/) |

---

## Problem Statement

Given a string `s` consisting only of characters `a`, `b`, and `c`, return the number of substrings containing **at least one occurrence** of all three characters.

---

## Examples

### Example 1
```
Input:  s = "abcabc"
Output: 10
```
The qualifying substrings are `"abc"`, `"abca"`, `"abcab"`, `"abcabc"`, `"bca"`, `"bcab"`, `"bcabc"`, `"cab"`, `"cabc"`, and `"abc"` (again, a different occurrence).

### Example 2
```
Input:  s = "aaacb"
Output: 3
```
The qualifying substrings are `"aaacb"`, `"aacb"`, and `"acb"`.

### Example 3
```
Input:  s = "abc"
Output: 1
```

---

## Constraints

- `3 <= s.length <= 5 * 10^4`
- `s` only consists of `a`, `b`, or `c` characters.

---

## Intuition

A brute-force check of every substring is `O(n²)` (or `O(n³)` with naive validation), which is too slow for `n` up to `5 × 10⁴`. The key insight is a **fixed-right-endpoint counting trick**:

For each index `i` (treated as the *end* of a substring), keep track of the most recent position each of `a`, `b`, and `c` last appeared — call these `last_a`, `last_b`, `last_c`. Any substring `s[j..i]` is guaranteed to contain all three characters as long as `j <= min(last_a, last_b, last_c)`. That means there are exactly `min(last_a, last_b, last_c) + 1` valid starting points `j` (from index `0` up to that minimum, inclusive) for substrings ending at `i`.

Summing this count over every `i` from `0` to `n - 1` gives the total number of qualifying substrings, in a single linear pass — no nested loops, no explicit window expansion/contraction needed.

---

## Solution

```python
class Solution:
    def numberOfSubstrings(self, s: str) -> int:
        last = {'a': -1, 'b': -1, 'c': -1}
        count = 0

        for i, ch in enumerate(s):
            last[ch] = i
            count += min(last['a'], last['b'], last['c']) + 1

        return count
```

---

## Complexity Analysis

| | Complexity | Reason |
|---|---|---|
| **Time** | **O(n)** | Single pass over `s`, O(1) work per character |
| **Space** | **O(1)** | Only three counters stored, regardless of input size |

---

## Edge Cases

| Case | Behaviour |
|---|---|
| One character never appears (e.g. `"aaa"`) | `min(...)` stays `-1`, contributes `0` for every index |
| Exactly one valid substring (e.g. `"abc"`) | Returns `1` |
| Characters arrive out of order (e.g. `"cba"`) | Still counted correctly — order doesn't matter, only "last seen" position |
| Long repeating pattern | Counts grow roughly quadratically as more valid windows accumulate |

---

## Approach Tags

`Sliding Window` · `Last Seen Index` · `Linear Scan`

---

*Day 56 of the LeetCode Daily Challenge*
