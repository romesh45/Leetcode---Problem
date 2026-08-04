from typing import List


class Solution:
    def findMissingElements(self, nums: List[int]) -> List[int]:
        s = set(nums)
        return [x for x in range(min(nums), max(nums) + 1) if x not in s]


# Quick tests
if __name__ == "__main__":
    sol = Solution()

    print(sol.findMissingElements([1, 4, 2, 5]))   # [3]
    print(sol.findMissingElements([7, 8, 6, 9]))   # []
    print(sol.findMissingElements([5, 1]))          # [2, 3, 4]
    print(sol.findMissingElements([1, 2]))          # []
