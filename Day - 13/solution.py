from collections import deque
from typing import List


class Solution:
    def canReach(self, arr: List[int], start: int) -> bool:
        # BFS over array indices. Treat each index i as a graph node with
        # at most 2 outgoing edges: i + arr[i] and i - arr[i] (if in bounds).
        # A `visited` array bounds the total work to O(n).
        n = len(arr)
        visited = [False] * n
        queue = deque([start])
        visited[start] = True

        while queue:
            i = queue.popleft()

            # Goal check on dequeue — we found a zero, so a path exists.
            if arr[i] == 0:
                return True

            # Try both jump directions. Bounds-check before enqueuing.
            for nxt in (i + arr[i], i - arr[i]):
                if 0 <= nxt < n and not visited[nxt]:
                    visited[nxt] = True
                    queue.append(nxt)

        # Queue drained without ever landing on a zero → unreachable.
        return False


# ── Quick tests ──────────────────────────────────────────────────────────────
if __name__ == "__main__":
    sol = Solution()
    print(sol.canReach([4, 2, 3, 0, 3, 1, 2], 5))   # True
    print(sol.canReach([4, 2, 3, 0, 3, 1, 2], 0))   # True
    print(sol.canReach([3, 0, 2, 1, 2], 2))         # False
    print(sol.canReach([0], 0))                     # True
    print(sol.canReach([1, 1, 1, 1, 1, 0], 0))      # True (walks 0→1→2→3→4→5)
    print(sol.canReach([2, 0, 1], 1))               # True (already at zero)
    print(sol.canReach([1, 0], 1))                  # True
