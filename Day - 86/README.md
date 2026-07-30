# Day 80 -- LeetCode Challenge

## 3518. Smallest Palindromic Rearrangement II

| Field | Details |
|---|---|
| **Difficulty** | Hard |
| **Topics** | String -- Combinatorics -- Greedy |
| **LeetCode Link** | [3518. Smallest Palindromic Rearrangement II](https://leetcode.com/problems/smallest-palindromic-rearrangement-ii/) |

---

## Problem Statement

Given a palindromic string `s` and an integer `k`, return the k-th lexicographically smallest palindromic permutation of `s`. Return `""` if fewer than `k` exist.

---

## Examples

### Example 1
```
Input:  s = "abba", k = 2
Output: "baab"
```
Two palindromic rearrangements: `"abba"` (rank 1) and `"baab"` (rank 2).

### Example 2
```
Input:  s = "aa", k = 2
Output: ""
```
Only one arrangement: `"aa"`.

### Example 3
```
Input:  s = "bacab", k = 1
Output: "abcba"
```

---

## Constraints

- `1 <= s.length <= 10^4`
- `s` is palindromic (at most one character with odd frequency)
- `1 <= k <= 10^6`

---

## Intuition

A palindrome is uniquely determined by its **left half** and optional middle character. So counting and ranking palindromic permutations is the same as counting and ranking permutations of the left half (a multiset).

The number of distinct arrangements of a multiset `{c1: a1, c2: a2, ...}` of total size `m` is the multinomial coefficient:

```
m! / (a1! * a2! * ... * am!)  =  C(m, a1) * C(m-a1, a2) * ...
```

We first check if the total count >= k; if not, return `""`.

Then we build the left half greedily, one character at a time. At each position we maintain a running `start` counter (total permutations already counted and skipped). For each candidate character (tried in alphabetical order):

1. Tentatively place it (decrement its count in `freq`).
2. Compute `p` = number of arrangements of the remaining characters.
3. If `start + p >= k`, the k-th permutation is within this group -- place the character and move on.
4. Otherwise, restore the character, add `p` to `start`, and try the next character.

---

## Solution

```python
from math import comb


class Solution:
    def smallestPalindrome(self, s: str, k: int) -> str:
        n = len(s)
        half = n // 2
        freq = [0] * 26
        for i in range(half):
            freq[ord(s[i]) - ord('a')] += 1

        def perm(rem):
            acc = 1
            for ci in range(26):
                f = freq[ci]
                if not f:
                    continue
                if f > rem:
                    return 0
                acc *= comb(rem, f)
                if acc > k:
                    return acc
                rem -= f
            return acc

        left = []
        start = 0

        for i in range(half):
            selected = False
            for ci in range(26):
                if not freq[ci]:
                    continue
                freq[ci] -= 1

                p = perm(half - i - 1)

                if start + p >= k:
                    left.append(chr(ci + ord('a')))
                    selected = True
                    break

                freq[ci] += 1
                start += p

            if not selected:
                return ""

        h1 = "".join(left)
        mid = s[n // 2] if n % 2 == 1 else ''
        h2 = "".join(left[::-1])
        return h1 + mid + h2
```

---

## Complexity Analysis

| | Complexity | Reason |
|---|---|---|
| **Time** | **O(half * 26 * 26)** | half positions; 26 candidates each; perm() iterates over 26 chars and exits early once acc > k |
| **Space** | **O(half)** | left array + O(26) freq |

The `if acc > k: return acc` early exit in `perm()` is the key efficiency trick: once the count exceeds `k`, we stop computing. In practice this terminates in O(1) iterations for large character counts.

---

## How `start + p >= k` Works

`start` is the cumulative count of all permutations ranked below the current candidate group. `p` is the size of the current group (permutations starting with this character at this position). The k-th permutation falls inside this group when `start + p >= k`. This is equivalent to decrementing k by p each time we skip a group -- same logic, different bookkeeping.

---

## Edge Cases

| Case | Behaviour |
|---|---|
| Only one distinct palindrome | `perm(half)` = 1; k=1 succeeds, k>1 returns `""` |
| Single character string | half=0, loop skips, mid=s[0], returns s[0] |
| k equals total count exactly | Last permutation is returned correctly |

---

## Approach Tags

`Greedy` -- `Multinomial Coefficient` -- `Combinatorics` -- `Palindrome`

---

*Day 80 of the LeetCode Daily Challenge*
