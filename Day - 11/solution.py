from typing import List


class Solution:
    def findMin(self, nums: List[int]) -> int:
        # Binary search for the rotation pivot — the smallest element.
        # We compare nums[mid] with nums[right] (NOT nums[left]) to decide
        # which half currently contains the minimum.
        left, right = 0, len(nums) - 1

        while left < right:
            mid = (left + right) // 2

            if nums[mid] > nums[right]:
                # nums[mid] is bigger than the rightmost element → the "drop"
                # (and therefore the minimum) lies strictly to the right of mid.
                left = mid + 1
            else:
                # nums[mid] <= nums[right] → the right half is sorted.
                # The minimum is at mid or somewhere to its left — never to the right.
                # Keep mid as a candidate by setting right = mid (not mid - 1).
                right = mid

        # The loop exits when left == right, pinned on the index of the minimum.
        return nums[left]


# ── Quick tests ──────────────────────────────────────────────────────────────
if __name__ == "__main__":
    sol = Solution()
    print(sol.findMin([3, 4, 5, 1, 2]))             # 1
    print(sol.findMin([4, 5, 6, 7, 0, 1, 2]))       # 0
    print(sol.findMin([11, 13, 15, 17]))            # 11
    print(sol.findMin([2, 1]))                      # 1
    print(sol.findMin([1]))                         # 1
    print(sol.findMin([5, 1, 2, 3, 4]))             # 1
    print(sol.findMin([1, 2, 3, 4, 5]))             # 1  (not rotated / rotated n times)
