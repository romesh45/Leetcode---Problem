from functools import lru_cache
from typing import List


class Solution:
    def stoneGameII(self, piles: List[int]) -> int:
        n = len(piles)

        suffix_sum = [0] * (n + 1)
        for i in range(n - 1, -1, -1):
            suffix_sum[i] = suffix_sum[i + 1] + piles[i]

        @lru_cache(maxsize=None)
        def dp(i: int, m: int) -> int:
            if i >= n:
                return 0
            if i + 2 * m >= n:
                return suffix_sum[i]

            best = 0
            remaining_total = suffix_sum[i]
            for x in range(1, 2 * m + 1):
                if i + x > n:
                    break
                opponent = dp(i + x, max(m, x))
                candidate = remaining_total - opponent
                if candidate > best:
                    best = candidate
            return best

        result = dp(0, 1)
        dp.cache_clear()
        return result


if __name__ == "__main__":
    sol = Solution()

    # Example 1
    piles1 = [2, 7, 9, 4, 4]
    print(sol.stoneGameII(piles1))  # Expected: 10

    # Example 2
    piles2 = [1, 2, 3, 4, 5, 100]
    print(sol.stoneGameII(piles2))  # Expected: 104

    # Edge case: single pile
    piles3 = [10]
    print(sol.stoneGameII(piles3))  # Expected: 10

    # Edge case: two piles
    piles4 = [1, 100]
    print(sol.stoneGameII(piles4))  # Expected: 101

    # Larger random-ish case
    piles5 = [1] * 100
    print(sol.stoneGameII(piles5))  # Expected: 50
