# Day 47 — LeetCode Challenge

## 1840. Maximum Building Height

| Field | Details |
|---|---|
| **Difficulty** | Hard |
| **Topics** | Array · Math · Constraint Propagation · Sorting |
| **LeetCode Link** | [1840. Maximum Building Height](https://leetcode.com/problems/maximum-building-height/) |

---

## Problem Statement

Build `n` buildings in a line (labeled `1..n`) with:

- Each height a **non-negative integer**.
- Building `1` has height **0**.
- Adjacent buildings differ in height by **at most 1**.
- Some buildings have a **max-height cap** via `restrictions[i] = [idᵢ, maxHeightᵢ]`.

Each building appears at most once in `restrictions`, and building `1` is never in it. Return the **maximum possible height** of the tallest building.

---

## Examples

### Example 1
```
Input:  n = 5, restrictions = [[2,1],[4,1]]
Output: 2
```
Heights `[0,1,2,1,2]` → tallest `2`.

### Example 2
```
Input:  n = 6, restrictions = []
Output: 5
```
Heights `[0,1,2,3,4,5]` → tallest `5`.

### Example 3
```
Input:  n = 10, restrictions = [[5,3],[2,5],[7,4],[10,3]]
Output: 5
```
Heights `[0,1,2,3,3,4,4,5,4,3]` → tallest `5`.

---

## Constraints

- `2 <= n <= 10⁹`  ← **can't touch every building**
- `0 <= restrictions.length <= min(n − 1, 10⁵)`
- `2 <= idᵢ <= n`, ids unique, `0 <= maxHeightᵢ <= 10⁹`

---

## Intuition

### `n` up to 10⁹ ⇒ work with anchors, not buildings

We can't iterate over a billion buildings. But only the **restrictions matter** as turning points — everything between two restrictions is determined by them. So we work with `O(m)` **anchor points**:

- Every restriction `[id, cap]`.
- Building `1` fixed at height `0` → anchor `[1, 0]`.
- Building `n` (if unrestricted) → anchor `[n, n−1]` (its natural ceiling: start at 0, gain +1 per step over `n−1` steps).

### A cap isn't the real max — neighbours tighten it

A restriction says "≤ cap", but a building also can't exceed what its neighbours allow: from height `h` at position `p`, a building `d` steps away is at most `h + d`. So we **propagate** the `≤ 1` rule between anchors:

- **Forward pass** (left→right): `h[i] = min(h[i], h[i−1] + dist)`.
- **Backward pass** (right→left): `h[i] = min(h[i], h[i+1] + dist)`.

After both, every anchor holds its **true achievable maximum**.

### The tent between two anchors

Between adjacent anchors `(lid, lh)` and `(rid, rh)`, heights rise at most `+1` per step from each side:

```
        peak
        /\
       /  \
   lh /    \ rh
     •      •
   lid      rid
```

A building at position `pos` satisfies `height ≤ min(lh + (pos − lid), rh + (rid − pos))`. The two rising lines cross at the peak:

```
peak = ⌊(lh + rh + (rid − lid)) / 2⌋
```

The answer is the maximum peak over all adjacent gaps. Propagation guarantees `|lh − rh| ≤ rid − lid`, so each peak is `≥ max(lh, rh)` — the endpoints are automatically considered.

---

## Deriving the Peak Formula

Maximize `f(pos) = min(lh + (pos − lid), rh + (rid − pos))` over integer `pos ∈ [lid, rid]`.

The first term rises with `pos`, the second falls. The max is where they're equal:

```
lh + (pos − lid) = rh + (rid − pos)
2·pos = rh − lh + rid + lid
```

Substituting back, the crossing height is:

```
lh + (pos − lid) = (lh + rh + (rid − lid)) / 2
```

Heights are integers, so floor it: **`⌊(lh + rh + (rid − lid)) / 2⌋`**. ∎

---

## Algorithm

```
anchors = restrictions + [1,0] + ([n, n-1] if n unrestricted)
sort anchors by id

forward:  h[i] = min(h[i], h[i-1] + (id[i] - id[i-1]))
backward: h[i] = min(h[i], h[i+1] + (id[i+1] - id[i]))

answer = max over adjacent pairs of ⌊(lh + rh + (rid - lid)) / 2⌋
```

---

## Solution

```python
from typing import List


class Solution:
    def maxBuilding(self, n: int, restrictions: List[List[int]]) -> int:
        r = [list(x) for x in restrictions]
        r.append([1, 0])
        if all(x[0] != n for x in r):
            r.append([n, n - 1])
        r.sort()
        m = len(r)

        for i in range(1, m):
            r[i][1] = min(r[i][1], r[i - 1][1] + (r[i][0] - r[i - 1][0]))
        for i in range(m - 2, -1, -1):
            r[i][1] = min(r[i][1], r[i + 1][1] + (r[i + 1][0] - r[i][0]))

        ans = 0
        for i in range(1, m):
            lid, lh = r[i - 1]
            rid, rh = r[i]
            ans = max(ans, (lh + rh + (rid - lid)) // 2)
        return ans
```

---

## Complexity Analysis

Let `m = restrictions.length` (≤ 10⁵).

| | Complexity | Reason |
|---|---|---|
| **Time** | **O(m log m)** | Sorting the anchors; the passes are O(m) |
| **Space** | **O(m)** | The anchor list |

**Independent of `n`** — `n = 10⁹` runs in microseconds.

---

## Full Trace — Example 1: `n = 5, restrictions = [[2,1],[4,1]]`

**Anchors** (after adding `[1,0]` and `[5,4]`, sorted): `[1,0], [2,1], [4,1], [5,4]`.

**Forward:**

| i | anchor | `min(cap, left + dist)` | result |
|:-:|:-:|---|:-:|
| 1 | [2,1] | `min(1, 0+1)` | 1 |
| 2 | [4,1] | `min(1, 1+2)` | 1 |
| 3 | [5,4] | `min(4, 1+1)` | **2** |

**Backward:**

| i | anchor | `min(cur, right + dist)` | result |
|:-:|:-:|---|:-:|
| 2 | [4,1] | `min(1, 2+1)` | 1 |
| 1 | [2,1] | `min(1, 1+2)` | 1 |
| 0 | [1,0] | `min(0, 1+1)` | 0 |

Anchors now: `[1,0], [2,1], [4,1], [5,2]`.

**Peaks:**

| gap | `(lh + rh + dist) // 2` | peak |
|:-:|---|:-:|
| (1,0)–(2,1) | `(0+1+1)//2` | 1 |
| (2,1)–(4,1) | `(1+1+2)//2` | 2 |
| (4,1)–(5,2) | `(1+2+1)//2` | 2 |

**Answer: 2** ✓

---

## Full Trace — Example 3: `n = 10, restrictions = [[5,3],[2,5],[7,4],[10,3]]`

Anchors (with `[1,0]`, sorted): `[1,0],[2,5],[5,3],[7,4],[10,3]`.

After forward+backward propagation: `[1,0],[2,1],[5,3],[7,4],[10,3]`.

Peaks: `(1,0)-(2,1)→1`, `(2,1)-(5,3)→3`, `(5,3)-(7,4)→4`, `(7,4)-(10,3)→5`.

**Answer: 5** ✓ — matches the heights `[0,1,2,3,3,4,4,5,4,3]` (peak `5` at building 8).

---

## Why Two Passes Are Needed

A **single** forward pass under-constrains: it only enforces "no anchor exceeds the *left* side." But a restriction far to the right can force an earlier building *down* too. Example: `[[2,5]]` with `n` small — building 2's cap of 5 is irrelevant because building 1 (height 0) limits it to 1 from the left, **and** later a low cap could limit it from the right. The backward pass catches right-side constraints; together they yield each anchor's true ceiling.

---

## Validation

`solution.py` cross-checks against an O(n) brute force (relax `cap` forward then backward over every building, take the max) on **3000 random instances**, and times the billion-building case:

```
randomized cross-check passed ✓
n=1e9 → 250000050  (0.0000s)
```

---

## Key Insights

| Insight | Explanation |
|---|---|
| **Anchors, not buildings** | `n` up to 10⁹ — only the O(m) restrictions (plus 1 and n) are turning points. |
| **Propagate the ±1 rule both ways** | A cap is tightened by both the left and right neighbours. |
| **Tent peak is closed-form** | `⌊(lh + rh + dist) / 2⌋` — where the two rising lines cross. |
| **Add `[1,0]` and `[n, n−1]`** | Building 1 is fixed; n's natural ceiling closes the last gap. |
| **Complexity is `n`-independent** | Dominated by sorting the restrictions. |

---

## Edge Cases

| Case | Behavior |
|---|---|
| No restrictions | One gap `(1,0)→(n,n−1)` → peak `n−1` |
| `n` is restricted | Don't add the synthetic `[n, n−1]` anchor |
| Restriction looser than neighbours allow | Propagation tightens it to the real max |
| Adjacent tight caps | Peak between them stays low |
| `n = 2` | Single gap → height `1` |

---

## Approach Tags

`Constraint Propagation` · `Anchor Compression` · `Tent Peak Formula` · `Two-Pass Relaxation`

---

*Day 47 of the LeetCode Daily Challenge*
