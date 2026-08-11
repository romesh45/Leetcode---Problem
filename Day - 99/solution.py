from typing import List


class Solution:
    def missingInteger(self, nums: List[int]) -> int:
        # Step 1: sum the longest sequential prefix
        prefix_sum = nums[0]
        for i in range(1, len(nums)):
            if nums[i] == nums[i - 1] + 1:
                prefix_sum += nums[i]
            else:
                break

        # Step 2: find smallest integer >= prefix_sum not in nums
        s = set(nums)
        x = prefix_sum
        while x in s:
            x += 1
        return x


# Quick tests
if __name__ == "__main__":
    sol = Solution()

    print(sol.missingInteger([1, 2, 3, 2, 5]))             # 6
    print(sol.missingInteger([3, 4, 5, 1, 12, 14, 13]))    # 15
    print(sol.missingInteger([1]))                          # 1
    print(sol.missingInteger([5, 6, 7, 8]))                 # 26  (sum=26, not in array)
