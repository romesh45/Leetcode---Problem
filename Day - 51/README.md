# Day 50 — LeetCode Challenge

## 3700. Number of ZigZag Arrays II

| Field | Details |
|---|---|
| **Difficulty** | Hard |
| **Topics** | Dynamic Programming · Matrix Exponentiation · Linear Algebra |
| **LeetCode Link** | [3700. Number of ZigZag Arrays II](https://leetcode.com/problems/number-of-zigzag-arrays-ii/) |

---

## Problem Statement

You are given three integers `n`, `l`, and `r`.

A **ZigZag array** of length `n` is defined as:

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

### Example 2
```
Input:  n = 3, l = 1, r = 3
Output: 10
```

---

## Constraints

- `3 <= n <= 10⁹`
- `1 <= l < r <= 75`

---

## The Critical Difference from Part I

| | Part I | Part II |
|---|---|---|
| `n` | ≤ 2000 | ≤ **10⁹** |
| `M = r − l + 1` | ≤ 2000 | ≤ **75** |
| Strategy | O(n × M) linear DP | **Matrix exponentiation** |

Part I has large `M` and small `n` → sweep over positions. Part II flips both constraints. Linear DP iterating `n − 2 ≈ 10⁹` steps is completely infeasible. But `M ≤ 75` means the state vector is tiny (size 150) — perfect for matrix exponentiation.

---

## Intuition

### Recap: the zigzag DP

The zigzag condition forces **direction alternation**: after an UP step the next must be DOWN, and vice versa. Define (with values zero-indexed as `v ∈ [0, M-1]`):

```
up[v]   = # arrays ending at (l+v) with last move UP
down[v] = # arrays ending at (l+v) with last move DOWN
```

**Transition:**
```
new_up[v]   = Σ down[u]  for u < v      ← moved up from a valley
new_down[v] = Σ up[u]    for u > v      ← moved down from a peak
```

This is a linear map on the state vector `s = [up[0], …, up[M-1], down[0], …, down[M-1]]`.

### Representing the transition as a matrix

Concatenate `up` and `down` into a single vector of length `2M`. Then:

```
s[v]     = up[v]      (indices 0 .. M-1)
s[M + v] = down[v]    (indices M .. 2M-1)
```

The transition is `s' = T · s` where `T` is a `(2M) × (2M)` matrix of 0s and 1s:

```
T[v][M + u]  = 1   for u < v     (new_up[v]   reads down[u])
T[M+v][u]    = 1   for u > v     (new_down[v] reads up[u])
all other entries = 0
```

Applying this transition `n − 2` times:

```
s_final = T^(n-2) · s_init
```

**Matrix exponentiation** computes `T^(n-2)` in `O(log n)` matrix multiplications, each costing `O((2M)³)`.

---

## Overflow-Safe Matrix Multiplication

With `M ≤ 75`, matrix size is `150 × 150`. Each element fits in `[0, MOD − 1] ≈ 10⁹`. A dot product term is up to `(10⁹)² = 10¹⁸`, and summing 150 such terms hits `1.5 × 10²⁰` — well beyond `int64` (max `9.2 × 10¹⁸`).

**Fix:** chunk the `k`-axis into groups of 8. Each chunk accumulates at most `8 × 10¹⁸ < 9.2 × 10¹⁸`, staying inside `int64`. Take modulo after each chunk.

```python
CHUNK = 8
C = zeros(size, size)
for k0 in range(0, size, CHUNK):
    C = (C + A[:, k0:k0+CHUNK] @ B[k0:k0+CHUNK, :]) % MOD
```

---

## Algorithm

```
M    = r - l + 1
size = 2 * M

Build T (2M × 2M):
    T[v][M+u]  = 1  for u < v        # up reads from down below
    T[M+v][u]  = 1  for u > v        # down reads from up above

init[v]     = v          for v in [0, M-1]    # up[v]
init[M + v] = M - 1 - v  for v in [0, M-1]    # down[v]

Tn = matrix_power(T, n - 2)          # log(n) multiplications
s  = Tn @ init  (mod MOD)

return sum(s) mod MOD
```

---

## Solution

```python
import numpy as np
MOD = 10**9 + 7

class Solution:
    def zigZagArrays(self, n: int, l: int, r: int) -> int:
        M    = r - l + 1
        size = 2 * M

        T = np.zeros((size, size), dtype=np.int64)
        for v in range(M):
            for u in range(v):
                T[v][M + u] = 1
        for v in range(M):
            for u in range(v + 1, M):
                T[M + v][u] = 1

        init = np.zeros(size, dtype=np.int64)
        for v in range(M):
            init[v]     = v
            init[M + v] = M - 1 - v

        def mat_mul(A, B):
            CHUNK = 8
            C = np.zeros((size, size), dtype=np.int64)
            for k0 in range(0, size, CHUNK):
                C = (C + A[:, k0:k0+CHUNK] @ B[k0:k0+CHUNK, :]) % MOD
            return C

        result = np.eye(size, dtype=np.int64)
        base, exp = T.copy(), n - 2
        while exp:
            if exp & 1:
                result = mat_mul(result, base)
            base = mat_mul(base, base)
            exp >>= 1

        state = np.zeros(size, dtype=np.int64)
        for k0 in range(0, size, 8):
            state = (state + result[:, k0:k0+8] @ init[k0:k0+8]) % MOD

        return int(state.sum() % MOD)
```

---

## Complexity Analysis

Let `M = r − l + 1 ≤ 75`, so `size = 2M ≤ 150`.

| | Complexity | Reason |
|---|---|---|
| **Time** | **O(M³ log n)** | `log₂(10⁹) ≈ 30` matrix mults, each O((2M)³) ≈ 3.4M ops → ~100M total |
| **Space** | **O(M²)** | Store two 150×150 matrices |

Concrete: ~0.4s for worst case `n = 10⁹, M = 75` using numpy.

Compare to Part I's `O(n × M)` which would be `10⁹ × 75 = 7.5 × 10¹⁰` — completely infeasible.

---

## Full Trace — Example 1: `n = 3, l = 4, r = 5`

`M = 2`, `size = 4`. State: `[up[0], up[1], down[0], down[1]]`.

**Transition matrix T:**
```
        up[0] up[1] dn[0] dn[1]
up[0] [  0     0     0     0  ]   # new_up[0]: no u < 0
up[1] [  0     0     1     0  ]   # new_up[1]: reads down[0]
dn[0] [  0     1     0     0  ]   # new_down[0]: reads up[1]
dn[1] [  0     0     0     0  ]   # new_down[1]: no u > 1
```

**Initial state** (2-element arrays):
```
init = [up[0]=0, up[1]=1, down[0]=1, down[1]=0]
```

**Apply T¹** (n − 2 = 1):
```
new[up[0]]   = 0
new[up[1]]   = 1 * down[0] = 1
new[down[0]] = 1 * up[1]   = 1
new[down[1]] = 0
```

**Answer:** `0 + 1 + 1 + 0 = 2` ✓

---

## Full Trace — Example 2: `n = 3, l = 1, r = 3`

`M = 3`, `size = 6`. Initial: `[0, 1, 2, 2, 1, 0]`.

After one application of T:
```
new_up[0]   = 0                          = 0
new_up[1]   = down[0]                    = 2
new_up[2]   = down[0] + down[1]          = 3
new_down[0] = up[1] + up[2]             = 3
new_down[1] = up[2]                      = 2
new_down[2] = 0                          = 0
```

**Answer:** `0 + 2 + 3 + 3 + 2 + 0 = 10` ✓

---

## Why Matrix Exponentiation Works

Any recurrence of the form `s_{i+1} = T · s_i` (linear, constant coefficients) satisfies:

```
s_n = T^(n-2) · s_2
```

Matrix exponentiation evaluates `T^k` in `O(log k)` multiplications using repeated squaring:

```
T^13 = T^8 · T^4 · T^1     (binary: 13 = 1101)
```

This is the standard technique whenever:
- The recurrence is **linear** (can be written as matrix-vector multiply)
- The state size is **small** (matrix mult must be fast)
- `n` is **large** (repeated squaring needed)

---

## Key Insights

| Insight | Explanation |
|---|---|
| **Same DP as Part I** | Zigzag = alternating UP/DOWN; same transitions apply |
| **Transition is linear** | `new_up[v]` and `new_down[v]` are sums of previous state entries → matrix form |
| **Small M enables matrix exp** | `M ≤ 75` → 150×150 matrix, ~3.4M ops per multiply |
| **Chunked int64 multiply** | Avoids overflow without arbitrary precision; 8 terms × 10¹⁸ < int64 max |
| **O(M³ log n)** | Completely independent of `n` beyond the `log n` factor |

---

## Comparison: Part I vs Part II

| Aspect | Part I | Part II |
|---|---|---|
| n range | ≤ 2,000 | ≤ 10⁹ |
| M range | ≤ 2,000 | ≤ 75 |
| Algorithm | Linear DP + prefix sums | Matrix exponentiation |
| Time | O(n × M) | O(M³ log n) |
| Key trick | Prefix/suffix sums | Repeated squaring |

---

## Approach Tags

`Matrix Exponentiation` · `Dynamic Programming` · `Linear Recurrence` · `Repeated Squaring` · `Modular Arithmetic`

---

*Day 50 of the LeetCode Daily Challenge*
