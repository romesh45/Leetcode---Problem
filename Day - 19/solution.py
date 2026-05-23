class Solution:
    def check(self, nums: List[int]) -> bool:
        n = len(nums)
        drops = 0
        for i in range(n):
            if nums[i] > nums[(i + 1) % n]:
                drops += 1
                if drops > 1:           
                    return False
        return True


# ── Quick tests ──────────────────────────────────────────────────────────────
if __name__ == "__main__":
    sol = Solution()
    print(sol.check([3, 4, 5, 1, 2]))      # True
    print(sol.check([2, 1, 3, 4]))         # False
    print(sol.check([1, 2, 3]))            # True
    print(sol.check([1]))                  # True
    print(sol.check([1, 1, 1]))            # True
    print(sol.check([2, 1]))               # True   (rotated [1, 2])
    print(sol.check([6, 10, 6]))           # True   ([6,6,10] rotated by 2 → single drop 10→6)
    print(sol.check([1, 3, 2]))            # False  (drops: 3>2 and wrap 2>1 → 2 drops)
