from typing import Optional

# NOTE FOR LEETCODE SUBMISSION:
# LeetCode already defines `ListNode` in its runtime — do NOT include the class
# definition below when you submit (redefining it shadows LeetCode's version).
# It is defined here ONLY so this file runs locally. Submit just the Solution.


# Definition for singly-linked list.
class ListNode:
    def __init__(self, val=0, next=None):
        self.val = val
        self.next = next


class Solution:
    def pairSum(self, head: Optional[ListNode]) -> int:
        # Twin of node i is node n-1-i (mirror across the middle).
        # O(1)-space plan: find the middle (slow/fast), reverse the second
        # half, then walk both halves in lockstep summing twins.

        # 1) slow → start of second half; fast → end.
        slow, fast = head, head
        while fast and fast.next:
            slow = slow.next
            fast = fast.next.next

        # 2) Reverse the second half starting at slow.
        prev = None
        while slow:
            slow.next, prev, slow = prev, slow, slow.next
        # `prev` now heads the reversed second half.

        # 3) Walk first half (head, forward) and reversed second half (prev,
        #    i.e. backward through original) together. Step i pairs node i with
        #    node n-1-i — exactly the twins. n/2 steps; pointers meet mid-list.
        best = 0
        first, second = head, prev
        while second:
            best = max(best, first.val + second.val)
            first = first.next
            second = second.next

        return best


# ── Local helpers ────────────────────────────────────────────────────────────
def build(values):
    dummy = ListNode()
    cur = dummy
    for v in values:
        cur.next = ListNode(v)
        cur = cur.next
    return dummy.next


# ── Quick tests ──────────────────────────────────────────────────────────────
if __name__ == "__main__":
    sol = Solution()
    print(sol.pairSum(build([5, 4, 2, 1])))        # 6
    print(sol.pairSum(build([4, 2, 2, 3])))        # 7
    print(sol.pairSum(build([1, 100000])))         # 100001
    print(sol.pairSum(build([1, 2, 3, 4, 5, 6])))  # 7  (1+6, 2+5, 3+4 all = 7)
    print(sol.pairSum(build([10, 1, 1, 10])))      # 20 (10+10)

    # Cross-check against the simple O(n)-space approach on random even lists.
    import random
    def brute(values):
        n = len(values)
        return max(values[i] + values[n - 1 - i] for i in range(n // 2))
    for _ in range(1000):
        m = random.randint(1, 50) * 2
        vals = [random.randint(1, 100000) for _ in range(m)]
        assert sol.pairSum(build(vals)) == brute(vals)
    print("randomized cross-check passed ✓")
