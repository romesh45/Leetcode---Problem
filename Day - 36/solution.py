class Solution:
    def maxTotalValue(self, nums: List[int], k: int) -> int:
        return k * (max(nums) - min(nums))


# ── Quick tests ───────────────────────────
if __name__ == "__main__":
    sol = Solution()
    print(sol.maxTotalValue([1, 3, 2], 2))          # 4
    print(sol.maxTotalValue([4, 2, 5, 1], 3))       # 12
    print(sol.maxTotalValue([5], 10))               # 0   (single element → max==min)
    print(sol.maxTotalValue([7, 7, 7], 5))          # 0   (all equal)
    print(sol.maxTotalValue([0, 1000000000], 100000))  # 100000000000000
    print(sol.maxTotalValue([3, 1, 4, 1, 5, 9, 2, 6], 4))  # 32  ((9-1)*4)
