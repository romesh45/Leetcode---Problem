# Day 40 — LeetCode Challenge

## 2130. Maximum Twin Sum of a Linked List

| Field | Details |
|---|---|
| **Difficulty** | Medium |
| **Topics** | Linked List · Two Pointers · In-Place Reversal · Fast & Slow Pointers |
| **LeetCode Link** | [2130. Maximum Twin Sum of a Linked List](https://leetcode.com/problems/maximum-twin-sum-of-a-linked-list/) |

---

## Problem Statement

In a linked list of **even** size `n`, the `i`-th node (0-indexed) is the **twin** of the `(n − 1 − i)`-th node, for `0 <= i <= n/2 − 1`. The **twin sum** is the sum of a node and its twin.

Return the **maximum** twin sum.

---

## Examples

### Example 1

```
Input:  head = [5,4,2,1]
Output: 6
```

Twins: `5+1 = 6`, `4+2 = 6` → max `6`.

### Example 2

```
Input:  head = [4,2,2,3]
Output: 7
```

Twins: `4+3 = 7`, `2+2 = 4` → max `7`.

### Example 3

```
Input:  head = [1,100000]
Output: 100001
```

Single twin pair → `100001`.

---

## Constraints

- Even number of nodes, `2 <= n <= 10⁵`
- `1 <= Node.val <= 10⁵`

---

## ⚠️ Submission Note — Don't Redefine `ListNode`

Same gotcha as [Day 34's `TreeNode`](https://leetcode.com/problems/create-binary-tree-from-descriptions/): LeetCode pre-defines `ListNode`. If you paste your own `class ListNode`, you're fine for *input* (the judge builds the list), but it's cleanest to rely on the provided one. This repo's `solution.py` defines `ListNode` **only so it runs locally** — strip it (or keep it commented) when submitting.

---

## Intuition

### Twins are a mirror across the middle

Node `i` pairs with node `n − 1 − i` — the list folded in half. The naive way is to dump all values into an array and pair `vals[i] + vals[n-1-i]`. That's O(n) time but **O(n) space**.

### Doing it in O(1) space

We can avoid the array with the classic linked-list maneuver:

1. **Find the middle** with fast & slow pointers — `slow` advances 1, `fast` advances 2, so when `fast` reaches the end, `slow` sits at the start of the second half.
2. **Reverse the second half** in place.
3. **Walk both halves together** — the first-half pointer goes forward (`0, 1, 2, …`) and the reversed second-half pointer effectively goes backward through the original (`n-1, n-2, …`). Step `i` sums node `i` with node `n-1-i`: exactly the twins.

Only `n/2` pairs exist, so the two pointers meet in the middle after `n/2` steps.

### Why the reversal aligns the twins

Before reversal, the second half is `node[n/2], node[n/2+1], …, node[n-1]`. After reversal it becomes `node[n-1], node[n-2], …, node[n/2]`. Walking it from its new head gives `n-1, n-2, …` — the mirror order. Pairing with the forward first half `0, 1, …` yields twin pairs directly.

---

## Algorithm

```
slow, fast = head, head
while fast and fast.next:        # find middle
    slow = slow.next
    fast = fast.next.next

prev = None                      # reverse second half
while slow:
    slow.next, prev, slow = prev, slow, slow.next

best = 0                         # sum twins in lockstep
first, second = head, prev
while second:
    best = max(best, first.val + second.val)
    first, second = first.next, second.next
return best
```

---

## Solution

```python
# Definition for singly-linked list.
# class ListNode:
#     def __init__(self, val=0, next=None):
#         self.val = val
#         self.next = next
from typing import Optional


class Solution:
    def pairSum(self, head: Optional[ListNode]) -> int:
        slow, fast = head, head
        while fast and fast.next:
            slow = slow.next
            fast = fast.next.next

        prev = None
        while slow:
            slow.next, prev, slow = prev, slow, slow.next

        best = 0
        first, second = head, prev
        while second:
            best = max(best, first.val + second.val)
            first = first.next
            second = second.next
        return best
```

> `ListNode` is commented out — LeetCode provides it. The local file defines it so the tests run.

---

## Complexity Analysis

| | Complexity | Reason |
|---|---|---|
| **Time** | **O(n)** | Find middle O(n/2) + reverse O(n/2) + pair O(n/2) |
| **Space** | **O(1)** | In-place reversal; no auxiliary array |

---

## Full Trace — Example 1: `head = [5, 4, 2, 1]`

**1) Find middle** (`n = 4`):

| step | slow | fast |
|:-:|:-:|:-:|
| start | 5 | 5 |
| 1 | 4 | 2 |
| 2 | 2 | None (fast.next.next) |

`slow` stops at node `2` (index 2) — start of the second half `[2, 1]`.

**2) Reverse second half** `[2, 1]` → `[1, 2]`; `prev` heads it.

**3) Pair twins:**

| step | first | second | sum | best |
|:-:|:-:|:-:|:-:|:-:|
| 1 | 5 | 1 | 6 | 6 |
| 2 | 4 | 2 | 6 | 6 |

**Answer: 6** ✓

---

## Why Fast & Slow Finds the Split Cleanly

For even `n`, the loop `while fast and fast.next` runs exactly `n/2` times:

- `fast` moves `2` per step, so after `n/2` steps it has moved `n` nodes → off the end (`None`).
- `slow` moves `1` per step → lands at index `n/2`, the first node of the second half.

This split is exact for even lengths (guaranteed here), so the reversed second half has exactly `n/2` nodes — perfectly matching the first half for pairing.

---

## Alternative — Array Dump (O(n) Space)

```python
def pairSum(self, head):
    vals = []
    while head:
        vals.append(head.val)
        head = head.next
    n = len(vals)
    return max(vals[i] + vals[n - 1 - i] for i in range(n // 2))
```

Dead simple and O(n) time — but O(n) space. Use it when readability trumps memory; use the reverse-in-place version when you want the optimal O(1)-space answer (and to show you know the linked-list toolkit).

---

## Key Insights

| Insight | Explanation |
|---|---|
| **Twins = mirror across the middle** | Node `i` pairs with `n-1-i`. |
| **Reverse-half aligns the mirror** | After reversal, walking the second half backward matches the first half forward. |
| **Fast & slow splits an even list exactly** | `slow` lands at index `n/2` in `n/2` steps. |
| **O(1) space via in-place reversal** | No array needed; the list itself is the workspace. |
| **Don't redefine `ListNode` on LeetCode** | The judge supplies it (same as `TreeNode` on Day 34). |

---

## Edge Cases

| Case | Behavior |
|---|---|
| Two nodes (`[1, 100000]`) | Single twin pair → their sum |
| All equal values | Every twin sum identical → that value × 2 |
| Strictly increasing (`[1..6]`) | All twin sums equal (`1+6 = 2+5 = 3+4`) |
| Max in outer pair | Captured at the first pairing step |
| Max in inner pair | Captured at a later step; `max` keeps the best |

---

## Approach Tags

`Fast & Slow Pointers` · `In-Place Reversal` · `Two-Pointer Pairing` · `O(1) Space`

---

*Day 40 of the LeetCode Daily Challenge*
