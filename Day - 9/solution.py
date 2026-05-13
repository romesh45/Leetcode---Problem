from typing import List


class Solution:
    def minMoves(self, nums: List[int], limit: int) -> int:
        n = len(nums)

        # Difference array over all possible target sums T in [2, 2*limit].
        # diff[T] holds the *delta* in cost at T; a prefix sum recovers
        # the actual total cost to make every pair sum to T.
        diff = [0] * (2 * limit + 2)

        for i in range(n // 2):
            a, b = nums[i], nums[n - 1 - i]
            lo, hi = min(a, b), max(a, b)

            # ── Default contribution for this pair ─────────────────────────
            # For *any* target T, the absolute worst case is 2 moves
            # (change both elements). Stamp +2 across the whole valid range.
            diff[2]              += 2
            diff[2 * limit + 1]  -= 2

            # ── 1-move window ──────────────────────────────────────────────
            # If we keep one element and change the other, the reachable
            # sums form the interval [1 + lo, limit + hi].
            # Inside this window cost drops from 2 → 1, so subtract 1.
            diff[1 + lo]         -= 1
            diff[limit + hi + 1] += 1

            # ── 0-move single point ────────────────────────────────────────
            # T == a + b already works for this pair → cost is 0, not 1.
            # Subtract 1 more at exactly that point.
            diff[a + b]          -= 1
            diff[a + b + 1]      += 1

        # Sweep prefix sum and track the minimum total cost over all targets.
        ans = float("inf")
        cur = 0
        for T in range(2, 2 * limit + 1):
            cur += diff[T]
            if cur < ans:
                ans = cur

        return ans


# ── Quick tests ──────────────────────────────────────────────────────────────
if __name__ == "__main__":
    sol = Solution()
    print(sol.minMoves([1, 2, 4, 3], 4))           # 1
    print(sol.minMoves([1, 2, 2, 1], 2))           # 2
    print(sol.minMoves([1, 2, 1, 2], 2))           # 0
    print(sol.minMoves([1, 1, 1, 1], 3))           # 0
    print(sol.minMoves([1, 2, 3, 4, 5, 6], 6))     # 0 (all pairs already sum to 7)
