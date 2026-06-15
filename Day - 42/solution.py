class ListNode:
    def __init__(self, val=0, next=None):
        self.val = val
        self.next = next


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


# ── Local helpers ────────────────
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
