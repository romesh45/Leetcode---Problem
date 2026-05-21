# Day 17 — LeetCode Challenge

## 3043. Find the Length of the Longest Common Prefix

| Field | Details |
|---|---|
| **Difficulty** | Medium |
| **Topics** | Hash Set · Trie · String · Math |
| **LeetCode Link** | [3043. Find the Length of the Longest Common Prefix](https://leetcode.com/problems/find-the-length-of-the-longest-common-prefix/) |

---

## Problem Statement

You are given two arrays of positive integers `arr1` and `arr2`.

A **prefix** of a positive integer is an integer formed from one or more of its **leftmost** digits — e.g. `123` is a prefix of `12345`, but `234` is not.

A **common prefix** of integers `a` and `b` is an integer `c` that is a prefix of both. For example `5655359` and `56554` share common prefixes `565` and `5655`.

Across **all pairs** `(x, y)` with `x ∈ arr1` and `y ∈ arr2`, return the **length of the longest common prefix**. If no pair shares any common prefix, return `0`.

---

## Examples

### Example 1

```
Input:  arr1 = [1, 10, 100], arr2 = [1000]
Output: 3
```

Pairs with `1000`: prefixes `1`, `10`, `100` all match → longest is `100` (length 3).

### Example 2

```
Input:  arr1 = [1, 2, 3], arr2 = [4, 4, 4]
Output: 0
```

No pair across the two arrays shares a leading digit. (Common prefixes *within* the same array don't count.)

---

## Constraints

- `1 <= arr1.length, arr2.length <= 5 · 10⁴`
- `1 <= arr1[i], arr2[i] <= 10⁸`

---

## Intuition

### Why brute force fails

Checking every pair is `|arr1| × |arr2|` ≤ `5·10⁴ × 5·10⁴ = 2.5·10⁹` comparisons — far too slow.

We need to **decouple** the two arrays: preprocess one, then query with the other.

### Key observation — `// 10` strips a digit

Integer-dividing a number by 10 removes its **last** digit:

```
12345 // 10 = 1234
 1234 // 10 = 123
  123 // 10 = 12
```

So the sequence `num, num//10, num//100, …` enumerates **exactly all prefixes** of `num`, from longest down to shortest. No string conversion needed to generate them.

### The plan: hash set of prefixes

**Build phase** — for every number in `arr1`, push all its prefixes into a set:

```
arr1 = [1, 10, 100]
prefixes = {1, 10, 100}   (1→{1}, 10→{10,1}, 100→{100,10,1})
```

**Query phase** — for each number in `arr2`, generate its prefixes **longest first** and look each up in the set. The first hit is the longest common prefix involving that number; record its digit length.

```
arr2 = [1000] → prefixes 1000, 100, 10, 1
1000 ∉ set; 100 ∈ set → length 3, stop.
```

Answer = max length over all of `arr2` = **3**.

### Why "longest first, then break"

In the query phase we test `num, num//10, …` — that's longest to shortest. The **first** match is therefore guaranteed to be the longest matching prefix for that number, so we can `break` immediately.

---

## Algorithm

```
prefixes = empty set
for num in arr1:
    while num > 0:
        add num to prefixes
        num //= 10

best = 0
for num in arr2:
    while num > 0:
        if num in prefixes:
            best = max(best, number_of_digits(num))
            break
        num //= 10

return best
```

---

## Solution

```python
from typing import List


class Solution:
    def longestCommonPrefix(self, arr1: List[int], arr2: List[int]) -> int:
        prefixes = set()
        for num in arr1:
            while num:
                prefixes.add(num)
                num //= 10

        best = 0
        for num in arr2:
            while num:
                if num in prefixes:
                    best = max(best, len(str(num)))
                    break
                num //= 10

        return best
```

---

## Complexity Analysis

Let `n = len(arr1)`, `m = len(arr2)`, and `D` = maximum digit count. Since values ≤ `10⁸`, **`D ≤ 9`**.

| | Complexity | Reason |
|---|---|---|
| **Time** | **O((n + m) · D)** | Each number generates ≤ `D` prefixes; set ops are O(1) average. Effectively linear. |
| **Space** | **O(n · D)** | The prefix set holds up to `n · D` distinct integers |

For the given limits this is ~`9 · 10⁵` operations — instant.

---

## Full Trace — Example 1: `arr1 = [1, 10, 100], arr2 = [1000]`

**Build phase:**

| num | prefixes generated | set after |
|:-:|---|---|
| 1 | `1` | `{1}` |
| 10 | `10, 1` | `{1, 10}` |
| 100 | `100, 10, 1` | `{1, 10, 100}` |

**Query phase** — `arr2 = [1000]`:

| Strip step | value | in set? |
|:-:|:-:|:-:|
| 1 | 1000 | no |
| 2 | 100 | **yes** → length `3`, break |

`best = 3`.

**Answer: 3** ✓

---

## Full Trace — Example 2: `arr1 = [1, 2, 3], arr2 = [4, 4, 4]`

**Build phase:** `prefixes = {1, 2, 3}`.

**Query phase** — each `4`:

| value | // 10 | in set? |
|:-:|:-:|:-:|
| 4 | 0 (loop ends) | no |

No element of `arr2` ever hits the set. `best` stays `0`.

**Answer: 0** ✓

---

## Why Not a Trie?

A digit-trie is the textbook structure for "longest common prefix" and is perfectly valid here:

- Insert each `arr1` number digit-by-digit into a 10-ary trie.
- For each `arr2` number, walk the trie and count how deep you get.

It has the same `O((n + m) · D)` complexity. The hash-set approach wins on **simplicity** — no node class, no pointers — while exploiting the same `D ≤ 9` bound. The set *is* effectively a flattened trie keyed by the prefix integer itself.

---

## Alternative — String Prefixes

You can also treat numbers as strings and store string prefixes:

```python
def longestCommonPrefix(self, arr1, arr2):
    prefixes = set()
    for num in arr1:
        s = str(num)
        for k in range(1, len(s) + 1):
            prefixes.add(s[:k])
    best = 0
    for num in arr2:
        s = str(num)
        for k in range(len(s), 0, -1):
            if s[:k] in prefixes:
                best = max(best, k)
                break
    return best
```

Functionally identical. The integer `// 10` version avoids slicing and string hashing, so it's a touch faster — but both pass comfortably.

---

## Key Insights

| Insight | Explanation |
|---|---|
| **Decouple the arrays** | Preprocess `arr1` into a set, then query with `arr2` — turns `O(n·m)` into `O(n + m)`. |
| **`// 10` enumerates prefixes** | Repeated integer division strips digits right-to-left, yielding all prefixes longest→shortest. |
| **Longest-first query + break** | The first set hit during the query is automatically the longest match for that number. |
| **`D ≤ 9` keeps it linear** | Values ≤ `10⁸` cap the prefix count per number at 9 — the digit factor is a small constant. |
| **The set is a flattened trie** | Each stored prefix integer is one trie path; lookup replaces a trie walk. |

---

## Edge Cases

| Case | Behavior |
|---|---|
| `arr1 = [1], arr2 = [1]` | Prefix `1` matches → length `1` |
| Identical 9-digit numbers | Full match → length `9` (the maximum possible) |
| No shared leading digit anywhere | No query ever hits the set → return `0` |
| One number is a prefix of another (`12` vs `12345`) | `12` found → length `2` |
| Duplicates within an array | Harmless — set dedupes; query still correct |

---

## Approach Tags

`Hash Set` · `Prefix Enumeration` · `Integer Digit Stripping` · `Trie (conceptual)`

---

*Day 17 of the LeetCode Daily Challenge*
