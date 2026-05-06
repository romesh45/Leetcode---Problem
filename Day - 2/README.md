# 1861. Rotating the Box

**Difficulty:** Medium  
**Topic Tags:** Array, Two Pointers, Matrix  
**LeetCode Link:** [Problem 1861](https://leetcode.com/problems/rotating-the-box/)

---

## Problem Statement

You are given an `m x n` matrix of characters `box` representing a side-view of a box. Each cell is:

- `'#'` → a stone
- `'*'` → a stationary obstacle
- `'.'` → empty

The box is **rotated 90° clockwise**, causing stones to fall **downward** due to gravity.  
Return the resulting `n x m` matrix.

**Example:**
```
Input:  ["#",".","*",".","."]
                 ↓ gravity (rightward before rotation)
After gravity:  [".",".","*","#","."]   wait — let's be precise:

Input:  [["#","#","*",".","."],
         ["#","#","*",".","."],
         ["#","#","#",".","."]]

Output (after gravity + 90° CW rotation): see below
```

---

## The Two-Step Insight

> The problem is just **two independent operations** done in order:
>
> 1. **Apply gravity** (stones slide right in the original orientation)
> 2. **Rotate the matrix** 90° clockwise

The key trick is recognizing that:
- After the 90° clockwise rotation, "downward" in the result = "rightward" in the original
- So apply gravity **first** (slide stones right per row), **then** rotate

---

## Visual Walkthrough

```
Step 1 — Original box (side view):

  [ # ][ . ][ # ][ * ][ . ][ # ]
    0    1    2    *    4    5

  Stones want to fall rightward (blocked by '*' and walls).

Step 2 — Apply gravity (two-pointer technique):

  Pointer 'empty' starts at the right end.
  Scan right → left:
  - '#' found → place it at 'empty', move empty left
  - '*' found → reset 'empty' to j-1 (new boundary)
  - '.' found → skip

  [ . ][ # ][ # ][ * ][ . ][ # ]
                  ↑
             obstacle resets pointer

  Segment 1 (right of '*'): # at 5 stays, nothing else to fall
  Segment 2 (left of '*'):  #,.,# → becomes .,#,# (two stones fall right)

Step 3 — Rotate 90° clockwise:

  Formula:  result[j][m - 1 - i] = box[i][j]

  Original is m rows × n cols → Result is n rows × m cols

  Each ROW in original becomes a COLUMN in result (read bottom to top).
```

---

## Algorithm

### Step 1: Apply Gravity (per row)

```
For each row:
  empty = n - 1          ← pointer: next free slot (rightmost)

  Scan j from n-1 → 0:
    if box[j] == '*':
        empty = j - 1    ← obstacle resets the boundary
    if box[j] == '#':
        box[j]     = '.' ← clear original position
        box[empty] = '#' ← stone falls to free slot
        empty -= 1       ← move pointer left
```

### Step 2: Rotate 90° Clockwise

```
result = n × m matrix (all '.')

For every (i, j) in original m × n:
    result[j][m - 1 - i] = box[i][j]

Original row 0, col 0  →  Result row 0, col (m-1)
Original row 0, col 1  →  Result row 1, col (m-1)
...
```

---

## Complexity Analysis

| | Complexity | Reason |
|---|---|---|
| **Time** | `O(m × n)` | Each cell visited once for gravity + once for rotation |
| **Space** | `O(n × m)` | Output matrix (rotation can't be done in-place on a different-shaped matrix) |

---

## Step-by-Step Dry Run

```
Input:
  Row 0: ["#","#","*",".","."]

━━━ Gravity (scan right → left) ━━━

  empty = 4
  j=4: '.' → skip
  j=3: '.' → skip
  j=2: '*' → reset empty = 1
  j=1: '#' → box[1]='.', box[1]='#', empty=0   (no-op, same spot)
  j=0: '#' → box[0]='.', box[0]='#', empty=-1  (no-op, same spot)

  After gravity: ["#","#","*",".","."]
  (stones were already packed against the obstacle — no change)

━━━ Rotation formula result[j][m-1-i] = box[i][j] ━━━

  Original row → becomes a column in the rotated result (read bottom to top)
```

---

## Key Insights

| Insight | Explanation |
|---|---|
| Gravity = rightward | In the side-view, after 90° CW rotation, "down" maps to "right" in original |
| Two-pointer for gravity | `empty` pointer avoids extra array — O(1) space per row |
| Obstacle is a boundary | `'*'` resets the pointer; each segment between obstacles is independent |
| Rotation formula | `result[j][m-1-i] = box[i][j]` — standard 90° CW transformation |

---

## Edge Cases Handled

| Case | Handling |
|---|---|
| No stones (`'.'` only) | Gravity loop skips, rotation runs normally |
| All stones, no obstacles | All stones pack to the right end of each row |
| Multiple obstacles | Each segment between obstacles handled independently |
| Stone already at wall/obstacle | Swaps with itself (no-op), pointer decrements |
| Single row or column | General formula works without special casing |

---

## Alternative: Rotation Formula Derivation

For a **90° clockwise** rotation of an `m × n` matrix to an `n × m` matrix:

```
(i, j)  →  (j, m - 1 - i)

Verification:
  Top-left     (0,   0) → (0,   m-1)  ✓ (goes to top-right)
  Top-right    (0, n-1) → (n-1, m-1)  ✓ (goes to bottom-right)
  Bottom-left  (m-1, 0) → (0,   0)    ✓ (goes to top-left)
```

For **90° counter-clockwise** (just in case):
```
result[n - 1 - j][i] = box[i][j]
```

---

## Related Problems

| Problem | Similarity |
|---|---|
| [48. Rotate Image](https://leetcode.com/problems/rotate-image/) | 90° CW rotation (in-place, square matrix) |
| [1260. Shift 2D Grid](https://leetcode.com/problems/shift-2d-grid/) | Matrix transformation |
| [2948. Make Lexicographically Smallest Array](https://leetcode.com/problems/make-lexicographically-smallest-array-by-applying-operations/) | Two-pointer sliding window concept |
| [61. Rotate List](https://leetcode.com/problems/rotate-list/) | Rotation on a different data structure |
