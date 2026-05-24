class Solution:
    def maximumJumps(self, nums: List[int], target: int) -> int:
        n = len(nums)
        dp = [-1] * n
        dp[0] = 0  
        for j in range(1, n):
            for i in range(j):
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
