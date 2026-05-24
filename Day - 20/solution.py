import sys
from functools import lru_cache
from typing import List


class Solution:
    def maxJumps(self, arr: List[int], d: int) -> int:
        n = len(arr)

        # Strictly-decreasing chains can be up to n long; bump recursion limit
        # to be safe for n up to 1000.
        sys.setrecursionlimit(10_000)

        @lru_cache(maxsize=None)
        def dfs(i: int) -> int:
            """Best number of indices reachable starting at i (counts i itself)."""
            best = 1

            # ── Walk RIGHT ────────────────────────────────────────────────
            # Break as soon as we hit any arr[j] >= arr[i]:
            #   • we can't land on it (strict > required),
            #   • we can't land past it either — the jump rule needs every
            #     "between" index k to satisfy arr[i] > arr[k], and this one
            #     doesn't, so it blocks every further j on the right.
            for j in range(i + 1, min(i + d, n - 1) + 1):
                if arr[j] >= arr[i]:
                    break
                best = max(best, 1 + dfs(j))

            # ── Walk LEFT ─────────────────────────────────────────────────
            # Symmetric: same break logic, just iterating the other direction.
            for j in range(i - 1, max(i - d, 0) - 1, -1):
                if arr[j] >= arr[i]:
                    break
                best = max(best, 1 + dfs(j))

            return best

        # Try every starting index; take the max.
        return max(dfs(i) for i in range(n))


# ── Quick tests ──────────────────────────────────────────────────────────────
if __name__ == "__main__":
    sol = Solution()
    print(sol.maxJumps([6, 4, 14, 6, 8, 13, 9, 7, 10, 6, 12], 2))   # 4
    print(sol.maxJumps([3, 3, 3, 3, 3], 3))                          # 1
    print(sol.maxJumps([7, 6, 5, 4, 3, 2, 1], 1))                    # 7
    print(sol.maxJumps([7, 1, 7, 1, 7, 1], 2))                       # 2
    print(sol.maxJumps([66], 1))                                     # 1
