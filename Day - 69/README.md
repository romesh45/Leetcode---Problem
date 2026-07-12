# Day 64 — LeetCode Challenge

## 1331. Rank Transform of an Array

| Field | Details |
|---|---|
| **Difficulty** | Easy |
| **Topics** | Array · Hash Table · Sorting |
| **LeetCode Link** | [1331. Rank Transform of an Array](https://leetcode.com/problems/rank-transform-of-an-array/) |

---

## Problem Statement

Replace each element of `arr` with its rank — where rank 1 is smallest, equal elements share a rank, and ranks are as small as possible (no gaps).

---

## Examples

### Example 1
```
Input:  arr = [40,10,20,30]
Output: [4,1,2,3]
```

### Example 2
```
Input:  arr = [100,100,100]
Output: [1,1,1]
```

### Example 3
```
Input:  arr = [37,12,28,9,100,56,80,5,12]
Output: [5,3,4,2,8,6,7,1,3]
```

---

## Constraints

- `0 <= arr.length <= 10⁵`
- `-10⁹ <= arr[i] <= 10⁹`

---

## Intuition

Wrapping `set(arr)` around the sort does all the heavy lifting: deduplication ensures equal values land on the same rank, and sorting gives the correct relative order. Enumerating the sorted unique values assigns consecutive ranks starting at 1 — no gaps by construction.

---

## Solution

```python
from typing import List


class Solution:
    def arrayRankTransform(self, arr: List[int]) -> List[int]:
        rank = {v: i + 1 for i, v in enumerate(sorted(set(arr)))}
        return [rank[x] for x in arr]
```

---

## Complexity Analysis

| | Complexity | Reason |
|---|---|---|
| **Time** | **O(n log n)** | Dominated by sorting the unique values |
| **Space** | **O(n)** | Rank dict holds at most n entries |

---

## Edge Cases

| Case | Behaviour |
|---|---|
| Empty array | `set([])` is empty; dict comprehension is empty; result `[]` |
| All elements equal | One unique value → rank `{v: 1}`; every position maps to `1` |
| All elements distinct | k unique values → ranks 1..k, no ties |
| Negative values | `sorted` handles negatives natively; ranks still start at 1 |

---

## Approach Tags

`Sorting` · `Hash Map` · `Rank Assignment`

---

*Day 64 of the LeetCode Daily Challenge*
