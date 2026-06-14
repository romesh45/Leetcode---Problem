# Day 41 — LeetCode Challenge

## 3838. Weighted Word Mapping

| Field | Details |
|---|---|
| **Difficulty** | Easy |
| **Topics** | String · Math · Hash/Array Lookup · Modular Arithmetic |
| **LeetCode Link** | [3838. Weighted Word Mapping](https://leetcode.com/problems/weighted-word-mapping/) |

---

## Problem Statement

You're given an array of lowercase words `words` and an integer array `weights` of length 26, where `weights[i]` is the weight of the `i`-th letter.

The **weight of a word** is the sum of its characters' weights. For each word:

1. Take its weight **modulo 26**.
2. Map the result to a letter using **reverse alphabetical order**: `0 → 'z'`, `1 → 'y'`, …, `25 → 'a'`.

Return the string formed by concatenating the mapped characters for all words, in order.

---

## Examples

### Example 1

```
Input:  words = ["abcd","def","xyz"],
        weights = [5,3,12,14,1,2,3,2,10,6,6,9,7,8,7,10,8,9,6,9,9,8,3,7,7,2]
Output: "rij"
```

- `"abcd"` → `5+3+12+14 = 34`, `34 % 26 = 8` → `'r'`
- `"def"` → `14+1+2 = 17`, `17 % 26 = 17` → `'i'`
- `"xyz"` → `7+7+2 = 16`, `16 % 26 = 16` → `'j'`

### Example 2

```
Input:  words = ["a","b","c"], weights = [1,1,…,1]
Output: "yyy"
```

Each weight is `1`, `1 % 26 = 1` → `'y'`.

### Example 3

```
Input:  words = ["abcd"], weights = [7,5,3,4,…]
Output: "g"
```

`7+5+3+4 = 19`, `19 % 26 = 19` → `'g'`.

---

## Constraints

- `1 <= words.length <= 100`
- `1 <= words[i].length <= 10`
- `weights.length == 26`
- `1 <= weights[i] <= 100`
- Lowercase letters only.

---

## Intuition

### Three mechanical steps per word

There's no hidden trick — just careful index arithmetic:

1. **Letter → weight:** letter `c` sits at alphabet position `ord(c) - ord('a')`, so its weight is `weights[ord(c) - 97]`. Sum over the word.
2. **Mod 26:** collapse the sum into `0..25`.
3. **Reverse-alphabet map:** `0 → 'z'`, `1 → 'y'`, …, `25 → 'a'`.

### The clean reverse-map formula

The reverse map doesn't need a lookup table. Since `'z'` is `122` and `'a'` is `97`:

```
122 − 0  = 122 = 'z'
122 − 1  = 121 = 'y'
…
122 − 25 = 97  = 'a'
```

So result `r` maps directly to **`chr(122 - r)`**. Equivalently `chr(ord('z') - r)`.

> Sanity check: `'a' + (25 - r)` gives the same letter — both express "count down from z." The `122 - r` form is the tersest.

### Why mod 26 keeps it in range

`r = weight % 26 ∈ [0, 25]`, so `122 - r ∈ [97, 122]` = exactly `'a'..'z'`. No clamping needed.

---

## Algorithm

```
result = []
for word in words:
    total = Σ weights[ord(c) - 'a']  for c in word
    r = total % 26
    result.append(chr(ord('z') - r))
return "".join(result)
```

---

## Solution

```python
from typing import List


class Solution:
    def mapWordWeights(self, words: List[str], weights: List[int]) -> str:
        result = []
        for word in words:
            total = sum(weights[ord(c) - 97] for c in word)
            r = total % 26
            result.append(chr(122 - r))
        return "".join(result)
```

---

## Complexity Analysis

Let `W = len(words)` and `L` = max word length (`≤ 10`).

| | Complexity | Reason |
|---|---|---|
| **Time** | **O(Σ word lengths)** | Each character contributes one O(1) weight lookup |
| **Space** | **O(W)** | The output string (one char per word) |

With `W ≤ 100` and `L ≤ 10`, at most ~1000 character operations — instant.

---

## Full Trace — Example 1: `["abcd", "def", "xyz"]`

Using `weights = [5,3,12,14,1,2,3,2,10,6,6,9,7,8,7,10,8,9,6,9,9,8,3,7,7,2]`.

| Word | Letter weights | Sum | `% 26` | `chr(122 − r)` |
|:-:|---|:-:|:-:|:-:|
| `abcd` | `5, 3, 12, 14` | 34 | 8 | `chr(114)` = `'r'` |
| `def` | `14, 1, 2` | 17 | 17 | `chr(105)` = `'i'` |
| `xyz` | `7, 7, 2` | 16 | 16 | `chr(106)` = `'j'` |

Concatenate → **`"rij"`** ✓

(For `"def"`: `d`=index 3 → weight 14, `e`=index 4 → weight 1, `f`=index 5 → weight 2.)

---

## Why `chr(122 - r)` Is the Reverse Map

The forward alphabet is `'a'(97) … 'z'(122)`. "Reverse alphabetical order" means index `0` should be the *last* letter and index `25` the *first*:

```
r:        0    1    2   …   24   25
maps to:  z    y    x   …    b    a
ASCII:   122  121  120  …   98   97
```

That's a strictly decreasing line: `ASCII = 122 − r`. So `chr(122 - r)` is the whole mapping in one expression. ∎

---

## Key Insights

| Insight | Explanation |
|---|---|
| **Index arithmetic, not a dict** | `ord(c) - 97` indexes the weight array directly — no hashing. |
| **Reverse map = `chr(122 - r)`** | `'z' - r` walks the alphabet backward; no lookup table. |
| **Mod 26 guarantees a valid letter** | `r ∈ [0,25]` ⇒ `122 - r ∈ ['a','z']`, always in range. |
| **Build a list, join once** | Avoids repeated string concatenation. |

---

## Edge Cases

| Case | Behavior |
|---|---|
| Weight a multiple of 26 | `r = 0` → maps to `'z'` |
| `r = 25` | Maps to `'a'` |
| Single-letter words | Weight is just that letter's value |
| Repeated letters | Each occurrence adds its weight again |
| All weights equal | All words of equal length map to the same letter |

---

## Approach Tags

`String Processing` · `Array Lookup` · `Modular Arithmetic` · `Reverse Alphabet Map`

---

*Day 41 of the LeetCode Daily Challenge*
