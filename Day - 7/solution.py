# 2770. Maximum Number of Jumps to Reach the Last Index
# https://leetcode.com/problems/maximum-number-of-jumps-to-reach-the-last-index/
# Difficulty: Medium | Time: O(n^2) | Space: O(n)

from typing import List

class Solution:
    def maximumJumps(self, nums: List[int], target: int) -> int:
        n = len(nums)

        # dp[i] = max jumps to reach index i (-1 means unreachable)
        dp = [-1] * n
        dp[0] = 0  # start at index 0, 0 jumps needed

        for j in range(1, n):
            for i in range(j):
                # Can we jump from i to j?
                if dp[i] != -1 and abs(nums[j] - nums[i]) <= target:
                    dp[j] = max(dp[j], dp[i] + 1)

        return dp[n - 1]


# ── Tests ────────────────────────────────────────────────────────────────────

if __name__ == "__main__":
    sol = Solution()

    test_cases = [
        ([1, 3, 6, 4, 1, 2], 2,  3),
        ([1, 3, 6, 4, 1, 2], 3,  5),
        ([1, 3, 6, 4, 1, 2], 0, -1),
        ([1, 2],             1,  1),
        ([0, 1000000000],    0, -1),
    ]

    all_pass = True
    for nums, target, expected in test_cases:
        result = sol.maximumJumps(nums, target)
        status = "PASS" if result == expected else "FAIL"
        if status == "FAIL":
            all_pass = False
        print(f"[{status}] nums={nums}, target={target} → {result}  (expected {expected})")

    print("\nAll tests passed ✓" if all_pass else "\nSome tests failed ✗")
