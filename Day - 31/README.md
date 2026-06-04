# Day 31 — LeetCode Challenge

## 3751. Total Waviness of Numbers in Range I

| Field | Details |
|---|---|
| **Difficulty** | Medium |
| **Topics** | Math · Digit Manipulation · Brute Force · Simulation |
| **LeetCode Link** | [3751. Total Waviness of Numbers in Range I](https://leetcode.com/problems/total-waviness-of-numbers-in-range-i/) |

---

## Problem Statement

Given two integers `num1` and `num2` defining an inclusive range `[num1, num2]`, compute the **total waviness** of all numbers in that range.

The **waviness** of a single number is the count of its **peaks** and **valleys**:

- A digit is a **peak** if it is **strictly greater** than *both* immediate neighbors.
- A digit is a **valley** if it is **strictly less** than *both* immediate neighbors.
- The **first and last** digits can never be peaks or valleys.
- Any number with fewer than 3 digits has waviness `0`.

Return the sum of waviness over every number in `[num1, num2]`.

---

## Examples

### Example 1

```
Input:  num1 = 120, num2 = 130
Output: 3
```

- `120`: middle `2` is a peak → 1
- `121`: middle `2` is a peak → 1
- `130`: middle `3` is a peak → 1

Total = `3`.

### Example 2

```
Input:  num1 = 198, num2 = 202
Output: 3
```

- `198`: middle `9` peak → 1
- `201`: middle `0` valley → 1
- `202`: middle `0` valley → 1

Total = `3`.

### Example 3

```
Input:  num1 = 4848, num2 = 4848
Output: 2
```

`4848`: digit `8` (index 1) is a peak, digit `4` (index 2) is a valley → waviness `2`.

---

## Constraints

- `1 <= num1 <= num2 <= 10⁵`

---

## Intuition

### The range is small — just enumerate

`num2 ≤ 10⁵`, so the range contains at most `100,000` numbers, each with at most 6 digits. Checking every number digit-by-digit is about `6·10⁵` comparisons — completely negligible. No cleverness required for the "I" version.

### Per-number waviness check

For a number, convert it to a list of digits and scan the **interior** positions:

```
number:   1  2  1  2  1
index:    0  1  2  3  4
          ↑              ↑
        first          last   ← never peaks/valleys
              ╰──┬──┬──╯
               interior (indices 1..len-2)
```

For each interior index `i`:
- **Peak:** `d[i] > d[i-1]` **and** `d[i] > d[i+1]`.
- **Valley:** `d[i] < d[i-1]` **and** `d[i] < d[i+1]`.

Both conditions use **strict** inequalities, so flat spots (equal neighbors) count as neither.

### Short numbers fall out for free

For a number with `len ≤ 2`, the interior loop `range(1, len-1)` is **empty** (e.g. `range(1, 1)` or `range(1, 0)`), so it contributes `0` without any special-case check. Clean.

---

## Algorithm

```
total = 0
for n in [num1 .. num2]:
    d = digits(n)
    for i in 1 .. len(d)-2:
        if d[i] > d[i-1] and d[i] > d[i+1]: total += 1   # peak
        elif d[i] < d[i-1] and d[i] < d[i+1]: total += 1  # valley
return total
```

---

## Solution

```python
class Solution:
    def totalWaviness(self, num1: int, num2: int) -> int:
        def waviness(n: int) -> int:
            d = list(map(int, str(n)))
            count = 0
            for i in range(1, len(d) - 1):
                if d[i] > d[i - 1] and d[i] > d[i + 1]:
                    count += 1
                elif d[i] < d[i - 1] and d[i] < d[i + 1]:
                    count += 1
            return count

        return sum(waviness(n) for n in range(num1, num2 + 1))
```

---

## Complexity Analysis

Let `R = num2 − num1 + 1` (≤ 10⁵) and `D` = max digit count (≤ 6).

| | Complexity | Reason |
|---|---|---|
| **Time** | **O(R · D)** ≈ **O(R)** | Each number scanned once; `D` is a small constant |
| **Space** | **O(D)** = **O(1)** | One digit list at a time |

At `R ≤ 10⁵` and `D ≤ 6`, this is well under a million operations.

---

## Full Trace — Example 3: `4848`

Digits: `[4, 8, 4, 8]`, indices `0..3`. Interior indices: `1, 2`.

| i | `d[i-1]` | `d[i]` | `d[i+1]` | peak? | valley? |
|:-:|:-:|:-:|:-:|:-:|:-:|
| 1 | 4 | 8 | 4 | `8 > 4` and `8 > 4` ✓ | — |
| 2 | 8 | 4 | 8 | — | `4 < 8` and `4 < 8` ✓ |

Waviness = `2` ✓

---

## Full Trace — Example 1: `[120, 130]`

We sum waviness over all 11 numbers; only three are nonzero.

| n | digits | interior check | waviness |
|:-:|:-:|---|:-:|
| 120 | 1,2,0 | `2 > 1` and `2 > 0` → peak | 1 |
| 121 | 1,2,1 | `2 > 1` and `2 > 1` → peak | 1 |
| 122 | 1,2,2 | `2 > 1` but `2 = 2` (not strict) | 0 |
| … | … | (123–129 similar: middle digit not a strict extremum) | 0 |
| 130 | 1,3,0 | `3 > 1` and `3 > 0` → peak | 1 |

Total = `1 + 1 + 1 = 3` ✓

Note `122` contributes `0`: even though `2 > 1` on the left, the right neighbor ties (`2 = 2`), and strictness fails.

---

## Why Strict Inequalities Matter

The definition uses **strictly** greater / less. So:

- `121` → middle `2` is a peak (2 > 1 on both sides). ✓
- `122` → middle `2` is **not** a peak (2 = 2 on the right). ✗
- `100` → middle `0`: `0 < 1` left, but `0 = 0` right → **not** a valley. ✗

Plateaus and equal neighbors break both conditions, which is why `100` has waviness `0` despite the visual "dip."

---

## Looking Ahead — The "II" Version (Digit DP)

This problem is labeled **I** because the small bound (`10⁵`) invites brute force. A typical **"II"** variant raises the bound to ~`10¹⁵` or higher, where enumerating every number is impossible. That version needs **digit dynamic programming**:

- Build numbers digit-by-digit from most significant to least.
- Carry state: the previous two digits (to detect a peak/valley as each new digit is placed), a `tight` flag (whether we're still bounded by `N`'s prefix), and a `started` flag (to handle leading zeros / length).
- Accumulate the total waviness contributed across all completions.
- Answer for `[num1, num2]` = `f(num2) − f(num1 − 1)` where `f(N)` counts total waviness for `[0, N]`.

That's a substantially more involved solution — and unnecessary here. The brute force is the correct tool for the given constraints.

---

## Key Insights

| Insight | Explanation |
|---|---|
| **Small range ⇒ brute force** | ≤ 10⁵ numbers × ≤ 6 digits is trivial to scan directly. |
| **Only interior digits qualify** | First/last digits are excluded by definition; loop `1 .. len-2`. |
| **Strict inequalities** | Equal neighbors disqualify a peak/valley — plateaus count as nothing. |
| **Short numbers need no special case** | The empty interior loop yields `0` automatically. |
| **"II" would need digit DP** | The technique to remember for the high-bound variant. |

---

## Edge Cases

| Case | Behavior |
|---|---|
| `num1 = num2` (single number) | Waviness of just that number |
| Range with no 3+ digit numbers (`1..99`) | All contribute `0` → total `0` |
| `100` | Middle `0` ties the right neighbor → not strict → `0` |
| Repeated digits (`111`) | No strict extremum → `0` |
| Alternating digits (`12121`) | Multiple peaks/valleys → waviness `3` |

---

## Approach Tags

`Brute Force` · `Digit Scan` · `Peak/Valley Detection` · `Strict Comparison`

---

*Day 31 of the LeetCode Daily Challenge*
