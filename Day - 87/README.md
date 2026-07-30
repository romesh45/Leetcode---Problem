# Day 87 -- LeetCode Challenge

## 3014. Minimum Number of Pushes to Type Word I

| Field | Details |
|---|---|
| **Difficulty** | Easy |
| **Topics** | Math -- Greedy |
| **LeetCode Link** | [3014. Minimum Number of Pushes to Type Word I](https://leetcode.com/problems/minimum-number-of-pushes-to-type-word-i/) |

---

## Problem Statement

Remap keys 2-9 on a telephone keypad to minimize the total pushes needed to type `word` (all letters are distinct).

---

## Examples

### Example 1
```
Input:  word = "abcde"
Output: 5    (each letter gets its own key, 1 push each)
```
### Example 2
```
Input:  word = "xycdefghij"
Output: 12   (first 8 letters: 1 push; letters 9-10: 2 pushes)
```

---

## Constraints

- `1 <= word.length <= 26`
- All letters in `word` are distinct

---

## Intuition

With 8 keys available (2-9), the i-th letter (0-indexed) assigned to a key costs `(i // 8) + 1` pushes:

| Slot | Letters assigned | Cost per letter |
|---|---|---|
| 1st on each key | letters 0-7 | 1 push |
| 2nd on each key | letters 8-15 | 2 pushes |
| 3rd on each key | letters 16-23 | 3 pushes |
| 4th on each key | letters 24-25 | 4 pushes |

Since all letters are distinct and their frequencies are all 1, just count the positions.

---

## Solution

```python
class Solution:
    def minimumPushes(self, word: str) -> int:
        return sum(i // 8 + 1 for i in range(len(word)))
```

---

## Complexity Analysis

| | Complexity | Reason |
|---|---|---|
| **Time** | **O(n)** | Single pass over length of word (n <= 26) |
| **Space** | **O(1)** | No extra storage |

Effectively O(1) given the fixed input bound.

---

## Approach Tags

`Greedy` -- `Math` -- `One-liner`

---

*Day 81 of the LeetCode Daily Challenge*
