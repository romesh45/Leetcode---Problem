# Day 88 -- LeetCode Challenge

## 3016. Minimum Number of Pushes to Type Word II

| Field | Details |
|---|---|
| **Difficulty** | Medium |
| **Topics** | String -- Greedy -- Sorting -- Hash Table |
| **LeetCode Link** | [3016. Minimum Number of Pushes to Type Word II](https://leetcode.com/problems/minimum-number-of-pushes-to-type-word-ii/) |

---

## Problem Statement

Remap keys 2-9 on a telephone keypad to minimize the total pushes needed to type `word`. Letters may repeat.

---

## Examples

### Example 1
```
Input:  word = "abcde"
Output: 5
```
### Example 2
```
Input:  word = "xyzxyzxyzxyz"
Output: 12   (x, y, z each appear 4 times; all get 1-push slots)
```
### Example 3
```
Input:  word = "aabbccddeeffgghhiiiiii"
Output: 24
```
8 letters (a-h) fill the 1-push slots; 'i' (6 occurrences, highest) should be on a 1-push slot too. Optimal: put 'i' first (1 push * 6) and push 'h' to the 2-push slot (2 * 2).

---

## Constraints

- `1 <= word.length <= 10^5`
- `word` consists of lowercase English letters

---

## Intuition

The cost of a letter is `freq * pushes_needed`. We have 8 keys, and each key can hold multiple letters at increasing push costs (1st letter = 1 push, 2nd = 2, etc.).

Greedy: assign the highest-frequency letters to the cheapest slots. Sort frequencies descending; the i-th letter (0-indexed) assigned costs `(i // 8) + 1` pushes per occurrence.

This is exactly Part I but weighted by frequency instead of assuming all frequencies are 1.

---

## Solution

```python
from collections import Counter


class Solution:
    def minimumPushes(self, word: str) -> int:
        freq = sorted(Counter(word).values(), reverse=True)
        return sum(count * (i // 8 + 1) for i, count in enumerate(freq))
```

---

## Complexity Analysis

| | Complexity | Reason |
|---|---|---|
| **Time** | **O(n + 26 log 26)** | Count O(n); sort O(26 log 26) = O(1); sum O(26) |
| **Space** | **O(1)** | At most 26 frequencies |

---

## Part I vs Part II

| | Part I | Part II |
|---|---|---|
| Input | All letters distinct | Letters may repeat |
| Approach | Direct formula (no sort needed) | Sort by frequency first |
| Formula | `sum(i//8+1 for i in range(n))` | `sum(freq[i] * (i//8+1) for i in ...)` |

---

## Approach Tags

`Greedy` -- `Frequency Sort` -- `Weighted Assignment`

---

*Day 82 of the LeetCode Daily Challenge*
