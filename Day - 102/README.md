# Day 92 -- LeetCode Challenge

## 3090. Maximum Length Substring With Two Occurrences

| Field | Details |
|---|---|
| **Difficulty** | Easy |
| **Topics** | String -- Hash Table -- Sliding Window |
| **LeetCode Link** | [3090. Maximum Length Substring With Two Occurrences](https://leetcode.com/problems/maximum-length-substring-with-two-occurrences/) |

---

## Problem Statement

Return the maximum length of a substring where each character appears at most twice.

---

## Examples

### Example 1
```
Input:  s = "bcbbbcba"
Output: 4
```
### Example 2
```
Input:  s = "aaaa"
Output: 2
```

---

## Constraints

- `2 <= s.length <= 100`
- `s` consists of lowercase English letters

---

## Solution

```python
from collections import defaultdict


class Solution:
    def maximumLengthSubstring(self, s: str) -> int:
        freq = defaultdict(int)
        left = ans = 0
        for right, c in enumerate(s):
            freq[c] += 1
            while freq[c] > 2:
                freq[s[left]] -= 1
                left += 1
            ans = max(ans, right - left + 1)
        return ans
```

This is problem 2958 (at-most-k-frequency) with `k = 2` hardcoded.

---

## Complexity Analysis

| | Complexity | Reason |
|---|---|---|
| **Time** | **O(n)** | Each character enters and leaves the window once |
| **Space** | **O(1)** | At most 26 entries in the frequency map |

---

## Approach Tags

`Sliding Window` -- `Hash Map`

---

*Day 92 of the LeetCode Daily Challenge*
