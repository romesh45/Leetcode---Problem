# Day 10 — LeetCode Challenge

## 2784. Check if Array is Good

| Field | Details |
|---|---|
| **Difficulty** | Easy |
| **Topics** | Array · Sorting · Hash Table · Counting |
| **LeetCode Link** | [2784. Check if Array is Good](https://leetcode.com/problems/check-if-array-is-good/) |

---

## Problem Statement

You are given an integer array `nums`. The array is **good** if it is a permutation of:

```
base[n] = [1, 2, ..., n − 1, n, n]
```

That is, a length-`(n + 1)` array containing each of `1 … n − 1` exactly once, plus **two** copies of `n`.

Examples:
- `base[1] = [1, 1]`
- `base[3] = [1, 2, 3, 3]`
- `base[4] = [1, 2, 3, 4, 4]`

Return `true` if `nums` is a permutation of `base[n]` for some `n`, else `false`.

---

## Examples

### Example 1

```
Input:  nums = [2, 1, 3]
Output: false
```

`max = 3` ⇒ candidate `n = 3` ⇒ `base[3]` has 4 elements but `nums` has 3.

### Example 2

```
Input:  nums = [1, 3, 3, 2]
Output: true
```

`max = 3`, `len = 4 = n + 1` ✓, sorted `nums = [1, 2, 3, 3] = base[3]` ✓.

### Example 3

```
Input:  nums = [1, 1]
Output: true
```

`base[1] = [1, 1]`, exact match.

### Example 4

```
Input:  nums = [3, 4, 4, 1, 2, 1]
Output: false
```

`max = 4` ⇒ `base[4]` has 5 elements but `nums` has 6.

---

## Constraints

- `1 <= nums.length <= 100`
- `1 <= nums[i] <= 200`

---

## Intuition

### `n` is **forced** — no search needed

Whatever `n` is, the array `base[n]` contains `n` as its largest element. So:

```
n = max(nums)
```

There's no ambiguity, no candidates to try. Pick `n`, then **verify** that `nums` is a permutation of `base[n]`.

### Two cheap checks are enough

For `nums` to equal `base[n]` as a multiset:

1. **Length check** — `len(nums) == n + 1`.
   Catches Examples 1 & 4 instantly, before any sorting.

2. **Content check** — sorted `nums` must equal `[1, 2, …, n−1, n, n]`.
   Equivalently: each of `1..n−1` appears once and `n` appears twice.

If both hold, the array is good.

### Why sorting works as the verifier

Two multisets are equal **iff** their sorted forms are identical. Sorting `nums` and comparing it to the canonical `base[n]` is a one-liner that handles every constraint in one shot:
- duplicate `n`? ✓
- missing values in `1..n−1`? ✗ (sorted form would differ)
- stray values like `0` or `n + 1`? ✗ (sorted form would differ)

---

## Algorithm

```
1. n = max(nums)

2. if len(nums) != n + 1:
       return False

3. nums.sort()
   expected = [1, 2, ..., n - 1, n, n]
   return nums == expected
```

Alternative (no sorting) — use a counter:

```
1. n = max(nums)
2. if len(nums) != n + 1: return False
3. count = Counter(nums)
4. return count[n] == 2 and all(count[v] == 1 for v in range(1, n))
```

Both are O(n) up to the sort factor.

---

## Solution

```python
from typing import List


class Solution:
    def isGood(self, nums: List[int]) -> bool:
        n = max(nums)

        # Length must be exactly n + 1 to match base[n].
        if len(nums) != n + 1:
            return False

        # Sorted nums must equal [1, 2, ..., n-1, n, n].
        nums.sort()
        expected = list(range(1, n)) + [n, n]
        return nums == expected
```

---

## Complexity Analysis

| | Complexity | Reason |
|---|---|---|
| **Time** | **O(n log n)** | Dominated by the sort; the max and length checks are linear |
| **Space** | **O(n)** | Building the `expected` reference list (sort itself is in-place) |

A counting variant runs in **O(n)** time and **O(n)** auxiliary space.

---

## Full Trace — Example 2: `nums = [1, 3, 3, 2]`

| Step | State |
|---|---|
| `n = max(nums)` | `n = 3` |
| `len(nums) == n + 1` | `4 == 4` ✓ |
| `nums.sort()` | `[1, 2, 3, 3]` |
| `expected` | `[1, 2, 3, 3]` |
| Compare | equal → **return True** ✓ |

---

## Full Trace — Example 4: `nums = [3, 4, 4, 1, 2, 1]`

| Step | State |
|---|---|
| `n = max(nums)` | `n = 4` |
| `len(nums) == n + 1` | `6 == 5` ✗ |
| Short-circuit | **return False** ✓ |

No sort needed — the length check alone rejects the input.

---

## Key Insights

| Insight | Explanation |
|---|---|
| **`n` is determined by `max(nums)`** | `base[n]` always contains `n` as its largest element, so there's a single candidate to verify. |
| **Length filter first** | A constant-time `len(nums) == n + 1` check eliminates obvious failures before any sorting/counting. |
| **Sorted comparison is a multiset comparison** | Comparing the sorted array to `[1..n−1, n, n]` is the cleanest way to verify all values and counts in one go. |
| **No need to track which `n` to try** | Many "is this a permutation of …" problems get harder when the target shape is ambiguous; here it's fully fixed. |

---

## Alternative — Counter Solution

```python
from collections import Counter
from typing import List


class Solution:
    def isGood(self, nums: List[int]) -> bool:
        n = max(nums)
        if len(nums) != n + 1:
            return False
        count = Counter(nums)
        if count[n] != 2:
            return False
        return all(count[v] == 1 for v in range(1, n))
```

Runs in pure O(n) — useful if you want to avoid the sort, though for `n ≤ 100` it's indistinguishable in practice.

---

## Edge Cases

| Case | Behavior |
|---|---|
| `nums = [1, 1]` | `n=1`, len matches, sorted equals `[1, 1]` → **True** |
| `nums = [1]` | `n=1`, len `1 ≠ 2` → **False** |
| `nums = [2, 2]` | `n=2`, len `2 ≠ 3` → **False** (missing `1`) |
| `nums = [1, 2, 2]` | `n=2`, sorted `[1, 2, 2]` = `base[2]` → **True** |
| `nums = [1, 2, 3, 3, 3]` | `n=3`, len `5 ≠ 4` → **False** (too many `3`s) |
| `nums` missing a middle value | Sorted form differs from `base[n]` → **False** |

---

## Approach Tags

`Array` · `Sorting` · `Permutation Check` · `Counting`

---

*Day 10 of the LeetCode Daily Challenge*
