# Day 27 — LeetCode Challenge

## 2126. Destroying Asteroids

| Field | Details |
|---|---|
| **Difficulty** | Medium |
| **Topics** | Greedy · Sorting · Exchange Argument |
| **LeetCode Link** | [2126. Destroying Asteroids](https://leetcode.com/problems/destroying-asteroids/) |

---

## Problem Statement

You're given an integer `mass` (the planet's starting mass) and an integer array `asteroids`. You may collide the planet with the asteroids in **any order**.

- If `planet_mass >= asteroid_mass`, the asteroid is destroyed and the planet **gains** its mass.
- Otherwise, the planet is destroyed.

Return `true` if **all** asteroids can be destroyed, else `false`.

---

## Examples

### Example 1

```
Input:  mass = 10, asteroids = [3, 9, 19, 5, 21]
Output: true
```

Order `[9, 19, 5, 3, 21]`: `10 → 19 → 38 → 43 → 46 → 67`. All destroyed.

### Example 2

```
Input:  mass = 5, asteroids = [4, 9, 23, 4]
Output: false
```

Even after absorbing everything else (`5 + 4 + 9 + 4 = 22`), the planet can't reach `23`.

---

## Constraints

- `1 <= mass <= 10⁵`
- `1 <= asteroids.length <= 10⁵`
- `1 <= asteroids[i] <= 10⁵`

---

## Intuition

### Mass only ever grows

Every successful collision **adds** the asteroid's mass to the planet. So as we destroy asteroids, the planet's mass is **monotonically non-decreasing**. There's no downside to destroying an asteroid — it only makes us stronger.

### Greedy: smallest first

Given that mass only grows, the optimal strategy is obvious: **always destroy the smallest remaining asteroid.**

- The smallest is the easiest to beat (lowest bar to clear with current mass).
- Destroying it boosts our mass, making the next-smallest even easier.
- By the time we reach the biggest asteroid, we've absorbed the mass of everything smaller — the maximum possible boost.

Sort ascending, sweep left to right, absorb as we go. If at any point the current (smallest remaining) asteroid exceeds our mass, we fail.

### Why failure is genuine when it happens

Here's the subtle part: **every ordering absorbs the same total mass.** So at the moment the sorted scan hits an asteroid `a` it can't beat, the planet's mass is exactly:

```
mass + (sum of all asteroids strictly smaller than a)
```

That's the **maximum mass achievable** before confronting anything as large as `a` — because any order must destroy those smaller asteroids first to be bigger, and they sum to a fixed amount. If that maximum isn't enough for `a`, **no ordering can succeed.** Fail fast.

---

## Exchange Argument (Proof of Optimality)

**Claim:** If *any* order destroys all asteroids, then the **sorted-ascending** order does too.

**Proof.** Take any winning order. Suppose it's not sorted — then at some step it destroys asteroid `b` while a smaller asteroid `a < b` is still available. Swap them: destroy `a` at this step instead.

- At this step, the planet's mass is unchanged (same history before it). Since `a < b ≤ mass`, asteroid `a` is destroyable. ✓
- After destroying `a`, the planet's mass is `mass + a`, which is **at least** the `mass + b` we'd have had... no wait — it's `mass + a ≤ mass + b`. But `b` will now be destroyed *later*, when the planet is at least as massive as it was originally at `b`'s old slot (mass only grows). So `b` remains destroyable.

Each such swap reduces the number of "inversions" (out-of-order pairs) without breaking the run. Repeating until no inversions remain yields the fully sorted order — still a winning order. ∎

Therefore sorting ascending succeeds **iff** the asteroids are destroyable at all.

---

## Algorithm

```
sort asteroids ascending
for a in asteroids:
    if mass < a: return False
    mass += a
return True
```

---

## Solution

```python
from typing import List


class Solution:
    def asteroidsDestroyed(self, mass: int, asteroids: List[int]) -> bool:
        asteroids.sort()
        for a in asteroids:
            if mass < a:
                return False
            mass += a
        return True
```

