# Day 34 — LeetCode Challenge

## 2196. Create Binary Tree From Descriptions

| Field | Details |
|---|---|
| **Difficulty** | Medium |
| **Topics** | Hash Table · Tree · Binary Tree · Graph Construction |
| **LeetCode Link** | [2196. Create Binary Tree From Descriptions](https://leetcode.com/problems/create-binary-tree-from-descriptions/) |

---

## Problem Statement

You're given a 2D array `descriptions` where `descriptions[i] = [parentᵢ, childᵢ, isLeftᵢ]` means `parentᵢ` is the parent of `childᵢ` in a binary tree of **unique** values:

- `isLeftᵢ == 1` → `childᵢ` is the **left** child of `parentᵢ`.
- `isLeftᵢ == 0` → `childᵢ` is the **right** child of `parentᵢ`.

Construct the binary tree and return its **root**. The input is guaranteed to describe a valid binary tree.

---

## Examples

### Example 1

```
Input:  descriptions = [[20,15,1],[20,17,0],[50,20,1],[50,80,0],[80,19,1]]
Output: [50,20,80,15,17,19]
```

Root is `50` (it has no parent).

### Example 2

```
Input:  descriptions = [[1,2,1],[2,3,0],[3,4,1]]
Output: [1,2,null,null,3,4]
```

Root is `1`.

---

## Constraints

- `1 <= descriptions.length <= 10⁴`
- `descriptions[i].length == 3`
- `1 <= parentᵢ, childᵢ <= 10⁵`
- `0 <= isLeftᵢ <= 1`
- The described binary tree is valid.

---

## ⚠️ Common Submission Error — Redefining `TreeNode`

**If you include your own `class TreeNode` in the submission, you'll get:**

```
TypeError: <__main__.TreeNode object> is not valid value for the expected return type TreeNode
Exception: Type <class '__main__.TreeNode'> cannot be serialized
```

**Why:** LeetCode pre-defines `TreeNode` in its runtime and its result serializer only recognizes *that* class. Redefining `TreeNode` in your file creates a **different** class that shadows it — so the node you return is an instance the serializer can't handle.

**Fix:** Do **not** define `TreeNode` in your submission. Use LeetCode's built-in one (it appears commented out at the top of the template). Submit only the `Solution` class.

> In this repo's `solution.py`, a `TreeNode` *is* defined — but **only so the file runs locally**, where no built-in `TreeNode` exists. The header comment flags this clearly. When pasting into LeetCode, strip the class.

---

## Intuition

### Two sub-problems

1. **Wire up all parent → child links.** Values are unique, so we can identify each node by its value.
2. **Find the root.** In a valid binary tree, exactly one node has **no parent**.

### Create nodes lazily, by value

Maintain a `dict` mapping `value → TreeNode`. A `get(val)` helper creates the node the first time a value is seen — whether it shows up as a parent or as a child — and returns the existing node afterward. This guarantees **one physical node per value**, reused everywhere that value appears across the descriptions.

Without this, you'd risk creating duplicate nodes for the same value (e.g. a node that's a child in one description and a parent in another).

### Find the root via a "children" set

Record every value that ever appears as a **child**. After processing all descriptions, scan the node values: the one **not** in the children set is the root — it's never anyone's child, so it has no parent.

Since the tree is valid, this root is **unique**.

---

## Algorithm

```
nodes    = {}            # value -> TreeNode
children = set()         # values seen as a child

get(val):
    if val not in nodes: nodes[val] = TreeNode(val)
    return nodes[val]

for [parent, child, isLeft] in descriptions:
    p, c = get(parent), get(child)
    if isLeft == 1: p.left  = c
    else:           p.right = c
    children.add(child)

for val in nodes:
    if val not in children:
        return nodes[val]      # the root
```

---

## Solution (LeetCode-Submittable)

