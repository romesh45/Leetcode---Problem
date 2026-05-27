# Day 23 — LeetCode Challenge

## 3121. Count the Number of Special Characters II

| Field | Details |
|---|---|
| **Difficulty** | Medium |
| **Topics** | Hash Map · Counting · String · Ordering |
| **LeetCode Link** | [3121. Count the Number of Special Characters II](https://leetcode.com/problems/count-the-number-of-special-characters-ii/) |

---

## Problem Statement

You are given a string `word`. A letter `c` is **special** if **all** of the following hold:

1. `c` appears in **both** lowercase and uppercase in `word`.
2. **Every** lowercase occurrence of `c` appears **before** the **first** uppercase occurrence of `c`.

Return the number of special letters.

---

## Examples

### Example 1

```
Input:  word = "aaAbcBC"
Output: 3
```

Indices: `a(0) a(1) A(2) b(3) c(4) B(5) C(6)`.

- `a`: lowercase ends at index `1`, first uppercase at `2`. `1 < 2` ✓
- `b`: lowercase at `3`, first uppercase at `5`. `3 < 5` ✓
- `c`: lowercase at `4`, first uppercase at `6`. `4 < 6` ✓

All three qualify → `3`.

### Example 2

```
Input:  word = "abc"
Output: 0
```

No uppercase letters → no letter qualifies.

### Example 3

```
Input:  word = "AbBCab"
Output: 0
```

Indices: `A(0) b(1) B(2) C(3) a(4) b(5)`.

- `a`: lowercase at `4`, uppercase `A` at `0`. `4 < 0`? No. ✗
- `b`: last lowercase at `5`, first uppercase at `2`. `5 < 2`? No. ✗
- `c`: only `C` exists, no lowercase. ✗

None qualify → `0`.

---

## Constraints

- `1 <= word.length <= 2 · 10⁵`
- `word` consists of only English letters (both cases).

---

## Intuition

### Reduce the rule to two indices

The ordering condition says **every** lowercase `c` precedes **the first** uppercase `c`. That's a quantifier over many occurrences — but it collapses to comparing two specific indices:

- **`last_lower[c]`** — the **latest** index where `c` (lowercase) appears.
  If even the last lowercase is before the first uppercase, then all earlier lowercase occurrences are too.
- **`first_upper[c]`** — the **earliest** index where `C` (uppercase) appears.
  If the very first uppercase already comes after the last lowercase, the later ones don't matter.

**A letter `c` is special ⇔ both indices exist AND `last_lower[c] < first_upper[c.upper()]`.**

This is the **worst-case meets worst-case** trick — pick the boundary that's hardest to beat on each side.

### Why "last lower vs first upper" and not other combinations

| Wrong combination | Why it fails |
|---|---|
| First lower vs first upper | Misses later lowercase occurrences that might violate the order (e.g. `"AbBCab"` — `a` first at 4, but the rule needs no lowercase *after* the first uppercase) |
| Last lower vs last upper | The first uppercase might already come *before* some lowercase; comparing to the last is too lenient |
| First lower vs last upper | Both bounds are loose — almost always passes when it shouldn't |

Only **last lower vs first upper** captures the exact rule.

### Building the maps in one pass

- Lowercase: `last_lower[c] = i` on every encounter (overwrite — natural way to "keep the last").
- Uppercase: `first_upper[c] = i` **only if not already present** (preserve the first).

After the pass, both maps have at most 26 entries each, so the final tally is constant-time.

---

## Algorithm

```
last_lower  = empty map
first_upper = empty map

for i, ch in enumerate(word):
    if ch is lowercase:
        last_lower[ch] = i              # always overwrite
    else:
        if ch not in first_upper:
            first_upper[ch] = i         # write only once

count = 0
for c, lo_idx in last_lower:
    if c.upper() in first_upper and lo_idx < first_upper[c.upper()]:
        count += 1
return count
```

---

## Solution

```python
class Solution:
    def numberOfSpecialChars(self, word: str) -> int:
        last_lower = {}
        first_upper = {}

        for i, ch in enumerate(word):
            if ch.islower():
                last_lower[ch] = i
            else:
                if ch not in first_upper:
                    first_upper[ch] = i

        count = 0
        for c, lo_idx in last_lower.items():
            up = c.upper()
            if up in first_upper and lo_idx < first_upper[up]:
                count += 1
        return count
```

---

## Complexity Analysis

| | Complexity | Reason |
|---|---|---|
| **Time** | **O(n)** | Single pass over `word`; final tally is ≤ 26 checks |
| **Space** | **O(1)** | Both maps bounded by 26 letters |

Optimal — the input must be read at least once.

---

## Full Trace — Example 1: `word = "aaAbcBC"`

**Build phase:**

| i | ch | `last_lower` | `first_upper` |
|:-:|:-:|---|---|
| 0 | a | `{a: 0}` | `{}` |
| 1 | a | `{a: 1}` (overwrite) | `{}` |
| 2 | A | `{a: 1}` | `{A: 2}` |
| 3 | b | `{a: 1, b: 3}` | `{A: 2}` |
| 4 | c | `{a: 1, b: 3, c: 4}` | `{A: 2}` |
| 5 | B | `{a: 1, b: 3, c: 4}` | `{A: 2, B: 5}` |
| 6 | C | `{a: 1, b: 3, c: 4}` | `{A: 2, B: 5, C: 6}` |

**Tally phase:**

| c | `last_lower[c]` | `c.upper()` in `first_upper`? | `last_lower[c] < first_upper[c.upper()]`? |
|:-:|:-:|:-:|:-:|
| a | 1 | A: 2 ✓ | `1 < 2` ✓ |
| b | 3 | B: 5 ✓ | `3 < 5` ✓ |
| c | 4 | C: 6 ✓ | `4 < 6` ✓ |

**Count = 3** ✓

---

## Full Trace — Example 3: `word = "AbBCab"`

**Build phase:**

| i | ch | `last_lower` | `first_upper` |
|:-:|:-:|---|---|
| 0 | A | `{}` | `{A: 0}` |
| 1 | b | `{b: 1}` | `{A: 0}` |
| 2 | B | `{b: 1}` | `{A: 0, B: 2}` |
| 3 | C | `{b: 1}` | `{A: 0, B: 2, C: 3}` |
| 4 | a | `{b: 1, a: 4}` | `{A: 0, B: 2, C: 3}` |
| 5 | b | `{b: 5, a: 4}` (overwrite) | `{A: 0, B: 2, C: 3}` |

**Tally phase:**

| c | `last_lower[c]` | `first_upper[c.upper()]` | `<`? |
|:-:|:-:|:-:|:-:|
| b | 5 | 2 | `5 < 2`? ✗ |
| a | 4 | 0 | `4 < 0`? ✗ |

(`c` not in `last_lower`, skipped.) **Count = 0** ✓

---

## Why "Last Lower vs First Upper" Is the Tight Boundary

We want to check: **for every lowercase occurrence at index `p` and every uppercase occurrence at index `q`, `p < q`.**

That's equivalent to: `max(p over lowercase) < min(q over uppercase)` — i.e., `last_lower[c] < first_upper[C]`.

If you compare any looser pair (like first lower vs first upper), you can pass the check while still having a later lowercase that violates the rule. If you compare any tighter pair, you'd over-reject. The two extremes are exactly right.

---

## Alternative — Single Pass with State Tracking

We can avoid the dictionaries by tracking, per letter:
- whether we've seen any uppercase yet (boolean), and
- whether any *new* lowercase appears after that.

```python
def numberOfSpecialChars(self, word):
    saw_upper = [False] * 26   # have we seen uppercase c?
    saw_lower = [False] * 26   # have we seen lowercase c?
    invalid   = [False] * 26   # have we seen lowercase AFTER uppercase?

    for ch in word:
        idx = (ord(ch) - ord('A')) % 32 - 1  # 0..25 for both cases
        # ... full implementation tracks the order events
```

This is more verbose; the two-map version is cleaner and equally efficient. The trade-off is purely stylistic for the given input size.

---

## Alternative — Bitmasks

For pure speed, two 26-bit masks + a "lowercase seen after uppercase" mask:

```python
def numberOfSpecialChars(self, word):
    upper_seen = 0
    lower_after_upper = 0   # bit c is set if a lowercase c appeared AFTER any uppercase c
    lower_seen = 0

    for ch in word:
        if ch.isupper():
            bit = 1 << (ord(ch) - ord('A'))
            upper_seen |= bit
        else:
            bit = 1 << (ord(ch) - ord('a'))
            lower_seen |= bit
            if upper_seen & bit:
                lower_after_upper |= bit

    # Special letters: lower seen AND upper seen AND NOT (lower after upper)
    return bin(lower_seen & upper_seen & ~lower_after_upper).count('1')
```

**O(n)** time, **O(1)** space, pure bitwise operations. Excellent if you love bit tricks.

---

## Key Insights

| Insight | Explanation |
|---|---|
| **Universal-quantifier ordering collapses to two indices** | "Every lowercase before first uppercase" ⇔ "last lowercase < first uppercase". |
| **Worst-case meets worst-case** | Take the latest lowercase (hardest to beat) and the earliest uppercase (lowest bar to clear). |
| **Maps bounded by 26 entries** | Final tally is O(1); the only linear work is reading the input. |
| **Bitmasks are a natural alternative** | The set of letters fits in 26 bits — set ops become bitwise ops. |
| **"At least once" vs "in order" need different data** | Day 22 (LC 3120) needed only presence sets; Day 23 needs index tracking. |

---

## Edge Cases

| Case | Behavior |
|---|---|
| `word = "aA"` | `last_lower[a]=0 < first_upper[A]=1` → **1** |
| `word = "Aa"` | `last_lower[a]=1 > first_upper[A]=0` → **0** |
| `word = "abc"` (no uppercase) | `first_upper` empty → **0** |
| `word = "ABC"` (no lowercase) | `last_lower` empty → tally loop empty → **0** |
| Mixed but only some satisfy | Counted individually per letter |
| All 26 letters in order then all uppercase | All 26 special → **26** |

---

## Approach Tags

`Hash Map` · `Index Tracking` · `Worst-Case Boundary` · `Single Pass`

---

## Comparison with LC 3120 (Day 22)

| Aspect | Day 22 (3120 — Special I) | Day 23 (3121 — Special II) |
|---|---|---|
| Special condition | Appears in both cases | Both cases + every lowercase before first uppercase |
| Data needed | Two presence sets | Two index maps (last lowercase, first uppercase) |
| Final check | `c ∈ lower AND c.upper() ∈ upper` | `last_lower[c] < first_upper[c.upper()]` |
| Time / Space | O(n) / O(1) | O(n) / O(1) |
| Bigger constraint | `n ≤ 50` | `n ≤ 2·10⁵` |

Same shape — single pass + 26-bounded final tally — but the extra ordering condition forces tracking indices instead of just presence.

---

*Day 23 of the LeetCode Daily Challenge*
