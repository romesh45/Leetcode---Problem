# Day 42 — LeetCode Challenge

## 2095. Delete the Middle Node of a Linked List

| Field | Details |
|---|---|
| **Difficulty** | Medium |
| **Topics** | Linked List · Two Pointers · Fast & Slow Pointers |
| **LeetCode Link** | [2095. Delete the Middle Node of a Linked List](https://leetcode.com/problems/delete-the-middle-node-of-a-linked-list/) |

---

## Problem Statement

Given the `head` of a linked list, delete the **middle node** and return the head of the modified list.

The middle node of a list of size `n` is the `⌊n/2⌋`-th node (0-indexed).

> For `n = 1, 2, 3, 4, 5`, the middle indices are `0, 1, 1, 2, 2`.

---

## Examples

### Example 1

```
Input:  head = [1,3,4,7,1,2,6]
Output: [1,3,4,1,2,6]
```

`n = 7`, middle index `3` (value `7`) removed.

### Example 2

```
Input:  head = [1,2,3,4]
Output: [1,2,4]
```

`n = 4`, middle index `2` (value `3`) removed.

### Example 3

```
Input:  head = [2,1]
Output: [2]
```

`n = 2`, middle index `1` removed.

---

## Constraints

- Number of nodes in `[1, 10⁵]`
- `1 <= Node.val <= 10⁵`

---

## ⚠️ Submission Note — Don't Redefine `ListNode`

Same as [Day 40](https://leetcode.com/problems/maximum-twin-sum-of-a-linked-list/) and [Day 34's `TreeNode`](https://leetcode.com/problems/create-binary-tree-from-descriptions/): LeetCode pre-defines `ListNode`. This repo's `solution.py` defines it **only for local runs** — keep it commented (or strip it) when submitting.

---

## Intuition

### Find the middle with fast & slow

The textbook way to locate a list's middle in one pass without knowing `n` upfront: two pointers from the head, `fast` moving 2 nodes per step, `slow` moving 1. When `fast` falls off the end, `slow` is at the middle.

For this problem's `⌊n/2⌋` definition, the loop condition `while fast and fast.next` makes `slow` land **exactly** on the target index — verified against the spec's table (`n=1→0, 2→1, 3→1, 4→2, 5→2`).

### Deleting needs the predecessor

In a singly-linked list you can't delete a node you only have a pointer *to* — you need its **predecessor** to reroute the link. So we carry a `prev` pointer one step behind `slow`. Once `slow` is the middle, `prev.next = slow.next` splices it out.

### The single-node trap

If the list has one node, its middle is that node, and deleting it yields an empty list. We must return `None`. Handling this **upfront** also guarantees `prev` is never `None` when we splice (the main loop runs at least once for `n ≥ 2`).

---

## Algorithm

```
if head has 0 or 1 node: return None

prev = None
slow = fast = head
while fast and fast.next:
    prev = slow
    slow = slow.next
    fast = fast.next.next

prev.next = slow.next        # unlink the middle
return head
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
    def deleteMiddle(self, head: Optional[ListNode]) -> Optional[ListNode]:
        if not head or not head.next:
            return None

        prev = None
        slow, fast = head, head
        while fast and fast.next:
            prev = slow
            slow = slow.next
            fast = fast.next.next

        prev.next = slow.next
        return head
```

> `ListNode` is commented out — LeetCode supplies it. The local file defines it so the tests run.

---

## Complexity Analysis

| | Complexity | Reason |
|---|---|---|
| **Time** | **O(n)** | Single pass; `fast` traverses the list once |
| **Space** | **O(1)** | Three pointers, no extra structure |

---

## Full Trace — Example 1: `[1, 3, 4, 7, 1, 2, 6]` (n = 7)

Indices: `0:1  1:3  2:4  3:7  4:1  5:2  6:6`

| iter | prev | slow (idx) | fast (idx) |
|:-:|:-:|:-:|:-:|
| start | None | 0 (`1`) | 0 (`1`) |
| 1 | 0 | 1 (`3`) | 2 (`4`) |
| 2 | 1 | 2 (`4`) | 4 (`1`) |
| 3 | 2 | 3 (`7`) | 6 (`6`) |
| stop | — | — | `fast.next` is None |

`slow` is at index 3 (value `7`) = ⌊7/2⌋. `prev` (index 2, value `4`) reroutes: `prev.next = slow.next` (index 4).

Result: **`[1, 3, 4, 1, 2, 6]`** ✓

---

## Full Trace — Example 3: `[2, 1]` (n = 2)

| iter | prev | slow | fast |
|:-:|:-:|:-:|:-:|
| start | None | 0 (`2`) | 0 (`2`) |
| 1 | 0 | 1 (`1`) | `fast.next.next` = None |
| stop | — | — | loop ends (`fast` is None) |

`slow` at index 1 (value `1`) = ⌊2/2⌋. `prev` (index 0) → `prev.next = slow.next = None`.

Result: **`[2]`** ✓

---

## Why the Loop Lands on ⌊n/2⌋

Each iteration advances `slow` by 1 and `fast` by 2. The loop runs until `fast` can no longer take a full 2-step (`fast` or `fast.next` is `None`):

- **Even `n`:** `fast` visits `0, 2, 4, …, n` — runs `n/2` iterations → `slow` at index `n/2`. ✓
- **Odd `n`:** `fast` visits `0, 2, …, n-1` (the last node) — runs `(n-1)/2` iterations… but with the trailing `prev` update each loop, `slow` ends at `⌊n/2⌋`. ✓

The single `while fast and fast.next` condition produces the exact `⌊n/2⌋` index the problem wants — no off-by-one adjustment needed.

---

## Alternative — Two-Pass (Count then Walk)

```python
def deleteMiddle(self, head):
    if not head or not head.next:
        return None
    n = 0
    cur = head
    while cur:
        n += 1
        cur = cur.next
    mid = n // 2
    cur = head
    for _ in range(mid - 1):     # stop at predecessor
        cur = cur.next
    cur.next = cur.next.next
    return head
```

Also O(n) time / O(1) space, but **two passes** and explicit index math. The fast/slow version finds the middle in a *single* pass — cleaner and the idiomatic choice.

---

## Key Insights

| Insight | Explanation |
|---|---|
| **Fast & slow finds the middle in one pass** | `fast` at 2×, `slow` at 1×; `slow` ends at ⌊n/2⌋. |
| **Carry `prev` to delete** | Singly-linked deletion reroutes the predecessor's `next`. |
| **Single-node guard** | `head.next is None` → return `None`; also keeps `prev` non-None later. |
| **`while fast and fast.next` gives exact ⌊n/2⌋** | No off-by-one tweak for even vs odd lengths. |
| **Don't redefine `ListNode`** | LeetCode supplies it (same as Days 34, 40). |

---

## Edge Cases

| Case | Behavior |
|---|---|
| Single node (`[1]`) | Returns `None` (empty list) |
| Two nodes (`[2,1]`) | Removes index 1 → `[2]` |
| Odd length | Removes the true center |
| Even length | Removes the right-of-center node (`⌊n/2⌋`) |
| Long list (10⁵) | Single O(n) pass handles it |

---

## Approach Tags

`Fast & Slow Pointers` · `Predecessor Tracking` · `Single-Pass Middle` · `O(1) Space`

---

*Day 42 of the LeetCode Daily Challenge*
