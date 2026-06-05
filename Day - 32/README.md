# Day 32 — LeetCode Challenge

## 3753. Total Waviness of Numbers in Range II

| Field | Details |
|---|---|
| **Difficulty** | Hard |
| **Topics** | Digit DP · Dynamic Programming · Math · Memoization |
| **LeetCode Link** | [3753. Total Waviness of Numbers in Range II](https://leetcode.com/problems/total-waviness-of-numbers-in-range-ii/) |

---

## Problem Statement

Given an inclusive range `[num1, num2]`, return the **total waviness** of all numbers in it.

The **waviness** of a number = count of its **peaks** and **valleys**:

- **Peak:** a digit strictly greater than *both* immediate neighbors.
- **Valley:** a digit strictly less than *both* immediate neighbors.
- First and last digits never qualify.
- Numbers with fewer than 3 digits have waviness `0`.

---

## Examples

### Example 1
```
Input:  num1 = 120, num2 = 130
Output: 3
```
`120`, `121`, `130` each have one peak → total `3`.

### Example 2
```
Input:  num1 = 198, num2 = 202
Output: 3
```
`198` (peak 9), `201` (valley 0), `202` (valley 0) → total `3`.

### Example 3
```
Input:  num1 = 4848, num2 = 4848
Output: 2
```
`4848`: peak `8`, valley `4` → waviness `2`.

---

## Constraints

- `1 <= num1 <= num2 <= 10¹⁵`  ← **the difference from "I"**

---

## Intuition

### Brute force is dead

[Day 31 (LC 3751)](https://leetcode.com/problems/total-waviness-of-numbers-in-range-i/) capped at `10⁵` and we just enumerated. Here `num2 ≤ 10¹⁵` — up to a **quadrillion** numbers. We can't visit them. We need to count waviness contributions *combinatorially*.

### Range → prefix difference

Define:

```
f(N) = total waviness summed over all numbers in [0, N]
```

Then by inclusion:

```
answer = f(num2) − f(num1 − 1)
```

This reduces "range" to two "prefix up to N" computations — the standard digit-DP framing.

### Counting contributions, not numbers

A peak/valley lives at one **interior position** of one number. Instead of asking "what's the waviness of each number?", we ask: **as we build numbers digit by digit, how many times does a peak/valley get formed across all numbers ≤ N?**

Every time we place a digit that *completes a triple* whose middle is a strict extremum, we add `+1` to **every** number that flows through that partial prefix. Digit DP tracks exactly that.

### What state do we need?

To know whether the digit we just finished (`p2`) is a peak/valley, we need the triple `(p1, p2, cur)`:
- `p1` — digit two positions back
- `p2` — digit one position back (the candidate middle)
- `cur` — the digit being placed now

Plus the usual digit-DP bookkeeping:
- `tight` — are we still bounded by `N`'s prefix?
- `started` — has the number begun? (leading zeros are not real digits)

### The triple sweeps every interior digit exactly once

For a number `a b c d`:

```
place a → state (·, a)
place b → state (a, b)        no triple yet (only one prior digit)
place c → check b in (a,b,c)  ← first interior digit
place d → check c in (b,c,d)  ← second interior digit
```

Each interior digit is the "middle" exactly once. No double counting, no misses.

---

## Algorithm

```
f(N):
    digits = decimal digits of N
    dp(pos, p1, p2, tight, started) → (count, waviness_sum):
        if pos == len: return (1, 0)
        limit = digits[pos] if tight else 9
        for cur in 0..limit:
            ntight = tight and cur == limit
            if not started:
                if cur == 0: recurse (…, none, none, …, started=False)
                else:        recurse (…, none, cur,  …, started=True)
            else:
                add = 1 if (p1,p2 exist and p2 is strict peak/valley vs cur) else 0
                (c, w) = recurse(…, p2, cur, …, started=True)
                count += c
                waviness += w + add * c     ← distribute +1 over the branch
        return (count, waviness)

    return dp(0, none, none, tight=True, started=False).waviness

answer = f(num2) − f(num1 − 1)
```

---

## Solution

```python
class Solution:
    def totalWaviness(self, num1: int, num2: int) -> int:
        def f(N: int) -> int:
            if N < 0:
                return 0
            digits = list(map(int, str(N)))
            n = len(digits)

            from functools import lru_cache

            @lru_cache(maxsize=None)
            def dp(pos, p1, p2, tight, started):
                if pos == n:
                    return (1, 0)
                limit = digits[pos] if tight else 9
                cnt = wav = 0
                for cur in range(0, limit + 1):
                    ntight = tight and (cur == limit)
                    if not started:
                        if cur == 0:
                            c, w = dp(pos + 1, 10, 10, ntight, False)
                        else:
                            c, w = dp(pos + 1, 10, cur, ntight, True)
                        cnt += c; wav += w
                    else:
                        add = 0
                        if p1 != 10 and p2 != 10:
                            if p2 > p1 and p2 > cur:
                                add = 1
                            elif p2 < p1 and p2 < cur:
                                add = 1
                        c, w = dp(pos + 1, p2, cur, ntight, True)
                        cnt += c; wav += w + add * c
                return (cnt, wav)

            result = dp(0, 10, 10, True, False)[1]
            dp.cache_clear()
            return result

        return f(num2) - f(num1 - 1)
```

(`10` is the sentinel for "no digit yet" — outside the valid `0..9` range.)

---

## Complexity Analysis

Let `D = number of digits ≤ 16`.

| | Complexity | Reason |
|---|---|---|
| **Time** | **O(D · 11 · 11 · 2 · 2 · 10)** ≈ **O(D)** | State space × 10 transitions; ~`4·10⁴` states total |
| **Space** | **O(D · 11 · 11 · 2 · 2)** | Memo table |

Two `f` calls → still effectively constant for `D ≤ 16`. The `10¹⁵` input returns instantly.

---

## The Distribution Trick: `wav += w + add * c`

This single line is the heart of digit DP for **summing** (not just counting):

- `c` = how many complete numbers live in the subtree below this transition.
- `w` = total waviness those numbers accumulate **from `pos+1` onward**.
- `add` = whether *this* transition forms a peak/valley (0 or 1).

If this step contributes a peak/valley, it adds `+1` to **each** of the `c` numbers below — hence `add * c`. We fold that into the running waviness alongside the deeper contributions `w`. Returning `(count, sum)` together is what lets a peak discovered high in the tree be correctly multiplied across all descendants.

---

## Full Trace (Conceptual) — `f(130)`

We don't expand all branches (there are too many), but the structure for the contributing numbers:

- `120`: build `1 → 2 → 0`. At the last step, triple `(1, 2, 0)` → `2 > 1` and `2 > 0` → peak → `+1`.
- `121`: triple `(1, 2, 1)` → peak → `+1`.
- `130`: triple `(1, 3, 0)` → peak → `+1`.
- Numbers like `122`..`129`: middle `2` vs right neighbor ≥ 2 → not a strict peak → `+0`.

`f(130)` sums these (and all smaller numbers' contributions). The answer `f(130) − f(119) = 3` matches Example 1. ✓

---

## Validation

The `solution.py` includes a **randomized cross-check**: the digit-DP solution is compared against the Day-31 brute force on 300 random ranges within `[1, ~10⁴]`. It also runs `totalWaviness(1, 10**15)` to confirm the large case completes instantly.

```
randomized cross-check passed ✓
```

This guards against the classic digit-DP pitfalls: leading-zero handling, the `tight` boundary, and the off-by-one in which digit becomes the "middle."

---

## Comparison with Day 31 (LC 3751, "I")

| Aspect | Day 31 ("I", Medium) | Day 32 ("II", Hard) |
|---|---|---|
| Bound | `num2 ≤ 10⁵` | `num2 ≤ 10¹⁵` |
| Method | Brute force, scan every number | Digit DP + prefix difference |
| Per-number cost | O(digits) | Amortized O(1) via memoized states |
| Core trick | Direct peak/valley scan | Carry `(p1, p2)`, distribute `+1` over branch |
| Range handling | Loop `num1..num2` | `f(num2) − f(num1 − 1)` |

Same definition of waviness — the only change is the **bound**, which forces us from enumeration to combinatorial counting.

---

## Key Insights

| Insight | Explanation |
|---|---|
| **`f(num2) − f(num1−1)`** | Standard digit-DP range decomposition. |
| **Carry the previous two digits** | A peak/valley needs a full triple; `(p1, p2, cur)` is completed as `cur` is placed. |
| **Return (count, sum) together** | Lets a single peak high in the tree multiply across all `c` descendants. |
| **`add * c` distributes the contribution** | The crux of summing a per-number quantity via digit DP. |
| **`started` flag handles leading zeros** | Leading zeros aren't real digits and must not form spurious triples. |

---

## Edge Cases

| Case | Behavior |
|---|---|
| `num1 = num2` | `f(N) − f(N−1)` isolates one number's waviness |
| Range below 100 | No 3-digit numbers → all contribute `0` |
| Maximum `10¹⁵` | 16-digit DP, completes instantly |
| Numbers with plateaus (`122`, `100`) | Strict checks exclude them → `+0` |
| `num1 = 1` | `f(num1 − 1) = f(0) = 0` |

---

## Approach Tags

`Digit DP` · `Prefix Difference` · `Sum-Over-Range via DP` · `Memoization` · `Tight/Started State`

---

*Day 32 of the LeetCode Daily Challenge*