---

## Complexity Analysis

| | Complexity | Reason |
|---|---|---|
| **Time** | **O(n log n)** | Dominated by the sort; the sweep is O(n) |
| **Space** | **O(1)** extra | In-place sort + a running accumulator (sort may use O(n) internally) |

For `n ≤ 10⁵` this is instant.

> **Overflow note:** the planet's mass can grow up to `10⁵ + 10⁵ · 10⁵ ≈ 10¹⁰`, which exceeds 32-bit range. In Python this is a non-issue (arbitrary-precision ints); in Java/C++ use `long`.

---

## Full Trace — Example 1: `mass = 10, asteroids = [3, 9, 19, 5, 21]`

**Sorted:** `[3, 5, 9, 19, 21]`.

| Step | asteroid `a` | `mass < a`? | new `mass` |
|:-:|:-:|:-:|:-:|
| 1 | 3 | `10 < 3`? no | `10 + 3 = 13` |
| 2 | 5 | `13 < 5`? no | `13 + 5 = 18` |
| 3 | 9 | `18 < 9`? no | `18 + 9 = 27` |
| 4 | 19 | `27 < 19`? no | `27 + 19 = 46` |
| 5 | 21 | `46 < 21`? no | `46 + 21 = 67` |

Survived all → **return True** ✓

---

## Full Trace — Example 2: `mass = 5, asteroids = [4, 9, 23, 4]`

**Sorted:** `[4, 4, 9, 23]`.

| Step | asteroid `a` | `mass < a`? | new `mass` |
|:-:|:-:|:-:|:-:|
| 1 | 4 | `5 < 4`? no | `5 + 4 = 9` |
| 2 | 4 | `9 < 4`? no | `9 + 4 = 13` |
| 3 | 9 | `13 < 9`? no | `13 + 9 = 22` |
| 4 | 23 | `22 < 23`? **yes** | — → **return False** ✓ |

At step 4 the planet has absorbed *everything* smaller (mass `22`) — the maximum it could ever be before facing `23`. Still not enough → genuinely impossible.

---

## Why Not a Priority Queue?

You might reach for a min-heap ("always pop the smallest"). It works and gives the same answer, but it's strictly worse:

- Building/draining a heap is also `O(n log n)`, but with larger constants and `O(n)` extra space.
- Since the planet only grows, the "smallest available" never changes relative order — a one-time **sort** captures the entire greedy sequence. No need to re-extract minimums dynamically.

Sorting is the cleaner, faster realization of the same greedy idea.

---

## Key Insights

| Insight | Explanation |
|---|---|
| **Mass is monotonically non-decreasing** | Every collision adds mass — there's never a reason to skip a beatable asteroid. |
| **Greedy smallest-first is optimal** | Maximizes mass before the hard asteroids; provable via exchange argument. |
| **All orders absorb the same total** | So the sorted scan reaches each threshold with the max possible mass — failure is real. |
| **Sort beats a heap** | The greedy order is static (mass only grows), so one sort suffices. |
| **Watch for overflow in typed languages** | Mass can reach ~10¹⁰; use 64-bit integers outside Python. |

---

## Edge Cases

| Case | Behavior |
|---|---|
| `mass = 1, asteroids = [1]` | `1 >= 1` → destroy → **True** |
| `mass = 1, asteroids = [2]` | `1 < 2` immediately → **False** |
| Single asteroid larger than mass | **False** |
| All asteroids tiny | Sweep through, always **True** |
| Asteroid exactly equal to current mass | `mass >= a` (equality allowed) → destroyed |
| Chain that barely works (`5,[5,10,20,40]`) | `5→10→20→40→80` → **True** |

---

## Approach Tags

`Greedy` · `Sorting` · `Exchange Argument` · `Monotonic Accumulation`

---

*Day 27 of the LeetCode Daily Challenge*
