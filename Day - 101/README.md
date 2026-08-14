# Day 101 -- LeetCode Challenge

## 2213. Longest Substring of One Repeating Character

| Field | Details |
|---|---|
| **Difficulty** | Hard |
| **Topics** | String -- Segment Tree |
| **LeetCode Link** | [2213. Longest Substring of One Repeating Character](https://leetcode.com/problems/longest-substring-of-one-repeating-character/) |

---

## Problem Statement

Given a string `s` and `k` queries, each query replaces one character of `s`. After each update, return the length of the longest substring made of a single repeating character.

---

## Examples

### Example 1
```
Input:  s = "babacc", queryCharacters = "bcb", queryIndices = [1,3,3]
Output: [3, 3, 4]
```
### Example 2
```
Input:  s = "abyzz", queryCharacters = "aa", queryIndices = [2,1]
Output: [2, 3]
```

---

## Constraints

- `1 <= s.length, k <= 10^5`

---

## Intuition

Naive O(n) scan after each update gives O(nk) = O(10^10) -- too slow. We need a data structure that supports:
- Point update: change one character.
- Global query: longest uniform run.

A **segment tree** whose nodes store "run metadata" achieves O(log n) per operation.

### Node information

Each segment tree node covering range `[lo, hi]` stores:

| Field | Meaning |
|---|---|
| `lc` | Leftmost character |
| `rc` | Rightmost character |
| `ll` | Length of the uniform run at the left end |
| `rl` | Length of the uniform run at the right end |
| `ml` | Maximum uniform run anywhere in the range |
| `ln` | Total length of the range |

### Merge (pull-up)

When combining left child L and right child R:

```
ll = L.ll + R.ll   if L is entirely one char AND L.lc == R.lc
     L.ll           otherwise

rl = R.rl + L.rl   if R is entirely one char AND R.rc == L.rc
     R.rl           otherwise

cross = L.rl + R.ll  if L.rc == R.lc  (seam extends)
        0             otherwise

ml = max(L.ml, R.ml, cross)
```

---

## Solution

```python
from typing import List


class Solution:
    def longestRepeating(self, s: str, queryCharacters: str, queryIndices: List[int]) -> List[int]:
        n = len(s)
        s = list(s)
        lc = [''] * (4 * n);  rc = [''] * (4 * n)
        ll = [0]  * (4 * n);  rl = [0]  * (4 * n)
        ml = [0]  * (4 * n);  ln = [0]  * (4 * n)

        def pull(v):
            L, R = v << 1, v << 1 | 1
            lc[v] = lc[L];  rc[v] = rc[R];  ln[v] = ln[L] + ln[R]
            ll[v] = ll[L] + ll[R] if ll[L] == ln[L] and lc[L] == lc[R] else ll[L]
            rl[v] = rl[R] + rl[L] if rl[R] == ln[R] and rc[R] == rc[L] else rl[R]
            cross = rl[L] + ll[R] if rc[L] == lc[R] else 0
            ml[v] = max(ml[L], ml[R], cross)

        def build(v, lo, hi):
            if lo == hi:
                lc[v] = rc[v] = s[lo]
                ll[v] = rl[v] = ml[v] = ln[v] = 1
                return
            mid = (lo + hi) >> 1
            build(v << 1, lo, mid);  build(v << 1 | 1, mid + 1, hi)
            pull(v)

        def update(v, lo, hi, idx, ch):
            if lo == hi:
                lc[v] = rc[v] = ch
                return
            mid = (lo + hi) >> 1
            if idx <= mid:
                update(v << 1, lo, mid, idx, ch)
            else:
                update(v << 1 | 1, mid + 1, hi, idx, ch)
            pull(v)

        build(1, 0, n - 1)
        ans = []
        for ch, idx in zip(queryCharacters, queryIndices):
            s[idx] = ch
            update(1, 0, n - 1, idx, ch)
            ans.append(ml[1])
        return ans
```

---

## Complexity Analysis

| | Complexity | Reason |
|---|---|---|
| **Time** | **O((n + k) log n)** | Build O(n); each update + query O(log n) |
| **Space** | **O(n)** | Six arrays of size 4n |

---

## Key Merge Insight

The maximum run can span the boundary between two children -- `cross = L.rl + R.ll` when the boundary characters match. This cross-seam value is what makes the problem non-trivial and why a plain max-segment-tree doesn't suffice.

---

## Approach Tags

`Segment Tree` -- `String` -- `Run-Length Encoding`

---

*Day 93 of the LeetCode Daily Challenge*
