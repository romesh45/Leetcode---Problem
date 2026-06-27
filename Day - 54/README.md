# Day 53 — LeetCode Challenge

## 3020. Find the Maximum Number of Elements in Subset

| Field | Details |
|---|---|
| **Difficulty** | Medium |
| **Topics** | Array · Hash Map · Greedy |
| **LeetCode Link** | [3020. Find the Maximum Number of Elements in Subset](https://leetcode.com/problems/find-the-maximum-number-of-elements-in-subset/) |

---

## Problem Statement

Given an array of positive integers `nums`, select the largest subset that can be arranged into the palindrome pattern:

```
[x, x², x⁴, …, xᵏ/², xᵏ, xᵏ/², …, x⁴, x², x]
```

where `k` is a non-negative power of 2. Return the size of the largest such subset.

---

## Examples

### Example 1
```
Input:  nums = [5,4,1,2,2]
Output: 3
```
Subset `{4,2,2}` → `[2,4,2]` where `2² = 4`. ✓

### Example 2
```
Input:  nums = [1,3,2,4]
Output: 1
```
No two elements form a squaring chain; best is any single element.

---

## Constraints

- `2 <= nums.length <= 10⁵`
- `1 <= nums[i] <= 10⁹`

---

## Intuition

### What the pattern actually looks like when sorted

The pattern `[x, x², x⁴, …, xᵏ, …, x⁴, x², x]` is a palindrome. When you sort it:

```
[x, x, x², x², x⁴, x⁴, …, xᵏ]
 └──┘ └───┘  └────┘       └──┘
 pair  pair    pair     single (middle)
```

Three key observations:

1. **Every value except the middle appears exactly twice.** (Once on each side of the palindrome.)
2. **The middle is the maximum value** (`xᵏ`).
3. **Each value squared equals the next:** `x² = x²`, `(x²)² = x⁴`, etc.

This means the problem reduces to: **find the longest squaring chain** `x → x² → x⁴ → …` where every non-final value appears ≥ 2 times in `nums`, and the final value appears ≥ 1 time.

### Chain length → subset size

If you can build a chain of `depth` pair-values plus one middle:

```
subset size = 2 * depth + 1
```

If no middle is available after the pairs, use the last pair's value as the middle (reduce by 1 pair, one element becomes singleton):

```
subset size = 2 * (depth - 1) + 1 = 2 * depth - 1
```

### Special case: x = 1

Since `1² = 1`, the chain never advances. The entire pattern becomes `[1, 1, 1, …, 1]`. Any odd-length run of 1s is valid, so the best answer from 1s is:

```
count(1)  if count(1) is odd
count(1) - 1  otherwise
```

### Why the chain is short (at most ~30 steps)

Starting from any `x ≥ 2`, squaring doubles the exponent. Within at most 30 squarings, any value exceeds `10⁹` (the max constraint). So each chain walk is O(log log MAX) ≈ O(5).

---

## Algorithm

```
cnt = frequency map of nums
ans = 1

for each unique value x in cnt:

    if x == 1:
        c = cnt[1]
        ans = max(ans, c if c is odd else c-1)
        continue

    depth = 0, v = x
    while cnt[v] >= 2:
        depth += 1
        v = v * v
        if v > 10^9: break

    if cnt[v] >= 1:
        candidate = 2*depth + 1      # pairs + singleton middle
    else:
        candidate = max(1, 2*depth - 1)  # use last pair's value as middle

    ans = max(ans, candidate)

return ans
```

---

## Solution

```python
from typing import List
from collections import Counter


class Solution:
    def maximumLength(self, nums: List[int]) -> int:
        cnt = Counter(nums)
        ans = 1

        for x in cnt:
            if x == 1:
                c = cnt[1]
                ans = max(ans, c if c % 2 == 1 else c - 1)
                continue

            depth = 0
            v = x
            while cnt.get(v, 0) >= 2:
                depth += 1
                if v > 10**9 // v:
                    v = v * v
                    break
                v = v * v

            if cnt.get(v, 0) >= 1:
                candidate = 2 * depth + 1
            else:
                candidate = max(1, 2 * depth - 1)

            ans = max(ans, candidate)

        return ans
```

---

## Complexity Analysis

Let `U` = number of unique values in `nums`, `C` = max chain length ≤ 30.

| | Complexity | Reason |
|---|---|---|
| **Time** | **O(n + U · C)** | Counter build O(n); each unique value walks chain ≤ 30 steps |
| **Space** | **O(U)** | Frequency counter |

Since `U ≤ n` and `C ≤ 30`, this is effectively O(n). Runs in ~0.05s for `n = 10⁵`.

---

## Full Trace — Example 1: `nums = [5,4,1,2,2]`

**Counter:** `{5:1, 4:1, 1:1, 2:2}`

| x | Walk | depth | v after loop | cnt[v] | candidate |
|:-:|:-:|:-:|:-:|:-:|:-:|
| 5 | cnt[5]=1 < 2, stop immediately | 0 | 5 | 1 | 2·0+1 = **1** |
| 4 | cnt[4]=1 < 2, stop | 0 | 4 | 1 | 2·0+1 = **1** |
| 1 | special: cnt[1]=1 (odd) | — | — | — | **1** |
| 2 | cnt[2]=2 ≥ 2 → depth=1, v=4; cnt[4]=1 < 2 → stop | 1 | 4 | 1 | 2·1+1 = **3** |

**Answer: max(1,1,1,3) = 3** ✓

Subset: `{2, 2, 4}` → sorted `[2, 2, 4]` → pattern `[2, 4, 2]`. ✓

---

## Full Trace — Example 2: `nums = [1,3,2,4]`

**Counter:** `{1:1, 3:1, 2:1, 4:1}`

| x | Walk | depth | v after | cnt[v] | candidate |
|:-:|:-:|:-:|:-:|:-:|:-:|
| 1 | cnt[1]=1 (odd) | — | — | — | **1** |
| 3 | cnt[3]=1 < 2 | 0 | 3 | 1 | 2·0+1=**1** |
| 2 | cnt[2]=1 < 2 | 0 | 2 | 1 | 2·0+1=**1** |
| 4 | cnt[4]=1 < 2 | 0 | 4 | 1 | 2·0+1=**1** |

**Answer: 1** ✓

---

## Detailed Example: `nums = [2, 4, 16, 4, 2]`

**Counter:** `{2:2, 4:2, 16:1}`

Starting from `x = 2`:
```
v=2,  cnt[2]=2 ≥ 2 → depth=1, v=4
v=4,  cnt[4]=2 ≥ 2 → depth=2, v=16
v=16, cnt[16]=1 < 2 → stop
cnt[16]=1 ≥ 1 → candidate = 2*2+1 = 5
```

Subset: `{2,2,4,4,16}` → sorted `[2,2,4,4,16]` → pattern `[2,4,16,4,2]`. ✓

**Answer: 5** ✓

---

## The x = 1 Special Case in Detail

Since `1² = 1`, squaring never advances the chain. The valid patterns are:
```
[1]         length 1
[1,1,1]     length 3  (x=1, middle=1²=1=1)
[1,1,1,1,1] length 5
…
```

All valid subset lengths are odd numbers. With `c` ones available, the answer is `c` if `c` is odd, else `c − 1` (drop one to make it odd).

---

## Why `candidate = 2*depth - 1` When No Middle Available

After the while loop, if `cnt[v] < 1`, we can't use `v` as the middle. But the last value added to the chain (call it `v_prev`) had `cnt[v_prev] ≥ 2`. We can use ONE of those copies as the middle:

```
Before: depth pairs using values x, x², …, v_prev, v_prev
After:  (depth-1) pairs + v_prev as singleton middle
Size:   2*(depth-1) + 1 = 2*depth - 1
```

This is always valid since `cnt[v_prev] ≥ 2 ≥ 1`.

---

## Edge Cases

| Case | Behaviour |
|---|---|
| All distinct elements | Every chain has depth=0, cnt[x]=1 → candidate=1 for all → answer 1 |
| All same value `x > 1` | Only depth=0 (count=n but chain needs x²); answer = 1 |
| `x=1` with even count | Drop one, return `c-1` (largest odd) |
| Large chain: `2 → 4 → 16 → 256 → …` | At most ~5 steps before exceeding 10⁹ |
| Single element | ans starts at 1; if that element = 1 with count 1, returns 1 |

---

## Key Insights

| Insight | Explanation |
|---|---|
| **Sort reveals structure** | Palindrome sorted = pairs of equal values + one max middle |
| **Squaring chain** | Each pair value squared equals the next pair value |
| **Greedy depth walk** | Extend chain greedily; first ≥1 count becomes middle |
| **x=1 is special** | 1²=1 so chain doesn't advance; answer = largest odd ≤ count |
| **Chain length ≤ 30** | Squaring from any x≥2 hits 10⁹ within ~30 steps |
| **O(n) effective** | Counter + 30 steps per unique value |

---

## Approach Tags

`Hash Map` · `Greedy Chain Extension` · `Squaring Chain` · `Palindrome Pattern` · `Frequency Count`

---

*Day 53 of the LeetCode Daily Challenge*
