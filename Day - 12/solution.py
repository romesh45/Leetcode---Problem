class Solution:
    def findMin(self, nums: List[int]) -> int:
        left, right = 0, len(nums) - 1
        while left < right:
            mid = (left + right) // 2
            if nums[mid] > nums[right]:
                left = mid + 1
            elif nums[mid] < nums[right]:
                right = mid
            else:
                right -= 1
        return nums[left]

# ── Quick tests ──────────────────────────────────────────────────────────────
if __name__ == "__main__":
    sol = Solution()
    print(sol.findMin([1, 3, 5]))                       # 1
    print(sol.findMin([2, 2, 2, 0, 1]))                 # 0
    print(sol.findMin([3, 3, 1, 3]))                    # 1
    print(sol.findMin([3, 1, 3]))                       # 1
    print(sol.findMin([10, 1, 10, 10, 10]))             # 1
    print(sol.findMin([1]))                             # 1
    print(sol.findMin([1, 1, 1, 1]))                    # 1
    print(sol.findMin([4, 5, 6, 7, 0, 1, 2]))           # 0
    print(sol.findMin([2, 2, 2, 2, 2]))                 # 2
