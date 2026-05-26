# Day 22 — LeetCode Challenge

## 3120. Count the Number of Special Characters I

| Field | Details |
|---|---|
| **Difficulty** | Easy |
| **Topics** | Hash Set · Counting · String |
| **LeetCode Link** | [3120. Count the Number of Special Characters I](https://leetcode.com/problems/count-the-number-of-special-characters-i/) |

---

## Problem Statement

You are given a string `word`. A letter is called **special** if it appears in **both** lowercase and uppercase in `word`.

Return the number of special letters.

---

## Examples

### Example 1

```
Input:  word = "aaAbcBC"
Output: 3
```

Special letters: `'a'` (sees `a` and `A`), `'b'` (sees `b` and `B`), `'c'` (sees `c` and `C`).

### Example 2

```
Input:  word = "abc"
Output: 0
```

No uppercase letter anywhere.

### Example 3

```
Input:  word = "abBCab"
Output: 1
```

Only `'b'` qualifies — it appears as both `b` and `B`. `'c'` only appears as `C`; `'a'` only as `a`.

---

## Constraints

- `1 <= word.length <= 50`
- `word` consists of only lowercase and uppercase English letters.

---

## Intuition

### What we actually need to track

For each of the 26 letters, the question collapses to: **"did we see it in both cases?"** We don't care about counts or positions — just two yes/no flags per letter.

That maps cleanly onto **two hash sets**:
- `lower_seen` — lowercase letters that have appeared
- `upper_seen` — uppercase letters that have appeared

A letter `c` is special iff `c ∈ lower_seen` AND `c.upper() ∈ upper_seen`.

### Why not a `Counter`?

A `Counter` gives us *counts*, but we only need *presence* (at least one). Sets are the smaller, cleaner answer to the question being asked. Using a Counter would still work — it just stores more information than necessary.

### Iterate the smaller scope

When tallying special letters, we loop over `lower_seen` (at most 26 entries) and check membership in `upper_seen`. No need to iterate `word` again. The final count step is **O(26) = O(1)**.

### Single-pass build, constant-space final tally

The whole algorithm is:
1. Single pass over `word` to fill the two sets — O(n).
2. Walk one set (size ≤ 26) checking the other — O(1).

That's optimal: you must read the input at least once to learn what's in it.

---

## Algorithm

```
lower_seen = ∅
upper_seen = ∅

for ch in word:
    if ch is lowercase: add ch  to lower_seen
    else              : add ch  to upper_seen

return |{ c ∈ lower_seen : c.upper() ∈ upper_seen }|
```

---

## Solution

```python
class Solution:
    def numberOfSpecialChars(self, word: str) -> int:
        lower_seen = set()
        upper_seen = set()

        for ch in word:
            if ch.islower():
                lower_seen.add(ch)
            else:
                upper_seen.add(ch)

        return sum(1 for c in lower_seen if c.upper() in upper_seen)
```

---

## One-Liner Variant

```python
class Solution:
    def numberOfSpecialChars(self, word: str) -> int:
        return len({c for c in word if c.islower() and c.upper() in word})
```

Reads "count distinct lowercase letters whose uppercase form also appears in `word`."

- Slightly different cost profile: the `c.upper() in word` check is O(n) per letter, so this is **O(n²)** worst case.
- For `n ≤ 50` it's negligible. For larger inputs, prefer the two-set version.

---

## Complexity Analysis

For the two-set solution:

| | Complexity | Reason |
|---|---|---|
| **Time** | **O(n)** | One pass over `word` + at most 26 lookups |
| **Space** | **O(1)** | Both sets bounded by 26 letters |

Optimal — any algorithm must read the whole string to be sure of correctness.

---

## Full Trace — Example 1: `word = "aaAbcBC"`

**Build phase:**

| ch | `islower()` | `lower_seen` | `upper_seen` |
|:-:|:-:|---|---|
| `a` | T | `{a}` | `{}` |
| `a` | T | `{a}` | `{}` |
| `A` | F | `{a}` | `{A}` |
| `b` | T | `{a, b}` | `{A}` |
| `c` | T | `{a, b, c}` | `{A}` |
| `B` | F | `{a, b, c}` | `{A, B}` |
| `C` | F | `{a, b, c}` | `{A, B, C}` |

**Tally phase:**

| `c` | `c.upper()` | in `upper_seen`? |
|:-:|:-:|:-:|
| `a` | `A` | ✓ |
| `b` | `B` | ✓ |
| `c` | `C` | ✓ |

**Count = 3** ✓

---

## Full Trace — Example 3: `word = "abBCab"`

**Build phase:**

| ch | `lower_seen` | `upper_seen` |
|:-:|---|---|
| `a` | `{a}` | `{}` |
| `b` | `{a, b}` | `{}` |
| `B` | `{a, b}` | `{B}` |
| `C` | `{a, b}` | `{B, C}` |
| `a` | `{a, b}` | `{B, C}` |
| `b` | `{a, b}` | `{B, C}` |

**Tally phase:**

| `c` | `c.upper()` | in `upper_seen`? |
|:-:|:-:|:-:|
| `a` | `A` | ✗ |
| `b` | `B` | ✓ |

**Count = 1** ✓

Notice `c` (lowercase) was never in the string, only `C`, so it doesn't even enter the tally loop.

---

## Alternative — Bitmask Variant

For pure micro-efficiency, replace the sets with two 26-bit masks:

```python
def numberOfSpecialChars(self, word):
    lower = upper = 0
    for ch in word:
        if ch.islower():
            lower |= 1 << (ord(ch) - ord('a'))
        else:
            upper |= 1 << (ord(ch) - ord('A'))
    return bin(lower & upper).count('1')
```

The shared bit positions in `lower & upper` are exactly the letters that appeared in both cases. **O(n)** time, **O(1)** space, and the constant is tiny. Same asymptotic answer; just a fun variant.

---

## Key Insights

| Insight | Explanation |
|---|---|
| **Presence, not counts** | We only need "at least one occurrence in each case" — sets capture this perfectly. |
| **Bridge the two sets via `c.upper()`** | Lowercase set and uppercase set live in different alphabets; the case conversion connects them. |
| **Iterate the smaller scope** | Tally over `lower_seen` (≤ 26) instead of re-scanning `word`. |
| **Bitmask = set in 1 int** | For 26 letters, two integers fully encode "what we've seen"; `&` + popcount finishes the job. |

---

## Edge Cases

| Case | Behavior |
|---|---|
| `word = "a"` | Only lowercase → no uppercase to match → `0` |
| `word = "A"` | Only uppercase, but `lower_seen` is empty → `0` |
| `word = "aA"` | Both seen → `1` |
| `word = "AaBbCcDd"` | All 4 letters special → `4` |
| All same letter, both cases (`"aAaAaA"`) | Single special letter → `1` |
| All-uppercase string | `lower_seen` empty → `0` |

---

## Approach Tags

`Hash Set` · `Presence Tracking` · `String Scan` · `Constant Alphabet Bound`

---

*Day 22 of the LeetCode Daily Challenge*
