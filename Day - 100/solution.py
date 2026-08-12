from typing import List
from collections import defaultdict


class Solution:
    def maxSubarrayLength(self, nums: List[int], k: int) -> int:
        freq = defaultdict(int)
        left = ans = 0
        for right, x in enumerate(nums):
            freq[x] += 1
            # Shrink window from the left until x's frequency is <= k
            while freq[x] > k:
                freq[nums[left]] -= 1
                left += 1
            ans = max(ans, right - left + 1)
        return ans


# Quick tests
if __name__ == "__main__":
    sol = Solution()

    print(sol.maxSubarrayLength([1, 2, 3, 1, 2, 3, 1, 2], 2))   # 6
    print(sol.maxSubarrayLength([1, 2, 1, 2, 1, 2, 1, 2], 1))   # 2
    print(sol.maxSubarrayLength([5, 5, 5, 5, 5, 5, 5], 4))      # 4
    print(sol.maxSubarrayLength([1], 1))                          # 1
