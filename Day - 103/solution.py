from typing import List
from functools import reduce
from operator import xor


class Solution:
    def longestSubsequence(self, nums: List[int]) -> int:
        # XOR of a subsequence depends only on which elements are included,
        # not their order. So we want the LARGEST subset with non-zero XOR.
        #
        # Case 1: XOR of all elements != 0 -> take everything, answer = n.
        #
        # Case 2: XOR of all elements == 0:
        #   - If any element x != 0: remove it. Remaining XOR = 0 ^ x = x != 0.
        #     Answer = n - 1.
        #   - All zeros: every subset has XOR 0. Answer = 0.

        total = reduce(xor, nums)
        if total != 0:
            return len(nums)
        if any(x != 0 for x in nums):
            return len(nums) - 1
        return 0


# Quick tests
if __name__ == "__main__":
    sol = Solution()

    print(sol.longestSubsequence([1, 2, 3]))      # 2  (1^2^3=0, remove one)
    print(sol.longestSubsequence([2, 3, 4]))      # 3  (2^3^4=5 != 0)
    print(sol.longestSubsequence([0, 0, 0]))      # 0  (all zeros)
    print(sol.longestSubsequence([0, 0, 1]))      # 2  (1^0^0=1? no, 0^0^1=1)
    print(sol.longestSubsequence([5]))             # 1
    print(sol.longestSubsequence([0]))             # 0
