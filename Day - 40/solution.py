class ListNode:
    def __init__(self, val=0, next=None):
        self.val = val
        self.next = next
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


# ── Local helpers ───────────────────────────
def build(values):
    dummy = ListNode()
    cur = dummy
    for v in values:
        cur.next = ListNode(v)
        cur = cur.next
    return dummy.next


# ── Quick tests ──────────────────────────────
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
