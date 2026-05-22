from typing import List


class Solution:
    def search(self, nums: List[int], target: int) -> int:
        # Modified binary search.
        #
        # A rotated sorted array has exactly ONE break point. So for any mid,
        # the split into [left..mid] and [mid..right] always leaves at least
        # one half fully sorted. Identify the sorted half (its value range is
        # known), test whether target lies inside it, and discard half.
        left, right = 0, len(nums) - 1

        while left <= right:
            mid = (left + right) // 2

            if nums[mid] == target:
                return mid

            # Is the LEFT half [left..mid] sorted?
            # nums[left] <= nums[mid] also covers the no-rotation / 1-element case.
            if nums[left] <= nums[mid]:
                # Left half is sorted — its range is [nums[left], nums[mid]).
                if nums[left] <= target < nums[mid]:
                    right = mid - 1      # target is inside the sorted left half
                else:
                    left = mid + 1       # target must be in the right half
            else:
                # Right half [mid..right] is sorted — range is (nums[mid], nums[right]].
                if nums[mid] < target <= nums[right]:
                    left = mid + 1       # target is inside the sorted right half
                else:
                    right = mid - 1      # target must be in the left half

        return -1


# ── Quick tests ──────────────────────────────────────────────────────────────
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