```python
# Definition for a binary tree node.
# class TreeNode:
#     def __init__(self, val=0, left=None, right=None):
#         self.val = val
#         self.left = left
#         self.right = right
from typing import List, Optional


class Solution:
    def createBinaryTree(self, descriptions: List[List[int]]) -> Optional[TreeNode]:
        nodes = {}
        children = set()

        def get(val):
            if val not in nodes:
                nodes[val] = TreeNode(val)
            return nodes[val]

        for parent, child, is_left in descriptions:
            p, c = get(parent), get(child)
            if is_left == 1:
                p.left = c
            else:
                p.right = c
            children.add(child)

        for val, node in nodes.items():
            if val not in children:
                return node

        return None
```

> Note `TreeNode` is **not** defined here — it's commented out because LeetCode supplies it. The repo's local file defines it so the tests run on your machine.

---

## Complexity Analysis

Let `n = len(descriptions)`.

| | Complexity | Reason |
|---|---|---|
| **Time** | **O(n)** | One pass to wire edges + one pass over the node map to find the root |
| **Space** | **O(n)** | The node map + children set (up to ~2n distinct values) |

---

## Full Trace — Example 1: `[[20,15,1],[20,17,0],[50,20,1],[50,80,0],[80,19,1]]`

| Description | Action | `children` after |
|---|---|---|
| `[20,15,1]` | create 20, 15; `20.left = 15` | `{15}` |
| `[20,17,0]` | create 17; `20.right = 17` | `{15, 17}` |
| `[50,20,1]` | create 50; `50.left = 20` | `{15, 17, 20}` |
| `[50,80,0]` | create 80; `50.right = 80` | `{15, 17, 20, 80}` |
| `[80,19,1]` | create 19; `80.left = 19` | `{15, 17, 20, 80, 19}` |

**Node values:** `{20, 15, 17, 50, 80, 19}`.
**Root search:** which value is *not* in `children`? → `50`. ✓

Resulting tree:
```
            50
           /  \
         20    80
        /  \   /
      15   17 19
```
Level-order: `[50, 20, 80, 15, 17, 19]` ✓

---

## Why the Root Can't Be "the First Parent"

A tempting shortcut is "the root is `descriptions[0][0]`." This is **wrong** — descriptions can list edges in any order. Consider:

```
descriptions = [[85,82,1], [74,85,1]]
```

Here `85` is the first parent, but `85` is itself a child of `74`. The real root is `74`. The "not-a-child" set correctly identifies it; the "first parent" heuristic would fail.

---

## Alternative — Track Parent Status with a Boolean Map

Instead of a set, some solutions store `hasParent[val] = True/False`. Equivalent logic, slightly more bookkeeping:

```python
has_parent = {}
def touch(v):
    if v not in nodes: nodes[v] = TreeNode(v)
    has_parent.setdefault(v, False)

for parent, child, is_left in descriptions:
    touch(parent); touch(child)
    ...
    has_parent[child] = True

return next(nodes[v] for v in nodes if not has_parent[v])
```

The `children` set is leaner — there's no need to record `False` for non-children.

---

## Key Insights

| Insight | Explanation |
|---|---|
| **Index nodes by unique value** | A `value → TreeNode` map lets every description reference the same physical node. |
| **Lazy creation via `get`** | Handles values appearing as both parent and child without duplication. |
| **Root = the value never seen as a child** | Valid tree ⇒ exactly one node has no parent. |
| **Don't redefine `TreeNode` on LeetCode** | The judge serializes its own class; a shadow class breaks the return. |
| **Edge order is arbitrary** | The root isn't necessarily the first parent — use the children set. |

---

## Edge Cases

| Case | Behavior |
|---|---|
| Single edge `[[1,2,1]]` | Root `1`, left child `2` → `[1, 2]` |
| Single edge `[[1,2,0]]` | Root `1`, right child `2` → `[1, null, 2]` |
| Root listed mid-array | Children set still finds it correctly |
| Deep skewed chain | Linear wiring; root is the topmost value |
| Maximum `10⁴` descriptions | O(n) handles it easily |

---

## Approach Tags

`Hash Map` · `Lazy Node Creation` · `Root via Indegree` · `Binary Tree Construction`

---

*Day 34 of the LeetCode Daily Challenge*
