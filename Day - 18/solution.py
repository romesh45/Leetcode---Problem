class Solution:
    def search(self, nums: List[int], target: int) -> int:
        left, right = 0, len(nums) - 1
        while left <= right:
            mid = (left + right) // 2
            if nums[mid] == target:
                return mid
            if nums[left] <= nums[mid]:
                if nums[left] <= target < nums[mid]:
                    right = mid - 1      
                else:
                    left = mid + 1       
            else:
                if nums[mid] < target <= nums[right]:
                    left = mid + 1      
                else:
                    right = mid - 1      
        return -1


# ── Quick tests ───────────
if __name__ == "__main__":
    sol = Solution()
    print(sol.search([4, 5, 6, 7, 0, 1, 2], 0))     # 4
    print(sol.search([4, 5, 6, 7, 0, 1, 2], 3))     # -1
    print(sol.search([1], 0))                       # -1
    print(sol.search([1], 1))                       # 0
    print(sol.search([5, 1, 3], 5))                 # 0
    print(sol.search([4, 5, 6, 7, 0, 1, 2], 7))     # 3
    print(sol.search([1, 2, 3, 4, 5], 4))           # 3  (not rotated)
    print(sol.search([6, 7, 1, 2, 3, 4, 5], 6))     # 0
