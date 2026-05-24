class Solution:
    def minMoves(self, nums: List[int], limit: int) -> int:
        n = len(nums)
        diff = [0] * (2 * limit + 2)
        for i in range(n // 2):
            a, b = nums[i], nums[n - 1 - i]
            lo, hi = min(a, b), max(a, b)
            diff[2]              += 2
            diff[2 * limit + 1]  -= 2
            diff[1 + lo]         -= 1
            diff[limit + hi + 1] += 1
            diff[a + b]          -= 1
            diff[a + b + 1]      += 1
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
