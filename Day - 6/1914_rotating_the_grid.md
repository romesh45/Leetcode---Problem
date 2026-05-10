# 1914. Cyclically Rotating a Grid

**Difficulty:** Medium  
**Topic Tags:** Array, Matrix, Simulation  
**LeetCode Link:** [Problem 1914](https://leetcode.com/problems/cyclically-rotating-a-grid/)

---

## Problem Statement

Given an `m × n` matrix and an integer `k`, rotate each concentric layer counter-clockwise `k` times and return the result.

---

## Key Insight — Flatten, Rotate, Restore

> The 2D rotation problem reduces to a simple 1D list rotation.

Every layer is a ring of cells. Traverse it clockwise into a flat list, shift the list left by `k` positions, then write values back in the same traversal order.

```
Layer 0 of [[1,2,3,4],[5,6,7,8],[9,10,11,12],[13,14,15,16]]:

Clockwise extraction:   [1, 2, 3, 4, 8, 12, 16, 15, 14, 13, 9, 5]
                         ↑ top → → → → right ↓   bottom ← ← left ↑

Rotate left by k=2:     [3, 4, 8, 12, 16, 15, 14, 13, 9, 5, 1, 2]
                         (elements[2:] + elements[:2])

Place back clockwise:   top=[3,4,8,12]  right=[16,15,14]  bottom=[13,9,5]  left=[1,2]
```

---

## Why "rotate left by k"?

Counter-clockwise rotation means each element moves to the **next position counter-clockwise**, which is equivalent to the **previous position in a clockwise traversal**. So the element that was at index `k` in clockwise order becomes index `0` after `k` rotations.

`rotated = elements[k:] + elements[:k]`

---

## Algorithm

```
num_layers = min(m, n) // 2

for layer in 0 → num_layers - 1:
    ┌─ Extract clockwise ──────────────────────────────────────────────┐
    │  top row:    (layer, layer)     →  (layer, n-1-layer)           │
    │  right col:  (layer+1, n-1-layer) → (m-1-layer, n-1-layer)     │
    │  bottom row: (m-1-layer, n-2-layer) → (m-1-layer, layer)       │
    │  left col:   (m-2-layer, layer) → (layer+1, layer)             │
    └──────────────────────────────────────────────────────────────────┘
    k_eff = k % len(elements)              ← handles k > layer size
    rotated = elements[k_eff:] + elements[:k_eff]
    Place back in the same clockwise traversal order
```

---

## Solution

```python
from typing import List

class Solution:
    def rotateGrid(self, grid: List[List[int]], k: int) -> List[List[int]]:
        m, n = len(grid), len(grid[0])

        def extract_layer(layer: int) -> List[int]:
            r1, c1 = layer, layer
            r2, c2 = m - 1 - layer, n - 1 - layer
            elements = []

            for c in range(c1, c2 + 1):          # top row →
                elements.append(grid[r1][c])
            for r in range(r1 + 1, r2 + 1):      # right col ↓
                elements.append(grid[r][c2])
            for c in range(c2 - 1, c1 - 1, -1):  # bottom row ←
                elements.append(grid[r2][c])
            for r in range(r2 - 1, r1, -1):       # left col ↑
                elements.append(grid[r][c1])

            return elements

        def place_layer(layer: int, elements: List[int]) -> None:
            r1, c1 = layer, layer
            r2, c2 = m - 1 - layer, n - 1 - layer
            idx = 0

            for c in range(c1, c2 + 1):
                grid[r1][c] = elements[idx]; idx += 1
            for r in range(r1 + 1, r2 + 1):
                grid[r][c2] = elements[idx]; idx += 1
            for c in range(c2 - 1, c1 - 1, -1):
                grid[r2][c] = elements[idx]; idx += 1
            for r in range(r2 - 1, r1, -1):
                grid[r][c1] = elements[idx]; idx += 1

        for layer in range(min(m, n) // 2):
            elements = extract_layer(layer)
            k_eff = k % len(elements)
            place_layer(layer, elements[k_eff:] + elements[:k_eff])

        return grid
```

---

## Dry Run — Example 1: `k=1`, `[[40,10],[30,20]]`

```
Layer 0 — 2×2, perimeter = 4 cells

Clockwise extraction: [40, 10, 20, 30]
                       TL   TR  BR   BL

k_eff = 1 % 4 = 1
Rotated:  [10, 20, 30, 40]   (shift left by 1)

Place back:
  TL=(0,0) ← 10    TR=(0,1) ← 20
  BR=(1,1) ← 30    BL=(1,0) ← 40

Result: [[10,20],[40,30]] ✓
```

---

## Complexity Analysis

| | Complexity | Reason |
|---|---|---|
| **Time** | `O(m × n)` | Every cell extracted once, rotated, and placed back |
| **Space** | `O(m × n)` | Storing all elements of the largest layer (at most m×n/2) |

---

## Layer Size Formula

For layer `l` in an `m × n` grid:

```
perimeter = 2 × (m - 2l) + 2 × (n - 2l) - 4
          = 2m + 2n - 8l - 4

Layer 0 in 4×4:  2(4) + 2(4) - 0 - 4  = 12 cells
Layer 1 in 4×4:  2(4) + 2(4) - 8 - 4  =  4 cells
Number of layers = min(m, n) // 2
```

---

## Key Insights

| Insight | Explanation |
|---|---|
| Flatten → rotate → restore | Reduces 2D ring rotation to a 1D list shift |
| Clockwise extraction = counter-clockwise rotation | Left-shifting a clockwise list by k is the same as k CCW rotations |
| `k % layer_size` | Eliminates redundant full rotations (k can be up to 10⁹) |
| Layers are independent | Each layer's rotation has no effect on any other |

---

## Edge Cases

| Case | Handling |
|---|---|
| `k` is a multiple of layer size | `k % L = 0`, no rotation needed (natural from modulo) |
| Single-cell "layer" | Perimeter = 1, k % 1 = 0, no change |
| `k > 10⁸` | Always reduced by `k % L` before any shifting |

---

## Related Problems

| Problem | Similarity |
|---|---|
| [48. Rotate Image](https://leetcode.com/problems/rotate-image/) | In-place 90° matrix rotation |
| [1861. Rotating the Box](https://leetcode.com/problems/rotating-the-box/) | Layer/row manipulation with gravity |
| [54. Spiral Matrix](https://leetcode.com/problems/spiral-matrix/) | Same clockwise traversal pattern to extract a spiral |
| [59. Spiral Matrix II](https://leetcode.com/problems/spiral-matrix-ii/) | Filling a matrix in spiral/clockwise order |
