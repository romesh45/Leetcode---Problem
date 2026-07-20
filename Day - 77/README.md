# Day 72 -- LeetCode Challenge

## 1260. Shift 2D Grid

| Field | Details |
|---|---|
| **Difficulty** | Easy |
| **Topics** | Array -- Matrix -- Simulation |
| **LeetCode Link** | [1260. Shift 2D Grid](https://leetcode.com/problems/shift-2d-grid/) |

---

## Problem Statement

Shift a 2D grid `k` times: each element moves one position to the right, wrapping from the end of a row to the start of the next, and from the last cell back to `grid[0][0]`.

---

## Examples

### Example 1
```
Input:  grid = [[1,2,3],[4,5,6],[7,8,9]], k = 1
Output: [[9,1,2],[3,4,5],[6,7,8]]
```

### Example 2
```
Input:  grid = [[3,8,1,9],[19,7,2,5],[4,6,11,10],[12,0,21,13]], k = 4
Output: [[12,0,21,13],[3,8,1,9],[19,7,2,5],[4,6,11,10]]
```

### Example 3
```
Input:  grid = [[1,2,3],[4,5,6],[7,8,9]], k = 9
Output: [[1,2,3],[4,5,6],[7,8,9]]
```

---

## Constraints

- `1 <= m, n <= 50`
- `-1000 <= grid[i][j] <= 1000`
- `0 <= k <= 100`

---

## Intuition

Row-major order makes the grid a linear sequence of m*n elements. One shift moves every element one position forward (cyclically). Shifting k times is a cyclic rotation by k -- mod m*n to avoid redundant full cycles.

Flatten, rotate, reshape.

---

## Solution

```python
from typing import List


class Solution:
    def shiftGrid(self, grid: List[List[int]], k: int) -> List[List[int]]:
        m, n = len(grid), len(grid[0])
        flat = [v for row in grid for v in row]
        k %= m * n
        flat = flat[-k:] + flat[:-k]
        return [flat[i * n:(i + 1) * n] for i in range(m)]
```

---

## Complexity Analysis

| | Complexity | Reason |
|---|---|---|
| **Time** | **O(m * n)** | Flatten + rotate + reshape each touch every cell once |
| **Space** | **O(m * n)** | Flat array and output grid |

---

## Edge Cases

| Case | Behaviour |
|---|---|
| `k % (m*n) == 0` | Rotation is 0, returns original grid |
| 1x1 grid | Any k leaves the single element unchanged |
| `k = 0` | flat[-0:] = flat[:] (full list) + flat[:-0] = flat[:] -- handled by mod |

---

## Approach Tags

`Flatten` -- `Cyclic Rotation` -- `Reshape`

---

*Day 72 of the LeetCode Daily Challenge*
