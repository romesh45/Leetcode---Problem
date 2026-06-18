# Day 44 — LeetCode Challenge

## 3614. Process String with Special Operations II

| Field | Details |
|---|---|
| **Difficulty** | Hard |
| **Topics** | String · Simulation · Reverse Mapping · Index Tracking |
| **LeetCode Link** | [3614. Process String with Special Operations II](https://leetcode.com/problems/process-string-with-special-operations-ii/) |

---

## Problem Statement

Same operations as [version I (Day 43)](https://leetcode.com/problems/process-string-with-special-operations-i/) — process `s` left to right over a string `result`:

- **lowercase letter** → append.
- **`*`** → remove the last character (if any).
- **`#`** → duplicate `result` (append it to itself).
- **`%`** → reverse `result`.

But now you're given an integer `k`: return the **`k`-th character** of the final `result`. If `k` is out of bounds, return `'.'`.

---

## Examples

### Example 1

```
Input:  s = "a#b%*", k = 1
Output: "a"
```

Final `result = "ba"`; index `1` is `'a'`.

### Example 2

```
Input:  s = "cd%#*#", k = 3
Output: "d"
```

Final `result = "dcddcd"`; index `3` is `'d'`.

### Example 3

```
Input:  s = "z*#", k = 0
Output: "."
```

Final `result = ""`; index `0` is out of bounds.

---

## Constraints

- `1 <= s.length <= 10⁵`
- `0 <= k <= 10¹⁵`
- The final length of `result` will not exceed `10¹⁵`.

---

## Intuition

### Why Day 43's simulation explodes

In version I, `|s| ≤ 20` kept the buffer tiny. Here `|s| ≤ 10⁵` and `#` **doubles** the string — the final length can reach `10¹⁵`. Building it would need a petabyte of memory. **We can't materialize `result`.**

But we don't have to: we only need **one character** — the one at index `k`.

### Forward to measure, backward to resolve

The plan is two linear passes:

**Pass 1 — Forward (lengths).** Walk `s` and track only the *length* of `result` after each op (append `+1`, `*` is `−1`, `#` is `×2`, `%` unchanged). Record `before[i]` = the length **just before** operation `i`. The final length tells us instantly whether `k` is out of bounds.

**Pass 2 — Backward (index).** Start with `k` as a position in the *final* string and **undo each operation in reverse**, transforming `k` into the equivalent position in the *earlier* string. Each character ultimately came from exactly one append — when `k` lands on that append, we have our answer.

### How each operation transforms `k` (in reverse)

Let `L = before[i]` = length before op `i`.

| Op | Forward effect | Reverse mapping of index `k` |
|:-:|---|---|
| letter | `after = L + 1`, new char at index `L` | if `k == L` → **answer is this letter**; else `k` unchanged |
| `*` | `after = L − 1` (a prefix of pre-string) | `k` unchanged |
| `#` | `after = L + L` (pre + pre) | if `k ≥ L`: `k −= L` (it's in the second copy) |
| `%` | `after = reverse(pre)` | `k = L − 1 − k` |

### Why it always terminates on a letter

Every character in the final string traces back through duplications, reversals, and trailing-deletions to a **single original append**. The backward walk follows that trace; for any in-bounds `k` it eventually hits the letter that produced it. (Out-of-bounds `k` is caught upfront by the length check.)

---

## Algorithm

```
forward: before[i] = length before op i; track final length
if k >= final length: return '.'

backward for i = n-1 .. 0, L = before[i]:
    letter : if k == L: return s[i]      (else k unchanged)
    '*'    : k unchanged
    '#'    : if k >= L: k -= L
    '%'    : k = L - 1 - k
```

---

## Solution

```python
class Solution:
    def processStr(self, s: str, k: int) -> str:
        CAP = 10**15 + 1  # defensive cap; valid lengths never exceed 10^15

        before = [0] * len(s)
        length = 0
        for i, ch in enumerate(s):
            before[i] = length
            if ch == '*':
                length = max(0, length - 1)
            elif ch == '#':
                length = min(length * 2, CAP)
            elif ch == '%':
                pass
            else:
                length += 1

        if k >= length:
            return "."

        for i in range(len(s) - 1, -1, -1):
            L = before[i]
            ch = s[i]
            if ch == '*':
                pass
            elif ch == '#':
                if k >= L:
                    k -= L
            elif ch == '%':
                k = L - 1 - k
            else:
                if k == L:
                    return ch

        return "."
```

> The `CAP` keeps integers bounded against pathological `#` chains the problem says won't occur; since real lengths stay `≤ 10¹⁵ < CAP` and `k ≤ 10¹⁵`, it never affects a valid answer.

---

## Complexity Analysis

| | Complexity | Reason |
|---|---|---|
| **Time** | **O(n)** | One forward pass + one backward pass over `s` |
| **Space** | **O(n)** | The `before` length array |

Measured: `10⁵` ops with many `#` and `k ≈ 10¹⁵` resolves in **~13 ms** — never building the string.

---

## Full Trace — Example 2: `s = "cd%#*#", k = 3`

**Forward — `before[]` (length before each op):**

| i | char | before[i] | length after |
|:-:|:-:|:-:|:-:|
| 0 | c | 0 | 1 |
| 1 | d | 1 | 2 |
| 2 | % | 2 | 2 |
| 3 | # | 2 | 4 |
| 4 | * | 4 | 3 |
| 5 | # | 3 | 6 |

Final length `6`; `k = 3 < 6` → in bounds.

**Backward — transform `k`:**

| i | char | L = before[i] | rule | new k |
|:-:|:-:|:-:|---|:-:|
| 5 | # | 3 | `k ≥ 3` → `k −= 3` | `0` |
| 4 | * | 4 | unchanged | `0` |
| 3 | # | 2 | `k < 2` → unchanged | `0` |
| 2 | % | 2 | `k = 2−1−0` | `1` |
| 1 | d | 1 | `k == L` (1) → **return 'd'** | — |

**Answer: `"d"`** ✓

---

## Full Trace — Example 1: `s = "a#b%*", k = 1`

Forward `before = [0, 1, 2, 3, 3]`, final length `2`, `k = 1` in bounds.

| i | char | L | rule | new k |
|:-:|:-:|:-:|---|:-:|
| 4 | * | 3 | unchanged | 1 |
| 3 | % | 3 | `3−1−1` | 1 |
| 2 | b | 2 | `k ≠ 2` → unchanged | 1 |
| 1 | # | 1 | `k ≥ 1` → `k −= 1` | 0 |
| 0 | a | 0 | `k == 0` → **return 'a'** | — |

**Answer: `"a"`** ✓

---

## Why Reverse Mapping Beats Forward Building

| | Forward build (Day 43 style) | Reverse mapping (this) |
|---|---|---|
| Memory | Up to `10¹⁵` chars — impossible | `O(n)` |
| Time | Up to `10¹⁵` ops | `O(n)` |
| Idea | Construct the whole string | Trace one index back to its source |

The insight generalizes: when an output is astronomically large but **a single position is queried**, track *sizes* forward and *walk the position backward* through the operations that built it.

---

## Comparison with Day 43 (LC 3612, "I")

| Aspect | Day 43 ("I", Medium) | Day 44 ("II", Hard) |
|---|---|---|
| `|s|` | ≤ 20 | ≤ 10⁵ |
| Final length | tiny | up to 10¹⁵ |
| Output | whole string | one character at index `k` |
| Method | build the buffer | length tracking + reverse index mapping |
| Complexity | O(final length) | O(n) |

Exactly the escalation flagged in Day 43's "Looking Ahead" — the doubling makes the string unbuildable, forcing a position-tracking approach.

---

## Validation

`solution.py` cross-checks against the Day-43 brute-force simulation across **20,000 random strings × 16 values of `k` each** (including out-of-bounds), and times the adversarial large case:

```
randomized cross-check passed ✓
n=1e5 with many '#', k≈1e15 → 'a'  (0.013s)
```

---

## Key Insights

| Insight | Explanation |
|---|---|
| **Don't build — query** | The string can be `10¹⁵` long; we only need one character. |
| **Track lengths forward** | Cheap O(n) record of the size before every op. |
| **Walk the index backward** | Undo each op's effect on position `k` until it hits the source letter. |
| **`#` → subtract `L` if in the second half** | Duplication is `pre + pre`; the copy maps back by the pre-length. |
| **`%` → `L − 1 − k`** | Reversal mirrors the index. |

---

## Edge Cases

| Case | Behavior |
|---|---|
| `k ≥ final length` | Out of bounds → `'.'` |
| Empty final string | Any `k` → `'.'` |
| `k` in a duplicated copy | Mapped back via `k −= L` at the `#` |
| Many reversals | Each flips the index `L−1−k` |
| Max `|s|` with deep doubling | O(n), no materialization → fast |

---

## Approach Tags

`Reverse Index Mapping` · `Length Tracking` · `Simulation Without Materialization` · `Two-Pass`

---

*Day 44 of the LeetCode Daily Challenge*
