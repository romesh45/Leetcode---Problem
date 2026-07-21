# Day 73 -- LeetCode Challenge

## 3499. Maximize Active Section with Trade I

| Field | Details |
|---|---|
| **Difficulty** | Medium |
| **Topics** | String -- Greedy -- Run-Length Encoding |
| **LeetCode Link** | [3499. Maximize Active Section with Trade I](https://leetcode.com/problems/maximize-active-section-with-trade-i/) |

---

## Problem Statement

Given a binary string `s`, make at most one trade to maximise '1' count. A trade converts a '1' block (surrounded by '0's) to '0's, then converts the resulting merged '0' block (surrounded by '1's) to '1's. String is treated as if augmented with '1' at both ends.

---

## Examples

### Example 1
```
Input:  s = "01"
Output: 1  (no valid trade)
```

### Example 2
```
Input:  s = "0100"
Output: 4  (gain = 1 + 2 = 3)
```

### Example 3
```
Input:  s = "1000100"
Output: 7  (gain = 3 + 2 = 5)
```

### Example 4
```
Input:  s = "01010"
Output: 4  (gain = 1 + 1 = 2)
```

---

## Constraints

- `1 <= n <= 10^5`
- `s[i]` is '0' or '1'

---

## Intuition

The trade picks a '1' block at positions [l, r] in s (surrounded by '0' runs of length a and c):

```
... '0'^a  '1'^b  '0'^c ...
           [convert to 0]
... '0'^(a+b+c) ...
    [convert to 1]
... '1'^(a+b+c) ...
```

Net change in count of '1's: +a + c (gain the two '0' runs, recover the b lost '1's as part of the merged block).

The '1' block we pick must be surrounded by '0' runs in s -- meaning it is NOT the first or last run. (The augmented '1's at the boundary do not serve as '0' borders.)

So: parse s into alternating runs, scan interior '1' runs, maximize left_0 + right_0.

---

## Solution

```python
class Solution:
    def maxActiveSectionsAfterTrade(self, s: str) -> int:
        base = s.count('1')
        n = len(s)

        runs = []
        i = 0
        while i < n:
            j = i
            while j < n and s[j] == s[i]:
                j += 1
            runs.append((s[i], j - i))
            i = j

        max_gain = 0
        for k in range(1, len(runs) - 1):
            if runs[k][0] == '1':
                gain = runs[k - 1][1] + runs[k + 1][1]
                if gain > max_gain:
                    max_gain = gain

        return base + max_gain
```

---

## Complexity Analysis

| | Complexity | Reason |
|---|---|---|
| **Time** | **O(n)** | One pass to count '1's, one pass for runs, one pass over runs |
| **Space** | **O(r)** | r = number of runs (at most n) |

---

## Why the augmented '1's matter

Without augmentation, any '0' block at the very start or end of s would be seen as surrounded by '1's (vacuously). The augmented '1's close this gap: a '1' run at the start of s is bordered on its left by an augmented '1', not a '0', so it cannot be traded. Same for the end.

---

## Edge Cases

| Case | Behaviour |
|---|---|
| All '1's | No '0' borders anywhere; no valid trade; returns n |
| All '0's | No '1' block to trade; returns 0 |
| s = "010" | Only one interior '1' run (k=1), gain = 1+1 = 2, returns 3 |
| s = "01" | '1' is at last run, excluded; no gain; returns 1 |

---

## Approach Tags

`Run-Length Encoding` -- `Greedy` -- `One-Pass`

---

*Day 73 of the LeetCode Daily Challenge*
