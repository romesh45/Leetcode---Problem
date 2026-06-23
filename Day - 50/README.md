# Day 50 — LeetCode Challenge

## 3699. Number of ZigZag Arrays I

| Field | Details |
|---|---|
| **Difficulty** | Hard |
| **Topics** | Dynamic Programming · Prefix Sum · Array |
| **LeetCode Link** | [3699. Number of ZigZag Arrays I](https://leetcode.com/problems/number-of-zigzag-arrays-i/) |

---

## Problem Statement

You are given three integers `n`, `l`, and `r`.

A **ZigZag array** of length `n` is defined as follows:

- Each element lies in the range `[l, r]`.
- No two adjacent elements are equal.
- No three consecutive elements form a strictly increasing or strictly decreasing sequence.

Return the total number of valid ZigZag arrays modulo `10⁹ + 7`.

---

## Examples

### Example 1
```
Input:  n = 3, l = 4, r = 5
Output: 2
```
Valid arrays: `[4, 5, 4]` and `[5, 4, 5]`.

### Example 2
```
Input:  n = 3, l = 1, r = 3
Output: 10
```
Valid arrays: `[1,2,1]`, `[1,3,1]`, `[1,3,2]`, `[2,1,2]`, `[2,1,3]`, `[2,3,1]`, `[2,3,2]`, `[3,1,2]`, `[3,1,3]`, `[3,2,3]`.

---

## Constraints

- `3 <= n <= 2000`
- `1 <= l < r <= 2000`

---

## Intuition

### What "ZigZag" really means

The "no three consecutive strictly monotone" rule forces the sequence to **alternate direction** at every step. Specifically:

- An **UP** move (`arr[i-1] < arr[i]`) must be followed by a **DOWN** move (`arr[i] > arr[i+1]`).
- A **DOWN** move must be followed by an **UP** move.

Every interior position is either a **local peak** or a **local valley**. The array looks like: valley → peak → valley → peak → … (or the reverse).

**This is the key invariant: the direction of each step must be strictly opposite to the previous step.**

---

### DP formulation

Let `M = r − l + 1` (the number of distinct values).

Define (working with zero-indexed values `v ∈ [0, M-1]` representing `l + v`):

```
up[v]   = number of valid arrays ending at value (l + v),
          where the last move was UP   (previous element < current)

down[v] = number of valid arrays ending at value (l + v),
          where the last move was DOWN (previous element > current)
```

**Base case (after placing 2 elements):**

For `arr[1] = l + v`:
- `up[v]`   = number of valid `arr[0]` values with `arr[0] < arr[1]` = `v` choices.
- `down[v]` = number of valid `arr[0]` values with `arr[0] > arr[1]` = `M − 1 − v` choices.

**Transition (extending by one element):**

The new element at value `new_v` must:
- Move **UP** if the previous move was **DOWN** → `new_v > cur_v`
- Move **DOWN** if the previous move was **UP**  → `new_v < cur_v`

```
new_up[new_v]   = Σ down[cur_v]  for all cur_v < new_v
new_down[new_v] = Σ up[cur_v]    for all cur_v > new_v
```

Both are **range sums** over the value dimension.

---

### Prefix sums eliminate the inner loop

A naïve implementation sums over all `cur_v` for each `new_v` → O(M²) per step → O(n × M²) total. With `n, M ≤ 2000` that's 8 × 10⁹ — too slow.

Instead, precompute:

```
prefix_down[v] = Σ down[0 .. v-1]     (cumulative from the left)
suffix_up[v]   = Σ up[v .. M-1]       (cumulative from the right)
```

Then:
```
new_up[new_v]   = prefix_down[new_v]        O(1) lookup
new_down[new_v] = suffix_up[new_v + 1]      O(1) lookup
```

Each step is now `O(M)`, and we run `n − 2` steps → **O(n × M) total**.

---

## Algorithm

```
M = r - l + 1
up[v]   = v          for v in [0, M-1]   # base: 2-element arrays, last move UP
down[v] = M - 1 - v  for v in [0, M-1]   # base: 2-element arrays, last move DOWN

repeat (n - 2) times:
    prefix_down[0..M] = prefix sums of down[]
    suffix_up[0..M]   = suffix sums of up[]

    new_up[v]   = prefix_down[v]
    new_down[v] = suffix_up[v + 1]
    up, down = new_up, new_down

return (Σ up + Σ down) mod (10⁹ + 7)
```

---

## Solution

```python
from typing import List

MOD = 10**9 + 7


class Solution:
    def numberOfZigzagArrays(self, n: int, l: int, r: int) -> int:
        M = r - l + 1

        up   = [v       for v in range(M)]
        down = [M-1-v   for v in range(M)]

        for _ in range(n - 2):
            prefix_down = [0] * (M + 1)
            for v in range(M):
                prefix_down[v + 1] = (prefix_down[v] + down[v]) % MOD

            suffix_up = [0] * (M + 1)
            for v in range(M - 1, -1, -1):
                suffix_up[v] = (suffix_up[v + 1] + up[v]) % MOD

            up   = [prefix_down[v]   for v in range(M)]
            down = [suffix_up[v + 1] for v in range(M)]

        return (sum(up) + sum(down)) % MOD
```

---

## Complexity Analysis

Let `M = r − l + 1 ≤ 2000`.

| | Complexity | Reason |
|---|---|---|
| **Time** | **O(n × M)** | `n − 2` steps, each O(M) for prefix/suffix build and array update |
| **Space** | **O(M)** | Two arrays of size M plus prefix/suffix buffers |

---

## Full Trace — Example 1: `n = 3, l = 4, r = 5`

`M = 2`.  Values: `v=0 → 4`,  `v=1 → 5`.

**Base (2 elements):**

| v | value | up[v] | down[v] |
|:-:|:-:|:-:|:-:|
| 0 | 4 | 0 | 1 |
| 1 | 5 | 1 | 0 |

*`up[0]=0`: no value below 4 in range. `down[0]=1`: one value above 4 (which is 5). Etc.*

**Step 1 (extend to length 3):**

```
prefix_down = [0, 1, 1]   (prefix sums of [1, 0])
suffix_up   = [1, 1, 0]   (suffix sums of [0, 1])

new_up[0]   = prefix_down[0] = 0
new_up[1]   = prefix_down[1] = 1

new_down[0] = suffix_up[1]  = 1
new_down[1] = suffix_up[2]  = 0
```

**Answer:** `(0 + 1) + (1 + 0) = 2` ✓

---

## Full Trace — Example 2: `n = 3, l = 1, r = 3`

`M = 3`. Values: `v=0→1, v=1→2, v=2→3`.

**Base (2 elements):**

| v | value | up[v] | down[v] |
|:-:|:-:|:-:|:-:|
| 0 | 1 | 0 | 2 |
| 1 | 2 | 1 | 1 |
| 2 | 3 | 2 | 0 |

**Step 1 (extend to length 3):**

```
prefix_down = [0, 2, 3, 3]
suffix_up   = [3, 3, 2, 0]

new_up   = [0, 2, 3]
new_down = [3, 2, 0]
```

**Answer:** `(0+2+3) + (3+2+0) = 5 + 5 = 10` ✓

---

## Why the Base Case Is `up[v] = v` and `down[v] = M-1-v`

For a 2-element array ending at `l + v`:
- **UP move** means `arr[0] < arr[1] = l + v`. Valid choices for `arr[0]`: `{l, l+1, …, l+v-1}` → exactly `v` values.
- **DOWN move** means `arr[0] > arr[1] = l + v`. Valid choices for `arr[0]`: `{l+v+1, …, r}` → exactly `M − 1 − v` values.

No modular arithmetic needed here since both values are at most `M − 1 ≤ 1999`.

---

## Edge Cases

| Case | Behaviour |
|---|---|
| `l == r` | `M = 1`: `up = [0]`, `down = [0]` from base → answer is 0 (not in constraints since `l < r`, but handled) |
| `r = l + 1` (binary range) | Only alternating `[l,r,l,r,…]`-style arrays valid; e.g. `n=3` → 2 |
| Large `n`, large `M` | O(n × M) = O(2000 × 2000) = 4 × 10⁶ — fast |
| `n = 3` | One transition step; answers match brute force exactly |

---

## Alternative — Naïve O(n × M²)

```python
# For each new_v, sum over all valid cur_v directly — TLE for large inputs
for new_v in range(M):
    new_up[new_v]   = sum(down[cur_v] for cur_v in range(new_v))
    new_down[new_v] = sum(up[cur_v]   for cur_v in range(new_v + 1, M))
```

Correct but O(M²) per step. The prefix/suffix trick is the critical optimisation.

---

## Key Insights

| Insight | Explanation |
|---|---|
| **Alternating direction** | "No three consecutive monotone" ≡ every step reverses direction |
| **DP on (value, last-direction)** | Two arrays `up[]` and `down[]` over value dimension suffice |
| **Prefix/suffix sums** | Turn O(M²) range queries into O(M) per step |
| **Base in O(M)** | `up[v] = v`, `down[v] = M−1−v` — no loops needed |
| **O(n × M) overall** | 4 × 10⁶ operations max; comfortably within limits |

---

## Approach Tags

`Dynamic Programming` · `Prefix Sum` · `Suffix Sum` · `Alternating Sequence` · `Counting`

---

*Day 50 of the LeetCode Daily Challenge*
