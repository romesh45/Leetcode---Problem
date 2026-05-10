# 2770. Maximum Number of Jumps to Reach the Last Index

**Difficulty:** Medium  
**Topic Tags:** Array, Dynamic Programming  
**LeetCode Link:** [Problem 2770](https://leetcode.com/problems/maximum-number-of-jumps-to-reach-the-last-index/)

---

## What the Problem is Asking

You are standing at index `0` of an array. You want to reach the **last index** in as many jumps as possible. From any index `i`, you can jump forward to any index `j` (where `j > i`) — but only if the difference between the two values is within a range: `-target ≤ nums[j] - nums[i] ≤ target`.

In simple words: you can only land on an index if its value is **close enough** to where you currently are. The "closeness" is controlled by `target`. If it's impossible to reach the last index at all, return `-1`.

---

## Understanding the Jump Rule

The condition `-target ≤ nums[j] - nums[i] ≤ target` is just a fancy way of saying:

> **The absolute difference between the two values must be ≤ target.**

So if `target = 2` and you are at a cell with value `3`, you can only jump to cells whose values sit between `1` and `5`.

As `target` gets bigger, more jumps become valid — so you can make more hops. As `target` shrinks toward `0`, only cells with the exact same value can be landed on.

---

## Why "Maximum" Jumps?

Most jump problems ask for the *minimum* steps. This one flips it — we want the *maximum*. This means we prefer taking as many small hops as possible rather than one big leap. The challenge is figuring out which path allows the most hops while still reaching the end.

---

## Intuition — Think Backwards from Each Index

Imagine you are standing at index `j` and asking:

> "Which earlier indices could have jumped to me? And among those, which one gives me the most jumps so far?"

If you know the maximum jumps to reach every index before `j`, then the maximum jumps to reach `j` is simply:

> `1 + (the best of all valid predecessors of j)`

This is the core idea of **Dynamic Programming**. You build up the answer one index at a time, using previously computed results.

---

## The DP Table — Step by Step

Define `dp[i]` as the maximum number of jumps to reach index `i`. If index `i` is unreachable, mark it as `-1`.

**Starting point:** `dp[0] = 0` — you're already at index `0` and haven't jumped at all.

**For every index `j` from `1` to `n-1`:**
- Look back at every earlier index `i` (from `0` to `j-1`)
- If `i` is reachable (meaning `dp[i] ≠ -1`) AND the jump is valid (value difference ≤ target):
  - Then `j` can be reached in `dp[i] + 1` jumps
  - Keep the maximum of all such possibilities

**Final answer:** `dp[n-1]` — if it's still `-1` at the end, no valid path exists.

---

## Walking Through Example 1

```
nums = [1, 3, 6, 4, 1, 2],  target = 2

dp starts as: [0, -1, -1, -1, -1, -1]
               idx: 0   1   2   3   4   5
```

**Index 1 (value 3):**
Look back at index 0 (value 1). |3 − 1| = 2 ≤ 2 ✓
→ dp[1] = 0 + 1 = **1**

**Index 2 (value 6):**
From index 0: |6 − 1| = 5 > 2 ✗
From index 1: |6 − 3| = 3 > 2 ✗
→ dp[2] = **-1** (unreachable)

**Index 3 (value 4):**
From index 0: |4 − 1| = 3 > 2 ✗
From index 1: |4 − 3| = 1 ≤ 2 ✓  → dp[3] = 1 + 1 = 2
→ dp[3] = **2**

**Index 4 (value 1):**
From index 0: |1 − 1| = 0 ≤ 2 ✓  → 0 + 1 = 1
From index 1: |1 − 3| = 2 ≤ 2 ✓  → 1 + 1 = 2  ← better
→ dp[4] = **2**

**Index 5 (value 2):**
From index 0: |2 − 1| = 1 ✓  → 1
From index 1: |2 − 3| = 1 ✓  → 2
From index 2: unreachable, skip
From index 3: |2 − 4| = 2 ✓  → 2 + 1 = 3  ← best
From index 4: |2 − 1| = 1 ✓  → 2 + 1 = 3
→ dp[5] = **3** ✓

Final dp table:
```
index:  0   1   2   3   4   5
dp:    [0,  1,  -1,  2,  2,  3]
```
Answer = dp[5] = **3**

The path that achieves it: index 0 → 1 → 3 → 5

---

## Walking Through Example 2

```
nums = [1, 3, 6, 4, 1, 2],  target = 3
```

With a larger target, more jumps become valid. Every consecutive pair now satisfies the condition (differences are all ≤ 3), so you can hop one step at a time all the way to the end.

Path: `0 → 1 → 2 → 3 → 4 → 5` = **5 jumps**

The dp table fills up cleanly as `[0, 1, 2, 3, 4, 5]`.

---

## Walking Through Example 3

```
nums = [1, 3, 6, 4, 1, 2],  target = 0
```

Target = 0 means you can only jump to a cell with the **exact same value** as your current one. No two cells share a value in this array, and there's no valid path at all → **-1**

---

## Complexity

**Time — O(n²)**
For each of the `n` indices, we look back at all previous indices. That's at most `n × n` comparisons. With n ≤ 1000, this is at most 1,000,000 operations — perfectly fine.

**Space — O(n)**
Only a single `dp` array of size `n` is needed. No extra structures.

---

## Key Insights to Remember

**Why DP and not Greedy?**
A greedy approach (e.g., always picking the nearest reachable index) doesn't work here. Taking a "convenient" jump now might lead you into a dead end with no way forward. DP explores every valid predecessor for each index and always keeps the best result.

**Why start dp values at -1?**
The value `-1` acts as a sentinel for "unreachable." When we check predecessors, we skip any index still at `-1` — there's no point building on an unreachable position.

**Why does dp[0] = 0?**
You start at index 0 having made zero jumps. This is the seed for the entire DP — every other value is built from this.

**What does "looking back" mean?**
For every new index `j`, we scan all indices to its left and ask: "Can I arrive at `j` from here?" If yes, we update `dp[j]` if this path gives a higher jump count.

---

## Visual Summary

```
                  target = 2
  ┌─────────────────────────────────────────────────────────┐
  │  Index:   0     1     2     3     4     5               │
  │  Value:   1     3     6     4     1     2               │
  │                                                         │
  │  Valid jumps (|diff| ≤ 2):                              │
  │  0 → 1  (|3-1| = 2 ✓)                                  │
  │  1 → 3  (|4-3| = 1 ✓)                                  │
  │  3 → 5  (|2-4| = 2 ✓)   ← best path = 3 jumps         │
  │                                                         │
  │  dp:  [0,  1,  -1,  2,  2,  3]                         │
  └─────────────────────────────────────────────────────────┘
```

---

## Related Problems

| Problem | Similarity |
|---|---|
| [55. Jump Game](https://leetcode.com/problems/jump-game/) | Reachability with forward jumps (greedy) |
| [45. Jump Game II](https://leetcode.com/problems/jump-game-ii/) | Minimum jumps to reach end (greedy) |
| [1696. Jump Game VI](https://leetcode.com/problems/jump-game-vi/) | Maximum score path with DP + sliding window deque |
| [2297. Jump Game VIII](https://leetcode.com/problems/jump-game-viii/) | Minimum cost with monotonic stack DP |
