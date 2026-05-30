# Day 25 — LeetCode Challenge

## 3300. Minimum Element After Replacement With Digit Sum

| Field | Details |
|---|---|
| **Difficulty** | Easy |
| **Topics** | Array · Math · Digit Sum · Single Pass |
| **LeetCode Link** | [3300. Minimum Element After Replacement With Digit Sum](https://leetcode.com/problems/minimum-element-after-replacement-with-digit-sum/) |

---

## Problem Statement

You are given an integer array `nums`. Replace each element with the **sum of its digits**. Return the **minimum** element of the resulting array.

---

## Examples

### Example 1

```
Input:  nums = [10, 12, 13, 14]
Output: 1
```

After digit-sum replacement: `[1+0, 1+2, 1+3, 1+4] = [1, 3, 4, 5]` → min `1`.

### Example 2

```
Input:  nums = [1, 2, 3, 4]
Output: 1
```

Single-digit numbers are unchanged → `[1, 2, 3, 4]` → min `1`.

### Example 3

```
Input:  nums = [999, 19, 199]
Output: 10
```

Digit sums: `9+9+9 = 27`, `1+9 = 10`, `1+9+9 = 19` → `[27, 10, 19]` → min `10`.

---

## Constraints

- `1 <= nums.length <= 100`
- `1 <= nums[i] <= 10⁴`

---

## Intuition

### Two micro-decisions

1. **Don't materialize the replaced array.** We only need the minimum, so we can stream digit sums into `min()` directly. Same complexity, less memory, clearer intent.
2. **Use integer arithmetic for digit sums.** Pulling digits with `% 10` and `// 10` avoids the string-conversion overhead of `str(x)`. Trivial for these inputs, but it's the right default reflex.

### How `% 10` and `// 10` reconstruct the digit sum

`x % 10` returns the **last digit** of `x` (the remainder when divided by 10).
`x // 10` is `x` with that last digit **stripped**.

So `while x: s += x % 10; x //= 10` walks through the digits right-to-left:

```
x = 199 → digit 9, x becomes 19
x =  19 → digit 9, x becomes 1
x =   1 → digit 1, x becomes 0
total = 9 + 9 + 1 = 19
```

For values up to `10⁴` we have at most 5 digits, so this is at most 5 iterations per number.

### Quick sanity check on bounds

A single-digit number maps to itself. So if `nums` contains *any* value in `1..9`, the answer is at most `9`. The minimum digit-sum overall is `1` (for `1, 10, 100, 1000, 10000, …`).

The maximum possible digit sum for `nums[i] ≤ 10⁴` is `9 + 9 + 9 + 9 = 36` (e.g. `9999`).

### One unified expression

`min(digit_sum(x) for x in nums)` cleanly captures the whole computation. No state, no edge cases.

---

## Algorithm

```
digit_sum(x):
    s = 0
    while x > 0:
        s += x mod 10
        x  = x // 10
    return s

return min(digit_sum(x) for x in nums)
```

---

## Solution

```python
from typing import List


class Solution:
    def minElement(self, nums: List[int]) -> int:
        def digit_sum(x: int) -> int:
            s = 0
            while x:
                s += x % 10
                x //= 10
            return s

        return min(digit_sum(x) for x in nums)
```

---

## One-Liner Variant (String-Based)

```python
class Solution:
    def minElement(self, nums: List[int]) -> int:
        return min(sum(int(d) for d in str(x)) for x in nums)
```

Reads "for each `x`, sum its digits as characters; take the min." Equally correct, a touch slower because of string conversion and per-character `int()` parsing — negligible at `n ≤ 100`.

---

## Complexity Analysis

| | Complexity | Reason |
|---|---|---|
| **Time** | **O(n · D)** = **O(n)** | `D ≤ 5` digits per number (since `nums[i] ≤ 10⁴`); each digit is constant work |
| **Space** | **O(1)** | A single accumulator inside `digit_sum`, plus the streaming min |

For `n ≤ 100` this is at most ~500 operations — instantaneous.

---

## Full Trace — Example 3: `nums = [999, 19, 199]`

**Iteration 1** — `x = 999`:
| step | `x` | `x % 10` | running `s` |
|:-:|:-:|:-:|:-:|
| start | 999 | — | 0 |
| 1 | 99 | 9 | 9 |
| 2 | 9 | 9 | 18 |
| 3 | 0 | 9 | 27 |

→ `digit_sum(999) = 27`. Current min = `27`.

**Iteration 2** — `x = 19`:
| step | `x` | `x % 10` | `s` |
|:-:|:-:|:-:|:-:|
| start | 19 | — | 0 |
| 1 | 1 | 9 | 9 |
| 2 | 0 | 1 | 10 |

→ `digit_sum(19) = 10`. Current min = `min(27, 10) = 10`.

**Iteration 3** — `x = 199`:
| step | `x` | `x % 10` | `s` |
|:-:|:-:|:-:|:-:|
| start | 199 | — | 0 |
| 1 | 19 | 9 | 9 |
| 2 | 1 | 9 | 18 |
| 3 | 0 | 1 | 19 |

→ `digit_sum(199) = 19`. Current min stays `10`.

**Answer: `10`** ✓

---

## Why Integer Arithmetic Beats String Conversion

For tiny inputs the difference is academic, but the integer version:

- Avoids allocating a temporary string of digit characters.
- Avoids `int(d)` parsing for each digit (Python re-creates a small int each time).
- Loops over a bounded `D` (≤ 5 here) using single-cycle CPU ops.

The string version is more idiomatic and reads better; pick it for readability if you don't care about a small constant factor.

---

## Key Insights

| Insight | Explanation |
|---|---|
| **Stream, don't materialize** | The answer only needs the min, so feed digit sums straight into `min()`. |
| **`% 10` / `// 10` is the canonical digit extractor** | Pure arithmetic, no string overhead, terminates in `O(log₁₀ x)` steps. |
| **Single-digit numbers are fixed points** | `digit_sum(d) = d` for `d ∈ 1..9`; any single-digit in `nums` caps the answer. |
| **Output range is tight** | For `nums[i] ≤ 10⁴`, the digit sum is in `[1, 36]`. |

---

## Edge Cases

| Case | Behavior |
|---|---|
| `nums = [1]` | `digit_sum(1) = 1` → return `1` |
| `nums = [10000]` | `1 + 0 + 0 + 0 + 0 = 1` → return `1` |
| `nums = [9999]` | `9·4 = 36` (max possible) → return `36` |
| All elements equal | Same digit sum across the board → that value |
| Mix of single- and multi-digit | Single-digit `1` (or `9999 → 36`, etc.) wins via min |

---

## Approach Tags

`Digit Sum` · `Single Pass` · `Math` · `Streaming Min`

---

*Day 25 of the LeetCode Daily Challenge*
