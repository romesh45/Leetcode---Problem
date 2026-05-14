from typing import List


class Solution:
    def isGood(self, nums: List[int]) -> bool:
        # The candidate "n" is forced by the maximum element of nums.
        # For nums to match base[n] = [1, 2, ..., n-1, n, n]:
        #   1) length must be exactly n + 1
        #   2) sorting nums must yield [1, 2, ..., n-1, n, n]
        n = max(nums)

        # Fast length check — rules out cases like Example 1 and Example 4
        # without doing any sorting work.
        if len(nums) != n + 1:
            return False

        # Sort once and compare element-by-element to the expected base[n].
        # base[n] is [1, 2, ..., n-1, n, n], which equals list(range(1, n)) + [n, n].
        nums.sort()
        expected = list(range(1, n)) + [n, n]
        return nums == expected


# ── Quick tests ──────────────────────────────────────────────────────────────
if __name__ == "__main__":
    sol = Solution()
    print(sol.isGood([2, 1, 3]))             # False
    print(sol.isGood([1, 3, 3, 2]))          # True
    print(sol.isGood([1, 1]))                # True
    print(sol.isGood([3, 4, 4, 1, 2, 1]))    # False
    print(sol.isGood([1, 2, 3, 4, 5, 5]))    # True
    print(sol.isGood([1]))                   # False (length must be 2)
    print(sol.isGood([2, 2, 1]))             # True  (base[2] = [1, 2, 2])
