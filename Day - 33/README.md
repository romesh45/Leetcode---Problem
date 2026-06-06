# Day 33 — LeetCode Challenge

## 2574. Left and Right Sum Differences

| Field | Details |
|---|---|
| **Difficulty** | Easy |
| **Topics** | Array · Prefix Sum · Single Pass |
| **LeetCode Link** | [2574. Left and Right Sum Differences](https://leetcode.com/problems/left-and-right-sum-differences/) |

---

## Problem Statement

Given a 0-indexed array `nums` of size `n`, define:

- `leftSum[i]` = sum of elements **strictly left** of index `i` (or `0` if none).
- `rightSum[i]` = sum of elements **strictly right** of index `i` (or `0` if none).

Return `answer` where `answer[i] = |leftSum[i] − rightSum[i]|`.

---

## Examples

### Example 1

```
Input:  nums = [10, 4, 8, 3]
Output: [15, 1, 11, 22]
```

`leftSum  = [0, 10, 14, 22]`
`rightSum = [15, 11, 3, 0]`
`answer   = [|0−15|, |10−11|, |14−3|, |22−0|] = [15, 1, 11, 22]`

### Example 2

```
Input:  nums = [1]
Output: [0]
```

Both sums are `0` → `|0 − 0| = 0`.

---

## Constraints

- `1 <= nums.length <= 1000`
- `1 <= nums[i] <= 10⁵`

---

## Intuition

### Don't build two arrays — derive the right sum

The naive approach materializes both `leftSum` and `rightSum`. But there's a tidy relationship: for any index `i`, the whole array splits into three disjoint parts:

```
[ ...left... ]  nums[i]  [ ...right... ]
     left                     right
```

So:

```
left + nums[i] + right = total
⟹  right = total − left − nums[i]
```

If we precompute `total = sum(nums)` and carry a running `left` prefix sum, the `right` sum is just **arithmetic** — no second scan, no second array.

### One clean pass

Walk left to right:
1. Compute `right = total − left − x`.
2. Append `|left − right|`.
3. Add `x` into `left` for the next index.

Each step is O(1).

---

## Algorithm

```
total = sum(nums)
left  = 0
for x in nums:
    right = total − left − x
    answer.append(|left − right|)
    left += x
return answer
```

---

## Solution

```python
from typing import List


class Solution:
    def leftRightDifference(self, nums: List[int]) -> List[int]:
        total = sum(nums)
        left = 0
        answer = []
        for x in nums:
            right = total - left - x
            answer.append(abs(left - right))
            left += x
        return answer
```

---

## Complexity Analysis

| | Complexity | Reason |
|---|---|---|
| **Time** | **O(n)** | One pass for `total`, one pass to fill `answer` |
| **Space** | **O(1)** extra | Two scalars (`total`, `left`); output array not counted |

---

## Full Trace — Example 1: `nums = [10, 4, 8, 3]`

`total = 10 + 4 + 8 + 3 = 25`.

| i | x | `left` (before) | `right = 25 − left − x` | `|left − right|` | `left` (after) |
|:-:|:-:|:-:|:-:|:-:|:-:|
| 0 | 10 | 0 | `25 − 0 − 10 = 15` | `|0 − 15| = 15` | 10 |
| 1 | 4 | 10 | `25 − 10 − 4 = 11` | `|10 − 11| = 1` | 14 |
| 2 | 8 | 14 | `25 − 14 − 8 = 3` | `|14 − 3| = 11` | 22 |
| 3 | 3 | 22 | `25 − 22 − 3 = 0` | `|22 − 0| = 22` | 25 |

Output: `[15, 1, 11, 22]` ✓

---

## Alternative — Explicit Prefix/Suffix Arrays

The textbook version builds both arrays first:

```python
def leftRightDifference(self, nums):
    n = len(nums)
    leftSum = [0] * n
    rightSum = [0] * n
    for i in range(1, n):
        leftSum[i] = leftSum[i-1] + nums[i-1]
    for i in range(n-2, -1, -1):
        rightSum[i] = rightSum[i+1] + nums[i+1]
    return [abs(leftSum[i] - rightSum[i]) for i in range(n)]
```

Same `O(n)` time but `O(n)` extra space for the two helper arrays. The single-pass version achieves the same result in `O(1)` extra space — cleaner and lighter.

---

## Key Insights

| Insight | Explanation |
|---|---|
| **`right = total − left − nums[i]`** | The array partitions into left / current / right, so the right sum is derivable. |
| **One running prefix replaces two arrays** | Carry `left`; compute `right` arithmetically each step. |
| **Precompute `total` once** | Turns each right-sum lookup into O(1). |
| **No suffix scan needed** | The subtraction eliminates a second pass. |

---

## Edge Cases

| Case | Behavior |
|---|---|
| `nums = [1]` | `left = 0`, `right = 0` → `[0]` |
| Two equal elements `[5, 5]` | `[|0−5|, |5−0|] = [5, 5]` |
| All equal `[2,2,2,2]` | Symmetric result `[6, 2, 2, 6]` |
| Single large element `[100]` | `[0]` |
| Increasing run | Right sum shrinks as `i` grows; answer dips then climbs |

---

## Approach Tags

`Prefix Sum` · `Single Pass` · `Total-Minus-Prefix` · `Constant Space`

---

*Day 33 of the LeetCode Daily Challenge*
