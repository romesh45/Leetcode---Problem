# Day 16 — LeetCode Challenge

## 2657. Find the Prefix Common Array of Two Arrays

| Field | Details |
|---|---|
| **Difficulty** | Medium |
| **Topics** | Bit Manipulation · Hash Set · Array · Simulation |
| **LeetCode Link** | [2657. Find the Prefix Common Array of Two Arrays](https://leetcode.com/problems/find-the-prefix-common-array-of-two-arrays/) |

---

## Problem Statement

You are given two **0-indexed permutations** `A` and `B`, each of length `n` (a permutation contains every integer `1 … n` exactly once).

The **prefix common array** `C` is defined so that `C[i]` equals the count of integers that appear **at or before index `i`** in **both** `A` and `B`.

Return `C`.

---

## Examples

### Example 1

```
Input:  A = [1, 3, 2, 4], B = [3, 1, 2, 4]
Output: [0, 2, 3, 4]
```

- `i = 0`: prefixes `{1}` and `{3}` → common `{}` → `0`
- `i = 1`: prefixes `{1,3}` and `{3,1}` → common `{1,3}` → `2`
- `i = 2`: prefixes `{1,3,2}` and `{3,1,2}` → common `{1,2,3}` → `3`
- `i = 3`: all four → `4`

### Example 2

```
Input:  A = [2, 3, 1], B = [3, 1, 2]
Output: [0, 1, 3]
```

- `i = 0`: `{2}` vs `{3}` → `0`
- `i = 1`: `{2,3}` vs `{3,1}` → common `{3}` → `1`
- `i = 2`: `{1,2,3}` vs `{1,2,3}` → `3`

---

## Constraints

- `1 <= A.length == B.length == n <= 50`
- `1 <= A[i], B[i] <= n`
- `A` and `B` are both permutations of `1 … n`.

---

## Intuition

### Track "what have I seen so far"

Scan both arrays left to right in lockstep. At each index `i`, maintain two growing sets:

- `seen_A` — values encountered so far in `A[0..i]`
- `seen_B` — values encountered so far in `B[0..i]`

`C[i]` is simply the **size of the intersection** `seen_A ∩ seen_B`.

### Two ways to represent "the set seen so far"

**(a) Hash sets** — `seen_A` and `seen_B` as Python `set`s, and `C[i] = len(seen_A & seen_B)`. Direct, readable.

**(b) Bitmasks** — since values are bounded by `n ≤ 50`, a single integer can hold the whole set: **bit `v` is set ⇔ value `v` has been seen**.
- "Add value `v`" → `mask |= (1 << v)`
- "Intersection" → `seen_A & seen_B`
- "Count common" → popcount of that AND

The bitmask version is elegant and fast — a few machine-word operations per step instead of set hashing.

### Why the AND captures exactly the common values

A value `v` is "common at or before `i`" exactly when it has appeared in **both** prefixes. In bitmask terms, bit `v` is set in `seen_A` **and** in `seen_B` → bit `v` is set in `seen_A & seen_B`. Counting those bits (`popcount`) gives `C[i]`.

### A neat consequence of permutations

Because both arrays are permutations of the *same* set `1…n`, after processing index `i` each prefix contains exactly `i + 1` **distinct** values. There are no duplicates to worry about — every `|=` flips a fresh bit.

---

## Algorithm

```
seen_A = 0
seen_B = 0
for i in 0 .. n-1:
    seen_A |= 1 << A[i]
    seen_B |= 1 << B[i]
    C[i] = popcount(seen_A & seen_B)
return C
```

---

## Solution

```python
from typing import List


class Solution:
    def findThePrefixCommonArray(self, A: List[int], B: List[int]) -> List[int]:
        n = len(A)
        C = [0] * n
        seen_A = 0
        seen_B = 0

        for i in range(n):
            seen_A |= (1 << A[i])
            seen_B |= (1 << B[i])
            C[i] = bin(seen_A & seen_B).count("1")

        return C
```

---

## Complexity Analysis

| | Complexity | Reason |
|---|---|---|
| **Time** | **O(n)** bitmask ops | One `|=`, one `&`, one popcount per index. Each operates on an `(n+1)`-bit integer → O(n/w) per op, so O(n²/w) precisely; effectively linear for `n ≤ 50` |
| **Space** | **O(1)** extra | Two integers (`seen_A`, `seen_B`); output array not counted |

For `n ≤ 50` this is effectively instantaneous.

---

## Full Trace — Example 1: `A = [1, 3, 2, 4], B = [3, 1, 2, 4]`

Bit `v` ↔ value `v`. Masks shown as the set of values whose bit is set.

| i | A[i] | B[i] | seen_A | seen_B | seen_A & seen_B | C[i] |
|:-:|:-:|:-:|---|---|---|:-:|
| 0 | 1 | 3 | `{1}` | `{3}` | `{}` | **0** |
| 1 | 3 | 1 | `{1,3}` | `{1,3}` | `{1,3}` | **2** |
| 2 | 2 | 2 | `{1,2,3}` | `{1,2,3}` | `{1,2,3}` | **3** |
| 3 | 4 | 4 | `{1,2,3,4}` | `{1,2,3,4}` | `{1,2,3,4}` | **4** |

Output: `[0, 2, 3, 4]` ✓

---

## Full Trace — Example 2: `A = [2, 3, 1], B = [3, 1, 2]`

| i | A[i] | B[i] | seen_A | seen_B | seen_A & seen_B | C[i] |
|:-:|:-:|:-:|---|---|---|:-:|
| 0 | 2 | 3 | `{2}` | `{3}` | `{}` | **0** |
| 1 | 3 | 1 | `{2,3}` | `{1,3}` | `{3}` | **1** |
| 2 | 1 | 2 | `{1,2,3}` | `{1,2,3}` | `{1,2,3}` | **3** |

Output: `[0, 1, 3]` ✓

---

## Alternative — Set-Based Solution

```python
from typing import List


class Solution:
    def findThePrefixCommonArray(self, A: List[int], B: List[int]) -> List[int]:
        seen_A, seen_B = set(), set()
        C = []
        for a, b in zip(A, B):
            seen_A.add(a)
            seen_B.add(b)
            C.append(len(seen_A & seen_B))
        return C
```

Same `O(n²)` worst-case work (the `&` rebuilds an intersection of size up to `n`), but reads very naturally. For these constraints, pick whichever you find clearer — the bitmask version simply replaces set hashing with single-word integer ops.

---

## Alternative — Counting Without Recomputing the Intersection

The intersection count is **monotonically non-decreasing** and only changes via the two new elements at step `i`. You can maintain a frequency array and a running counter:

```python
def findThePrefixCommonArray(self, A, B):
    n = len(A)
    freq = [0] * (n + 1)   # freq[v] = how many times v seen across A and B prefixes
    C = [0] * n
    common = 0
    for i in range(n):
        for v in (A[i], B[i]):
            freq[v] += 1
            if freq[v] == 2:        # v now appears in both prefixes
                common += 1
        C[i] = common
    return C
```

This is **true O(n)** — no per-step intersection or popcount. A value contributes to `common` exactly when its frequency hits 2 (seen once in each array). Note: if `A[i] == B[i]`, that single value's freq jumps `0 → 2` across the two updates and is counted once.

---

## Key Insights

| Insight | Explanation |
|---|---|
| **`C[i]` = size of intersection of the two prefixes** | Reframes the problem as incremental set-intersection tracking. |
| **Bitmask = a set in one integer** | Values bounded by `n ≤ 50` fit comfortably; set ops become bitwise ops. |
| **`seen_A & seen_B` is the common set** | AND keeps exactly the bits (values) present in both. |
| **Permutations ⇒ no duplicates** | Each `|=` always flips a new bit; prefix at index `i` has exactly `i+1` distinct values. |
| **Frequency-counter variant is strictly O(n)** | A value joins the common count the instant its global frequency reaches 2. |

---

## Edge Cases

| Case | Behavior |
|---|---|
| `n = 1` (`A = [1], B = [1]`) | Single step: both prefixes `{1}` → `C = [1]` |
| `A == B` | Every value is common immediately → `C = [1, 2, 3, …, n]` |
| `A` reversed of `B` | Common count stays low early, then jumps as prefixes overlap |
| `A[i] == B[i]` at some index | That value's bit is set in both masks the same step → counted correctly |

---

## Approach Tags

`Bit Manipulation` · `Bitmask as Set` · `Prefix Tracking` · `Frequency Counting`

---

*Day 16 of the LeetCode Daily Challenge*
