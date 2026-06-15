from typing import Optional

# NOTE FOR LEETCODE SUBMISSION:
# LeetCode already defines `ListNode` — do NOT include the class below when you
# submit (redefining it shadows the judge's version). It's defined here ONLY so
# this file runs locally. Submit just the Solution class.


# Definition for singly-linked list.
class ListNode:
    def __init__(self, val=0, next=None):
        self.val = val
        self.next = next


class Solution:
    def deleteMiddle(self, head: Optional[ListNode]) -> Optional[ListNode]:
        # A single node → its middle is itself → deleting leaves an empty list.
        # Handle upfront so `prev` is guaranteed non-None at splice time.
        if not head or not head.next:
            return None

        # Fast & slow: fast moves 2, slow moves 1. The loop runs ⌊n/2⌋ times,
        # so slow advances ⌊n/2⌋ nodes → lands exactly on the middle index.
        # `prev` trails slow so we can unlink the middle from its predecessor.
        prev = None
        slow, fast = head, head
        while fast and fast.next:
            prev = slow
            slow = slow.next
            fast = fast.next.next

        # Splice out the middle node `slow`.
        prev.next = slow.next
        return head


# ── Local helpers ────────────────────────────────────────────────────────────
def build(values):
    dummy = ListNode()
    cur = dummy
    for v in values:
        cur.next = ListNode(v)
        cur = cur.next
    return dummy.next


def to_list(head):
    out = []
    while head:
        out.append(head.val)
        head = head.next
    return out


# ── Quick tests ──────────────────────────────────────────────────────────────
if __name__ == "__main__":
    sol = Solution()
    print(to_list(sol.deleteMiddle(build([1, 3, 4, 7, 1, 2, 6]))))   # [1,3,4,1,2,6]
    print(to_list(sol.deleteMiddle(build([1, 2, 3, 4]))))            # [1,2,4]
    print(to_list(sol.deleteMiddle(build([2, 1]))))                  # [2]
    print(to_list(sol.deleteMiddle(build([1]))))                     # []
    print(to_list(sol.deleteMiddle(build([1, 2, 3]))))              # [1,3]  (remove idx 1)
    print(to_list(sol.deleteMiddle(build([1, 2, 3, 4, 5]))))        # [1,2,4,5] (remove idx 2)

    # Cross-check the deleted index against the spec ⌊n/2⌋ on random lists.
    import random
    for _ in range(1000):
        m = random.randint(1, 60)
        vals = [random.randint(1, 100000) for _ in range(m)]
        mid = m // 2
        expected = vals[:mid] + vals[mid + 1:]
        assert to_list(sol.deleteMiddle(build(vals))) == expected, (vals, mid)
    print("randomized cross-check passed ✓")
