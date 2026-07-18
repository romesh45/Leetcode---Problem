from math import gcd
from typing import List


class Solution:
    def findGCD(self, nums: List[int]) -> int:
        return gcd(min(nums), max(nums))


# Quick tests
if __name__ == "__main__":
    sol = Solution()

    print(sol.findGCD([2, 5, 6, 9, 10]))   # 2
    print(sol.findGCD([7, 5, 6, 8, 3]))    # 1
    print(sol.findGCD([3, 3]))             # 3
    print(sol.findGCD([1, 1000]))          # 1
    print(sol.findGCD([12, 18, 24]))       # 6
