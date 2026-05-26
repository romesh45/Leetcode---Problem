from collections import deque


class Solution:
    def canReach(self, s: str, minJump: int, maxJump: int) -> bool:
        n = len(s)

        # The destination index n-1 must itself be a '0' — otherwise no path
        # can ever land there.
        if s[-1] != '0':
            return False

        # ── BFS with a sliding frontier pointer ───────────────────────────────
        # From index i, the reachable window is [i + minJump, i + maxJump].
        # Naively enumerating each window is O(n * maxJump), worst-case ~10^10
        # on the constraint limits → TLE.
        #
        # Key observation: BFS dequeues indices in non-decreasing order, so the
        # window starts ALSO grow over time. Track `farthest` = the largest
        # index we've ever scanned. The next effective scan starts at
        #     lo = max(i + minJump, farthest + 1)
        # which guarantees every index in s is visited at most once across the
        # whole BFS — total work O(n).
        queue = deque([0])
        farthest = 0   # the rightmost index already considered

        while queue:
            i = queue.popleft()

            lo = max(i + minJump, farthest + 1)
            hi = min(i + maxJump, n - 1)

            for j in range(lo, hi + 1):
                if s[j] == '0':
                    # Early-exit: BFS layer ordering ⇒ first time we touch
                    # n-1 is via a shortest path; we just need ANY path.
                    if j == n - 1:
                        return True
                    queue.append(j)

            # Mark everything up to `hi` as "already scanned" so no future
            # dequeue re-examines this range.
            farthest = max(farthest, hi)

        return False


# ── Quick tests ──────────────────────────────────────────────────────────────
if __name__ == "__main__":
    sol = Solution()
    print(sol.canReach("011010", 2, 3))                       # True
    print(sol.canReach("01101110", 2, 3))                     # False
    print(sol.canReach("00", 1, 1))                           # True
    print(sol.canReach("01", 1, 1))                           # False (s[-1] is '1')
    print(sol.canReach("0000000000", 1, 1))                   # True
    print(sol.canReach("0" + "1" * 8 + "0", 1, 2))            # False (a wall of 1's blocks)
    print(sol.canReach("0" * 100000, 1, 5))                   # True
