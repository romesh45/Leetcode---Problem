# Day 48 — LeetCode Challenge

## 1833. Maximum Ice Cream Bars

| Field | Details |
|---|---|
| **Difficulty** | Medium |
| **Topics** | Greedy · Counting Sort · Array · Sorting |
| **LeetCode Link** | [1833. Maximum Ice Cream Bars](https://leetcode.com/problems/maximum-ice-cream-bars/) |

---

## Problem Statement

There are `n` ice cream bars with prices `costs[i]`. A boy has `coins` coins and wants to buy **as many bars as possible** (any order). Return the maximum number of bars he can afford.

> The problem requires you to solve it with **counting sort**.

---

## Examples

### Example 1
```
Input:  costs = [1,3,2,4,1], coins = 7
Output: 4
```
Buy `1 + 1 + 2 + 3 = 7` → 4 bars.

### Example 2
```
Input:  costs = [10,6,8,7,7,8], coins = 5
Output: 0
```
Cheapest is `6 > 5` → none.

### Example 3
```
Input:  costs = [1,6,3,1,2,5], coins = 20
Output: 6
```
All 6 bars total `18 ≤ 20` → all of them.

---

## Constraints

- `1 <= n <= 10⁵`
- `1 <= costs[i] <= 10⁵`
- `1 <= coins <= 10⁸`

---

## Intuition

### Cheapest-first is optimal

We want to maximize the **count** of bars, not minimize spend on any particular bar. So always buy the cheapest available bar: spending fewer coins per bar leaves the most coins for more bars.

**Exchange argument:** suppose an optimal purchase skips a cheap bar `a` to buy a pricier bar `b`. Swapping `b` for `a` costs `a ≤ b` coins, freeing `b − a ≥ 0` extra coins while keeping the count the same — never worse. Repeating sorts the purchase into cheapest-first. ∎

### Why counting sort (and why it's the right call here)

A comparison sort is `O(n log n)`. But `costs[i] ≤ 10⁵` is a **small bounded range**, so we can sort by **tallying**:

1. `count[c]` = how many bars cost exactly `c`.
2. Sweep prices `1, 2, …, MAX` — this visits bars in **ascending price order** without comparisons, in `O(n + MAX)`.

That's the counting-sort the problem asks for, and it's asymptotically better than `O(n log n)` when `MAX` is small relative to `n log n`.

### Buy in bulk per price

At each price we don't loop bar-by-bar — we buy a whole batch: `min(count[price], coins // price)` bars (as many as exist, capped by what coins allow). Then subtract and continue.

### The early break

When `coins < price`, stop: every later price is **higher**, so nothing more is affordable.

---

## Algorithm

```
count[c] = tally of costs
bars = 0
for price = 1 .. MAX:
    if count[price] == 0: continue
    if coins < price: break
    buyable = min(count[price], coins // price)
    bars  += buyable
    coins -= buyable * price
return bars
```

---

## Solution

```python
from typing import List


class Solution:
    def maxIceCream(self, costs: List[int], coins: int) -> int:
        MAX_COST = max(costs)
        count = [0] * (MAX_COST + 1)
        for c in costs:
            count[c] += 1

        bars = 0
        for price in range(1, MAX_COST + 1):
            if count[price] == 0:
                continue
            if coins < price:
                break
            buyable = min(count[price], coins // price)
            bars += buyable
            coins -= buyable * price

        return bars
```

---

## Complexity Analysis

Let `M = max(costs) ≤ 10⁵`.

| | Complexity | Reason |
|---|---|---|
| **Time** | **O(n + M)** | Tally O(n) + sweep O(M); no comparison sort |
| **Space** | **O(M)** | The count array |

Beats the `O(n log n)` sort-and-greedy when `M` is modest.

---

## Full Trace — Example 1: `costs = [1,3,2,4,1], coins = 7`

**Counting:** `count[1]=2, count[2]=1, count[3]=1, count[4]=1`.

**Sweep:**

| price | count | `coins < price`? | buyable | bars | coins left |
|:-:|:-:|:-:|:-:|:-:|:-:|
| 1 | 2 | no | `min(2, 7//1)=2` | 2 | `7 − 2 = 5` |
| 2 | 1 | no | `min(1, 5//2)=1` | 3 | `5 − 2 = 3` |
| 3 | 1 | no | `min(1, 3//3)=1` | 4 | `3 − 3 = 0` |
| 4 | 1 | `0 < 4` → **break** | — | — | — |

**Answer: 4** ✓

---

## Full Trace — Example 2: `costs = [10,6,8,7,7,8], coins = 5`

`count[6]=1, count[7]=2, count[8]=2, count[10]=1`.

| price | count | `coins < price`? |
|:-:|:-:|:-:|
| 1–5 | 0 | (skipped) |
| 6 | 1 | `5 < 6` → **break** |

No bar bought → **0** ✓

---

## Why Bulk Buying Is Safe

Buying `min(count[price], coins // price)` at once is identical to looping one-at-a-time but faster:

- `coins // price` is the max bars of this price the budget allows.
- `count[price]` caps it to what's in stock.
- After the batch, either stock at this price is exhausted (move on) or coins can't buy another at this price (and since prices only rise, the loop will `break` shortly).

No greedy opportunity is missed because all bars at the same price are interchangeable.

---

## Alternative — Sort-Based Greedy

```python
def maxIceCream(self, costs, coins):
    bars = 0
    for c in sorted(costs):
        if coins < c:
            break
        coins -= c
        bars += 1
    return bars
```

Same greedy logic, `O(n log n)`. Cleaner to write, but the problem explicitly asks for **counting sort** — and the counting version is faster here given the bounded prices. (This repo uses it as the cross-check reference.)

---

## Key Insights

| Insight | Explanation |
|---|---|
| **Cheapest-first maximizes count** | Spending less per bar leaves more coins; provable by exchange. |
| **Counting sort fits bounded prices** | `costs[i] ≤ 10⁵` → tally + ascending sweep replaces comparison sort. |
| **Bulk-buy per price** | `min(stock, coins // price)` — no per-bar loop. |
| **Break when `coins < price`** | Higher prices follow; nothing more is affordable. |
| **O(n + M) beats O(n log n)** | The whole point of the mandated counting sort. |

---

## Edge Cases

| Case | Behavior |
|---|---|
| Can't afford the cheapest | Breaks immediately → `0` |
| Can afford everything | Buys all `n` bars |
| All same price | Buys `min(n, coins // price)` |
| Single bar | `1` if affordable, else `0` |
| Huge `coins` (10⁸) | Capped by stock, not budget |

---

## Approach Tags

`Counting Sort` · `Greedy Cheapest-First` · `Bounded-Value Tally` · `Bulk Purchase`

---

*Day 48 of the LeetCode Daily Challenge*
