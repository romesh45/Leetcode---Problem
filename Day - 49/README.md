# Day 49 — LeetCode Challenge

## 1189. Maximum Number of Balloons

| Field | Details |
|---|---|
| **Difficulty** | Easy |
| **Topics** | Hash Table · Counting · String |
| **LeetCode Link** | [1189. Maximum Number of Balloons](https://leetcode.com/problems/maximum-number-of-balloons/) |

---

## Problem Statement

Given a string `text`, form as many copies of the word `"balloon"` as possible using each character of `text` **at most once**. Return the maximum number of instances.

---

## Examples

### Example 1
```
Input:  text = "nlaebolko"
Output: 1
```

### Example 2
```
Input:  text = "loonbalxballpoon"
Output: 2
```

### Example 3
```
Input:  text = "leetcode"
Output: 0
```

---

## Constraints

- `1 <= text.length <= 10⁴`
- `text` is lowercase English letters.

---

## Intuition

### It's a bottleneck problem

`"balloon"` has a fixed letter recipe:

```
b × 1,  a × 1,  l × 2,  o × 2,  n × 1
```

For each required letter, your supply alone supports `have[ch] // need[ch]` complete words. You can only build as many words as the **scarcest** ingredient permits — so the answer is the **minimum** of those ratios.

### The doubled letters are the trap

`l` and `o` each appear **twice** in `"balloon"`. If you only check raw counts (or forget to divide by 2), you'll over-count. Encoding the recipe as `Counter("balloon")` bakes in the `2`s, and `have[ch] // need[ch]` then divides correctly:

- 4 `l`s → `4 // 2 = 2` words' worth
- 3 `o`s → `3 // 2 = 1` word's worth

### Missing letters → automatic 0

A `Counter` returns `0` for absent keys. If `text` has no `b`, then `0 // 1 = 0`, which drives the `min` to `0` — exactly right, no special-casing.

---

## Algorithm

```
have = Counter(text)
need = Counter("balloon")          # {b:1, a:1, l:2, o:2, n:1}
return min(have[ch] // need[ch] for ch in need)
```

---

## Solution

```python
from collections import Counter


class Solution:
    def maxNumberOfBalloons(self, text: str) -> int:
        have = Counter(text)
        need = Counter("balloon")
        return min(have[ch] // cnt for ch, cnt in need.items())
```

---

## Complexity Analysis

| | Complexity | Reason |
|---|---|---|
| **Time** | **O(n)** | One pass to count `text`; the final `min` is over 5 fixed letters |
| **Space** | **O(1)** | The counter holds at most 26 keys |

---

## Full Trace — Example 2: `text = "loonbalxballpoon"`

**Count `text`:** `b:2, a:2, l:4, o:4, n:2` (plus `x:1, p:1` — ignored).

**Recipe ratios:**

| letter | have | need | `have // need` |
|:-:|:-:|:-:|:-:|
| b | 2 | 1 | 2 |
| a | 2 | 1 | 2 |
| l | 4 | 2 | 2 |
| o | 4 | 2 | 2 |
| n | 2 | 1 | 2 |

`min(2,2,2,2,2)` = **2** ✓

---

## Full Trace — Example 1: `text = "nlaebolko"`

Count: `n:1, l:2, a:1, e:1, b:1, o:2, k:1`.

| letter | have | need | `have // need` |
|:-:|:-:|:-:|:-:|
| b | 1 | 1 | 1 |
| a | 1 | 1 | 1 |
| l | 2 | 2 | 1 |
| o | 2 | 2 | 1 |
| n | 1 | 1 | 1 |

`min = 1` → **1** ✓ (note `o` appears twice — easy to miscount.)

---

## Why the Minimum, Not the Sum or Product

Building one `"balloon"` consumes one unit of *each* required letter (with `l`, `o` counted double). It's a conjunction — you need `b` **and** `a` **and** two `l`s **and** two `o`s **and** `n`, all at once. The number of complete sets you can assemble is limited by whichever ingredient runs out first, i.e. the smallest `have // need`. Summing or multiplying would ignore the "all together" requirement. ∎

---

## Key Insights

| Insight | Explanation |
|---|---|
| **Bottleneck = min ratio** | Words are capped by the scarcest required letter. |
| **Encode the recipe with `Counter`** | `Counter("balloon")` captures the ×2 for `l` and `o` automatically. |
| **Integer division handles doubles** | `have // need` divides the doubled-letter supply correctly. |
| **`Counter` → 0 for missing keys** | Absent ingredients force the answer to 0, no special case. |

---

## Edge Cases

| Case | Behavior |
|---|---|
| Missing a required letter | That ratio is 0 → answer 0 (Example 3) |
| Exactly one `"balloon"` worth | Returns 1 |
| Surplus of non-`balloon` letters | Ignored entirely |
| Odd count of `l` or `o` | Floored (e.g. 3 `l`s → supports 1 word) |
| Multiple full copies | `min` of the per-letter ratios |

---

## Approach Tags

`Frequency Counting` · `Bottleneck / Min Ratio` · `Recipe Matching` · `Hash Table`

---

*Day 49 of the LeetCode Daily Challenge*
