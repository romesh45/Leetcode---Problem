# Day 71 -- LeetCode Challenge

## 1081. Smallest Subsequence of Distinct Characters

| Field | Details |
|---|---|
| **Difficulty** | Medium |
| **Topics** | String -- Stack -- Greedy |
| **LeetCode Link** | [1081. Smallest Subsequence of Distinct Characters](https://leetcode.com/problems/smallest-subsequence-of-distinct-characters/) |

---

## Problem Statement

Return the lexicographically smallest subsequence of `s` that contains every distinct character of `s` exactly once.

---

## Examples

### Example 1
```
Input:  s = "bcabc"
Output: "abc"
```

### Example 2
```
Input:  s = "cbacdcbc"
Output: "acdb"
```

---

## Constraints

- `1 <= s.length <= 1000`
- `s` consists of lowercase English letters

---

## Intuition

Build the result character by character using a **greedy monotonic stack**. The goal is to keep the stack in ascending lexicographic order as much as possible, but only remove a character from the top when we are guaranteed to see it again later.

Two rules per character `c`:

1. **Skip** if `c` is already in the stack -- we already have the optimal placement.
2. **Pop** the top character `top` if:
   - `top > c` (replacing top with c makes the prefix smaller), AND
   - `last[top] > i` (top appears again later, so removing it now is safe).

Repeat popping until neither condition holds, then push `c`.

The `last[c]` lookup is precomputed in one pass.

---

## Solution

```python
class Solution:
    def smallestSubsequence(self, s: str) -> str:
        last = {c: i for i, c in enumerate(s)}
        stack = []
        in_stack = set()

        for i, c in enumerate(s):
            if c in in_stack:
                continue
            while stack and stack[-1] > c and last[stack[-1]] > i:
                in_stack.discard(stack.pop())
            stack.append(c)
            in_stack.add(c)

        return ''.join(stack)
```

---

## Complexity Analysis

| | Complexity | Reason |
|---|---|---|
| **Time** | **O(n)** | Each character pushed and popped at most once; dict lookups O(1) |
| **Space** | **O(1)** | Stack and set hold at most 26 characters |

---

## Trace: "cbacdcbc"

| i | c | Action | Stack |
|---|---|---|---|
| 0 | c | push | `[c]` |
| 1 | b | pop c (b<c, last[c]=7>1); push b | `[b]` |
| 2 | a | pop b (a<b, last[b]=6>2); push a | `[a]` |
| 3 | c | a<c, push | `[a,c]` |
| 4 | d | c<d, push | `[a,c,d]` |
| 5 | c | c in stack, skip | `[a,c,d]` |
| 6 | b | d>b but last[d]=4<6 -- can't pop; push b | `[a,c,d,b]` |
| 7 | c | c in stack, skip | `[a,c,d,b]` |

Result: `"acdb"` -- the key insight at i=6: d cannot be removed because its last occurrence (index 4) is behind us.

---

## Edge Cases

| Case | Behaviour |
|---|---|
| All distinct chars, already sorted | Stack never pops; result = s |
| All same char | One-character result |
| Reverse sorted, all distinct | Nothing can be popped (each char appears only once); result = s |

---

## Approach Tags

`Monotonic Stack` -- `Greedy` -- `Last Occurrence`

---

*Day 71 of the LeetCode Daily Challenge*
