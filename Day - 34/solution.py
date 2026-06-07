from typing import List, Optional

# NOTE FOR LEETCODE SUBMISSION:
# LeetCode already defines `TreeNode` in its runtime, so DO NOT include the
# class definition below when you submit — redefining it shadows LeetCode's
# version and the judge's serializer will reject your returned node with:
#   "TypeError: <TreeNode object> is not valid value for the expected return type"
#
# For LOCAL testing there is no built-in TreeNode, so we define one here.
# When pasting into LeetCode, keep ONLY the Solution class.


# Definition for a binary tree node.
class TreeNode:
    def __init__(self, val=0, left=None, right=None):
        self.val = val
        self.left = left
        self.right = right


class Solution:
    def createBinaryTree(self, descriptions: List[List[int]]) -> Optional[TreeNode]:
        # Build the tree by value:
        #   • `nodes`    maps each value → its single, reused TreeNode.
        #   • `children` records every value that appears as someone's child.
        # The root is the unique value that is NEVER a child.
        nodes = {}
        children = set()

        def get(val: int) -> TreeNode:
            # Lazily create a node the first time we see a value (as parent OR
            # child) so the same physical node is reused wherever it appears.
            if val not in nodes:
                nodes[val] = TreeNode(val)
            return nodes[val]

        for parent, child, is_left in descriptions:
            p, c = get(parent), get(child)
            if is_left == 1:
                p.left = c          # child is the LEFT child
            else:
                p.right = c         # child is the RIGHT child
            children.add(child)

        # Exactly one node has no parent → its value isn't in `children`.
        for val, node in nodes.items():
            if val not in children:
                return node

        return None                 # unreachable for valid input


# ── Helpers for local testing (level-order serialization) ────────────────────
def serialize(root: Optional[TreeNode]) -> List:
    """BFS level-order with trailing None trimmed — matches LeetCode style."""
    from collections import deque
    if not root:
        return []
    out, q = [], deque([root])
    while q:
        node = q.popleft()
        if node:
            out.append(node.val)
            q.append(node.left)
            q.append(node.right)
        else:
            out.append(None)
    while out and out[-1] is None:
        out.pop()
    return out


# ── Quick tests ──────────────────────────────────────────────────────────────
if __name__ == "__main__":
    sol = Solution()

    r1 = sol.createBinaryTree([[20, 15, 1], [20, 17, 0], [50, 20, 1], [50, 80, 0], [80, 19, 1]])
    print(serialize(r1))    # [50, 20, 80, 15, 17, 19]

    r2 = sol.createBinaryTree([[1, 2, 1], [2, 3, 0], [3, 4, 1]])
    print(serialize(r2))    # [1, 2, None, None, 3, 4]

    r3 = sol.createBinaryTree([[1, 2, 1]])
    print(serialize(r3))    # [1, 2]

    r4 = sol.createBinaryTree([[1, 2, 0]])
    print(serialize(r4))    # [1, None, 2]

    # Root appears in the MIDDLE of the list, not as the first parent.
    r5 = sol.createBinaryTree([[85, 82, 1], [74, 85, 1]])
    print(serialize(r5))    # [74, 85, None, 82]   → root is 74
