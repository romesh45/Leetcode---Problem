from typing import List


class Solution:
    def findMin(self, nums: List[int]) -> int:
        # Modified binary search — same skeleton as LC 153 ("no duplicates")
        # but with a third branch to handle nums[mid] == nums[right].
        #
        # We compare nums[mid] with nums[right] (NOT nums[left]) because the
        # right endpoint always sits in the "lower run" of the rotated array
        # (or equals it when not rotated).
        left, right = 0, len(nums) - 1

        while left < right:
            mid = (left + right) // 2

            if nums[mid] > nums[right]:
                # The "drop" lies strictly to the right of mid.
                # Minimum is somewhere in (mid, right].
                left = mid + 1

            elif nums[mid] < nums[right]:
                # Right half is sorted → minimum is at mid or to its left.
                # Keep mid as a candidate (right = mid, not mid - 1).
                right = mid

            else:
                # nums[mid] == nums[right] — ambiguous.
                # We can't decide which side holds the min from this comparison
                # (e.g., [3,3,1,3] vs [3,1,3,3,3] both hit this tie).
                #
                # Safe fallback: shrink the window by one from the right.
                # If nums[right] were the unique minimum, nums[mid] would equal it
                # → mid still holds an equivalent value, so dropping right is safe.
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
