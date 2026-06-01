# Day 28 — LeetCode Challenge

## 2144. Minimum Cost of Buying Candies With Discount

| Field | Details |
|---|---|
| **Difficulty** | Easy |
| **Topics** | Greedy · Sorting · Exchange Argument |
| **LeetCode Link** | [2144. Minimum Cost of Buying Candies With Discount](https://leetcode.com/problems/minimum-cost-of-buying-candies-with-discount/) |

---

## Problem Statement

A shop runs a promotion: **for every two candies bought, you get a third candy free.** The free candy must cost **≤ the minimum** of the two candies you bought.

Given a 0-indexed array `cost` where `cost[i]` is the cost of candy `i`, return the **minimum total cost** to buy all candies.

---

## Examples

### Example 1

```
Input:  cost = [1, 2, 3]
Output: 5
```

Buy `2` and `3`, take `1` free → pay `5`. (We can't free the `2` by buying `1` and `3`, since the free candy must be `≤ min(1,3) = 1`.)

### Example 2

```
Input:  cost = [6, 5, 7, 9, 2, 2]
Output: 23
```

Buy `9, 7` → free `6`. Buy `5, 2` → free `2`. Pay `9 + 7 + 5 + 2 = 23`.

### Example 3

```
Input:  cost = [5, 5]
Output: 10
```

Only two candies — no third to take free. Pay both → `10`.

---

## Constraints

- `1 <= cost.length <= 100`
- `1 <= cost[i] <= 100`

---

## Intuition

### The free candy is always the cheapest of its triple

The promotion rule says the free candy must cost `≤ min(two bought)`. So whatever triple you form, the free one is the **smallest of the three** — you can never free a candy more expensive than something you paid for.

### Maximize the value of free candies

We pay for everything except the freebies, so to minimize total cost we want the **free candies to be as expensive as possible**.

The play: **sort descending**, then group candies in threes. In each group, buy the two priciest and free the third (the cheapest of that group, but still the most expensive candy we're *allowed* to free at that stage).

After sorting descending, the free candies land at indices `2, 5, 8, …` — every position `≡ 2 (mod 3)`.

### Worked logic on the sorted order

```
sorted desc:  [c0 ≥ c1 ≥ c2 ≥ c3 ≥ c4 ≥ c5 ≥ …]
              buy  buy  FREE buy  buy  FREE …
              c0   c1   c2   c3   c4   c5
```

`c2 ≤ min(c0, c1)` ✓ (it's smaller than both). `c5 ≤ min(c3, c4)` ✓. Every freebie is legal, and each is the largest candy eligible to be free at that point.

---

## Exchange Argument (Proof of Optimality)

**Claim:** Sorting descending and freeing every 3rd candy minimizes total cost.

**Proof.** Sort descending. The two most expensive candies `c0, c1` can never be free — nothing else is `≥` them to act as the "two bought" with a larger freebie. So the best we can do with the first group is **buy `c0, c1` and free `c2`** (the largest remaining, hence the most valuable legal freebie).

Suppose an optimal solution frees some candy other than `c2` in this first triple — say it frees `c_j` with `j > 2`, so `c_j ≤ c2`. Then `c2` is paid for and `c_j` is free. Swap: free `c2` instead and pay for `c_j`. The swap is legal (`c2 ≤ min(c0, c1)` still holds) and saves `c2 − c_j ≥ 0`. So freeing `c2` is at least as good.

Remove `c0, c1, c2` and recurse on `cost[3:]` — identical structure. Induction gives the full greedy: free indices `2, 5, 8, …`. ∎

---

## Algorithm

```
sort cost descending
total = 0
for i, c in enumerate(cost):
    if i % 3 != 2:        # skip every 3rd candy — it's free
        total += c
return total
```

---

## Solution

```python
from typing import List


class Solution:
    def minimumCost(self, cost: List[int]) -> int:
        cost.sort(reverse=True)
        total = 0
        for i, c in enumerate(cost):
            if i % 3 != 2:
                total += c
        return total
```

---

## Complexity Analysis

| | Complexity | Reason |
|---|---|---|
| **Time** | **O(n log n)** | Dominated by the sort; the scan is O(n) |
| **Space** | **O(1)** extra | In-place sort + a running accumulator |

For `n ≤ 100` this is trivially fast.

---

## Full Trace — Example 2: `cost = [6, 5, 7, 9, 2, 2]`

**Sorted descending:** `[9, 7, 6, 5, 2, 2]`.

| Index `i` | cost `c` | `i % 3` | free? | add to total |
|:-:|:-:|:-:|:-:|:-:|
| 0 | 9 | 0 | no | `+9` → 9 |
| 1 | 7 | 1 | no | `+7` → 16 |
| 2 | 6 | 2 | **free** | — |
| 3 | 5 | 0 | no | `+5` → 21 |
| 4 | 2 | 1 | no | `+2` → 23 |
| 5 | 2 | 2 | **free** | — |

**Total = 23** ✓ (free candies: `6` and `2` — the most valuable freebies possible).

---

## Full Trace — Example 1: `cost = [1, 2, 3]`

**Sorted descending:** `[3, 2, 1]`.

| Index `i` | cost `c` | free? | total |
|:-:|:-:|:-:|:-:|
| 0 | 3 | no | 3 |
| 1 | 2 | no | 5 |
| 2 | 1 | **free** | 5 |

**Total = 5** ✓

---

## Why Descending, Not Ascending?

If you sorted **ascending** and freed every 3rd candy, you'd be giving away the *cheapest* candies — the least valuable freebies — and paying for the expensive ones. That **maximizes** cost, the opposite of what we want.

Quick counter-check on `[1, 2, 3]`:
- Ascending `[1, 2, 3]`, free index 2 → free `3`, pay `1 + 2 = 3`. **But this is illegal** — freeing `3` requires `3 ≤ min(1, 2) = 1`, which is false.
- Descending `[3, 2, 1]`, free index 2 → free `1`, pay `3 + 2 = 5`. **Legal and correct.**

Descending isn't just cheaper — it's the only ordering that keeps every freebie **legal** (the smallest-of-triple constraint).

---

## Key Insights

| Insight | Explanation |
|---|---|
| **Free candy = cheapest of its triple** | The `≤ min(bought)` rule forces this. |
| **Maximize freebie value** | We pay for everything except freebies, so make those as expensive as legally allowed. |
| **Sort descending, skip index ≡ 2 (mod 3)** | Puts the largest legal freebie in each group. |
| **Ascending would be both costlier and illegal** | Freeing cheap candies wastes the discount; freeing expensive ones breaks the rule. |
| **Leftover 1 or 2 candies are fully paid** | A group needs 3 candies to grant a freebie. |

---

## Edge Cases

| Case | Behavior |
|---|---|
| `cost = [5, 5]` | Only 2 candies, no freebie → pay both → `10` |
| `cost = [1]` | Single candy, paid → `1` |
| `cost = [1, 1, 1]` | Free one `1` → pay `2` |
| 6 identical candies `[10]*6` | Two freebies → pay 4 × 10 = `40` |
| `n` not divisible by 3 | Trailing 1–2 candies are paid in full (no third to free) |

---

## Approach Tags

`Greedy` · `Sorting (Descending)` · `Modular Indexing` · `Exchange Argument`

---

*Day 28 of the LeetCode Daily Challenge*
