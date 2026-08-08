# Day 87 -- LeetCode Challenge

## 3302. Find the Lexicographically Smallest Valid Sequence

| Field | Details |
|---|---|
| **Difficulty** | Medium |
| **Topics** | String -- Two Pointers -- Greedy |
| **LeetCode Link** | [3302. Find the Lexicographically Smallest Valid Sequence](https://leetcode.com/problems/find-the-lexicographically-smallest-valid-sequence/) |

---

## Problem Statement

Given `word1` and `word2`, a sequence of indices `seq` (sorted ascending, size `len(word2)`) is valid if concatenating `word1[seq[i]]` for all `i` produces a string "almost equal" to `word2` (at most one character differs). Return the lexicographically smallest valid `seq`, or `[]` if none exists.

---

## Examples

### Example 1
```
Input:  word1 = "vbcca", word2 = "abc"
Output: [0,1,2]
```
### Example 2
```
Input:  word1 = "bacdc", word2 = "abc"
Output: [1,2,4]
```
### Example 3
```
Input:  word1 = "aaaaaa", word2 = "aaabc"
Output: []
```
### Example 4
```
Input:  word1 = "abc", word2 = "ab"
Output: [0,1]
```

---

## Constraints

- `1 <= word2.length < word1.length <= 3 * 10^5`
- `word1` and `word2` consist only of lowercase English letters.

---

## Approach

1. **Precompute `R[j]`** = the largest starting index `x` such that `word2[j:]` is an
   *exact* subsequence of `word1[x:]`. One backward pass: scan `word1` from the end,
   greedily matching `word2` from its end. `R[m] = n` as the base case. This tells us,
   in O(1), whether "the rest matches exactly from here on" is still possible.

2. **Two-pointer greedy scan** (`ptr` into `word1`, `jj` into `word2`, a `mismatch_used` flag):
   - `word1[ptr] == word2[jj]` -> take it (free, smallest possible index for this slot).
   - else, if the swap hasn't been used and `ptr+1 <= R[jj+1]` (rest still matches
     exactly afterward) -> spend the swap here.
   - else -> `ptr` is useless for this character, advance `ptr` and retry.

   `ptr` strictly increases every iteration, so the scan is linear.

3. If `word2` is fully matched, return the collected indices; if `word1` runs out first,
   return `[]`.

Taking the smallest usable index at each step is safe because array comparison is
lexicographic: getting `seq[jj]` as small as possible always dominates, as long as the
remainder is still provably completable (which `R[]` checks in O(1)).

---

## Solution

```python
from typing import List


class Solution:
    def validSequence(self, word1: str, word2: str) -> List[int]:
        n, m = len(word1), len(word2)

        R = [-1] * (m + 1)
        R[m] = n
        j = m - 1
        for i in range(n - 1, -1, -1):
            if j >= 0 and word1[i] == word2[j]:
                R[j] = i
                j -= 1
            if j < 0:
                break

        result = []
        ptr = 0
        jj = 0
        mismatch_used = False
        while jj < m:
            if ptr >= n:
                return []
            if word1[ptr] == word2[jj]:
                result.append(ptr)
                ptr += 1
                jj += 1
            elif not mismatch_used and ptr + 1 <= R[jj + 1]:
                result.append(ptr)
                ptr += 1
                jj += 1
                mismatch_used = True
            else:
                ptr += 1
        return result
```

---

## Complexity Analysis

| | Complexity | Reason |
|---|---|---|
| **Time** | **O(n + m)** | Backward pass for `R[]`; `ptr` strictly increases in the main scan |
| **Space** | **O(m)** | The `R[]` array plus the output |

---

## Approach Tags

`Two Pointers` -- `Greedy` -- `Subsequence Matching`

---

*Day 87 of the LeetCode Daily Challenge*
