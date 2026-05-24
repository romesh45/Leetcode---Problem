class Solution:
    def isGood(self, nums: List[int]) -> bool:
        n = max(nums)
        if len(nums) != n + 1:
            return False
        nums.sort()
        expected = list(range(1, n)) + [n, n]
        return nums == expected


# ── Quick tests ──────────────────────────────────────────────────────────────
if __name__ == "__main__":
    sol = Solution()
    print(sol.isGood([2, 1, 3]))             # False
    print(sol.isGood([1, 3, 3, 2]))          # True
    print(sol.isGood([1, 1]))                # True
    print(sol.isGood([3, 4, 4, 1, 2, 1]))    # False
    print(sol.isGood([1, 2, 3, 4, 5, 5]))    # True
    print(sol.isGood([1]))                   # False (length must be 2)
    print(sol.isGood([2, 2, 1]))             # True  (base[2] = [1, 2, 2])
