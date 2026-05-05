# 61. Rotate List

**Difficulty:** Medium  
**Topic Tags:** Linked List, Two Pointers  
**LeetCode Link:** [Problem 61](https://leetcode.com/problems/rotate-list/)

---

## Problem Statement

Given the `head` of a linked list, rotate the list to the right by `k` places.

**Example 1:**
```
Input:  head = [1, 2, 3, 4, 5],  k = 2
Output: [4, 5, 1, 2, 3]
```

**Example 2:**
```
Input:  head = [0, 1, 2],  k = 4
Output: [2, 0, 1]
```

**Constraints:**
- Number of nodes: `[0, 500]`
- `-100 <= Node.val <= 100`
- `0 <= k <= 2 * 10⁹`

---

## Intuition

Rotating right by `k` is the same as **taking the last `k` nodes and moving them to the front**.

Instead of physically shifting nodes, we use a smarter trick:

1. Connect the tail back to the head → makes a **circular list**
2. Find the **new tail** at position `length − k − 1`
3. **Break the circle** there → done

> Rotating `[1→2→3→4→5]` by 2 = taking `[4→5]` from the back and prepending → `[4→5→1→2→3]`

---

## Approach — Circular Link & Break

### Steps

```
1. Edge case check   →  empty list, single node, or k = 0? return head
2. Find length       →  traverse to get length and reach the tail node
3. Reduce k          →  k = k % length  (handles k larger than list size)
4. Early exit        →  if k == 0 after mod, no rotation needed
5. Make circular     →  tail.next = head
6. Find new tail     →  walk (length − k − 1) steps from head
7. Break circle      →  new_head = new_tail.next  |  new_tail.next = None
8. Return new_head
```

### Visual Walkthrough (`k = 2`)

```
Original:     1 → 2 → 3 → 4 → 5 → None

Step 1: Find length = 5, tail = node(5)

Step 2: k = 2 % 5 = 2

Step 3: Make circular
          1 → 2 → 3 → 4 → 5
          ↑_________________↑

Step 4: New tail index = 5 - 2 - 1 = 2  →  node(3)
        New head                         →  node(4)

Step 5: Break circle at node(3)
          node(3).next = None

Result:   4 → 5 → 1 → 2 → 3 → None  ✓
```

---

## Solution

```python
class Solution:
    def rotateRight(self, head: Optional[ListNode], k: int) -> Optional[ListNode]:
        # Edge case: empty list, single node, or no rotation
        if not head or not head.next or k == 0:
            return head

        # Step 1: Find length and tail
        length = 1
        tail = head
        while tail.next:
            tail = tail.next
            length += 1

        # Step 2: Effective rotation (handles k > length)
        k = k % length
        if k == 0:
            return head

        # Step 3: Make circular
        tail.next = head

        # Step 4: Find new tail → (length - k - 1) steps from head
        new_tail = head
        for _ in range(length - k - 1):
            new_tail = new_tail.next

        # Step 5: Break the circle
        new_head = new_tail.next
        new_tail.next = None

        return new_head
```

---

## Complexity Analysis

| | Complexity | Reason |
|---|---|---|
| **Time** | `O(n)` | Two passes at most — one to find length, one to find new tail |
| **Space** | `O(1)` | Only pointer manipulation, no extra data structures |

---

## Key Insights

| Insight | Explanation |
|---|---|
| `k % length` | Eliminates redundant full rotations. Rotating by `length` = no change |
| Circular trick | Avoids the need to physically detach and reattach nodes |
| New tail position | Always at index `length − k − 1` from head (0-indexed) |

---

## Edge Cases Handled

| Case | Handling |
|---|---|
| `head = None` | Return `None` immediately |
| Single node | Return `head` immediately |
| `k = 0` | Return `head` immediately |
| `k > length` | `k = k % length` reduces it |
| `k = length` (multiple) | `k % length = 0`, return `head` early |

---

## Related Problems

| Problem | Similarity |
|---|---|
| [206. Reverse Linked List](https://leetcode.com/problems/reverse-linked-list/) | Linked list pointer manipulation |
| [141. Linked List Cycle](https://leetcode.com/problems/linked-list-cycle/) | Circular linked list detection |
| [189. Rotate Array](https://leetcode.com/problems/rotate-array/) | Same rotation concept on arrays |
