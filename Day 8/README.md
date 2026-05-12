# Day 7 — LeetCode Challenge

## 1665. Minimum Initial Energy to Finish Tasks

| Field | Details |
|---|---|
| **Difficulty** | Hard |
| **Topics** | Greedy · Sorting · Custom Sort |
| **LeetCode Link** | [1665. Minimum Initial Energy to Finish Tasks](https://leetcode.com/problems/minimum-initial-energy-to-finish-tasks/) |

---

## Problem Statement

You are given an array `tasks` where `tasks[i] = [actualᵢ, minimumᵢ]`:

- **`actualᵢ`** — energy actually spent to finish task `i`.
- **`minimumᵢ`** — energy you must have **before** starting task `i`.

> Example: task `[10, 12]` with current energy `11` → can't start. With current energy `13` → finish it; energy drops to `3`.

You can do the tasks in **any order**. Return the minimum initial energy required to finish all of them.

---

## Examples

### Example 1

```
Input:  tasks = [[1,2], [2,4], [4,8]]
Output: 8
```

Order chosen: do `[4,8]` first, then `[2,4]`, then `[1,2]`.
- Start 8 → after [4,8]: 4
- 4 → after [2,4]: 2
- 2 → after [1,2]: 1 ✓

### Example 2

```
Input:  tasks = [[1,3], [2,4], [10,11], [10,12], [8,9]]
Output: 32
```

### Example 3

```
Input:  tasks = [[1,7], [2,8], [3,9], [4,10], [5,11], [6,12]]
Output: 27
```

---

## Constraints

- `1 <= tasks.length <= 10^5`
- `1 <= actualᵢ <= minimumᵢ <= 10^4`

---

## Intuition

### The "buffer" insight

Define **surplus** of a task = `minimum − actual`. This is the **slack**: how much energy gets "wasted" sitting in your pocket above what you'll actually spend.

- Task `[1, 2]`: surplus = 1 (you need 2 to start, but only use 1)
- Task `[4, 8]`: surplus = 4 (you need 8 to start, but only use 4)

**Why do high-surplus tasks first?**

A high-surplus task has a high "entry fee" (minimum) relative to its actual cost. If you do it later, you've already spent energy on earlier tasks — so you need **even more** initial energy to still meet that high minimum. Do it early, while your energy reserves are full.

### The pairwise exchange argument

Consider any two adjacent tasks A and B in some ordering. Compare the energy required:

| Order | Required initial energy |
|---|---|
| A then B | `max(minₐ, actualₐ + minᵦ)` |
| B then A | `max(minᵦ, actualᵦ + minₐ)` |

Working through the algebra: A should come before B if and only if **`minₐ − actualₐ ≥ minᵦ − actualᵦ`** — bigger surplus first.

### The simulation idea

After sorting, we don't need a complex DP. Simulate from energy = 0:

- Walk through the sorted tasks
- If your current energy can't cover the task's minimum, "top up" by exactly the deficit
- Sum of all top-ups = the minimum initial energy

This works because top-ups are exactly the deficits that the optimal initial energy must cover. We never top up more than needed.

---

## Algorithm

```
1. Sort tasks descending by (minimum − actual).

2. energy  = 0      # running total of top-ups (this is the answer)
   current = 0      # energy available right now

3. For each (actual, minimum) in sorted order:
     if current < minimum:
         deficit = minimum - current
         energy  += deficit
         current  = minimum
     current -= actual

4. Return energy.
```

---

## Solution

```python
from typing import List


class Solution:
    def minimumEffort(self, tasks: List[List[int]]) -> int:
        # Sort by (minimum - actual) descending.
        # Tasks with a bigger "buffer" go first — they have high entry cost
        # relative to spend, so doing them early avoids paying that cost later.
        tasks.sort(key=lambda x: x[1] - x[0], reverse=True)

        energy  = 0   # total initial energy required (answer)
        current = 0   # energy available right now

        for actual, minimum in tasks:
            # Top up only when forced to.
            if current < minimum:
                energy  += minimum - current
                current  = minimum
            current -= actual

        return energy
```

---

## Complexity Analysis

| | Complexity | Reason |
|---|---|---|
| **Time** | **O(n log n)** | Dominated by the sort; the simulation is linear |
| **Space** | **O(1)** extra | In-place sort, two scalars for state |

---

## Full Trace — Example 1: `[[1,2], [2,4], [4,8]]`

**Step 1 — Sort by surplus descending:**

| Task | actual | minimum | surplus |
|---|:---:|:---:|:---:|
| `[4, 8]` | 4 | 8 | **4** |
| `[2, 4]` | 2 | 4 | **2** |
| `[1, 2]` | 1 | 2 | **1** |

**Step 2 — Simulate:**

| Iteration | `current` (before) | `minimum` | Top up | `current` after top-up | After task (−actual) | `energy` |
|:-:|:-:|:-:|:-:|:-:|:-:|:-:|
| `[4, 8]` | 0 | 8 | **+8** | 8 | 4 | **8** |
| `[2, 4]` | 4 | 4 | — | 4 | 2 | 8 |
| `[1, 2]` | 2 | 2 | — | 2 | 1 | 8 |

**Answer: 8** ✓

---

## Full Trace — Example 2: `[[1,3], [2,4], [10,11], [10,12], [8,9]]`

**Sorted by surplus descending** (ties broken in original order — stable sort):

| Task | surplus |
|---|:---:|
| `[1, 3]` | 2 |
| `[2, 4]` | 2 |
| `[10, 12]` | 2 |
| `[10, 11]` | 1 |
| `[8, 9]` | 1 |

**Simulation:**

| Task | current before | min | top up | current after | energy |
|---|:-:|:-:|:-:|:-:|:-:|
| `[1, 3]` | 0 | 3 | **+3** | 3 → 2 | 3 |
| `[2, 4]` | 2 | 4 | **+2** | 4 → 2 | 5 |
| `[10, 12]` | 2 | 12 | **+10** | 12 → 2 | 15 |
| `[10, 11]` | 2 | 11 | **+9** | 11 → 1 | 24 |
| `[8, 9]` | 1 | 9 | **+8** | 9 → 1 | **32** |

**Answer: 32** ✓

---

## Why "Top Up" Equals the Answer

A cleaner mental model: think of `energy` as an IOU you keep adding to whenever you can't pay.

After all tasks:
```
energy = sum of all top-ups
       = sum of (minimum_k − current_at_step_k)  [whenever positive]
       = minimum starting balance such that current never goes negative
       = answer
```

Each top-up at step `k` exactly raises `current` to `minimum[k]`. Right after the top-up, the simulation's state is identical to "started with `energy_so_far` initial energy and processed tasks 0..k." So whatever final `energy` ends at is precisely the smallest starting balance that works.

---

## Key Insights

| Insight | Explanation |
|---|---|
| **Sort by surplus, not by minimum or actual alone** | Surplus captures the relative pain of doing the task late. High-surplus tasks pay more dearly when deferred. |
| **Greedy works only after sorting** | The simulation is dumb — it just tops up when forced. The intelligence is entirely in the sort. |
| **Top-up sum = answer** | Every top-up is a deficit that the initial energy must cover. They never overlap (linear scan), so they sum cleanly. |
| **Stable sort matters for ties** | When surpluses tie, any order among equals works. Python's `sort` is stable, which preserves input order. |

---

## Why Sorting by Minimum or Actual Alone Fails

**By minimum ascending** (`[1,3], [2,4], [8,9], [10,11], [10,12]`):
- After `[8,9]`: current = ... — needs additional top-ups later → ends higher than 32.

**By actual descending** (`[10,11], [10,12], [8,9], [2,4], [1,3]`):
- Doesn't exploit the high-surplus tasks' position advantage → suboptimal.

Only sorting by **`minimum − actual` descending** gives a provably optimal arrangement (per the pairwise exchange argument).

---

## Edge Cases

| Case | Behavior |
|---|---|
| Single task `[a, m]` | Returns `m` (need exactly the minimum to start) |
| All tasks identical | All surpluses equal; top up exactly `m` once, then chain |
| `actual = minimum` for all | Surplus = 0 throughout; total energy = sum of all actuals (no overhead) |
| Very high surplus task | Dominates the answer; gets placed first |

---

## Approach Tags

`Greedy` · `Custom Sort Comparator` · `Pairwise Exchange Argument` · `Simulation`

---

*Day 7 of the LeetCode Daily Challenge*
