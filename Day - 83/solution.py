class Solution:
    def maximumProduct(self, nums: List[int]) -> int:
        # After sorting, the answer is one of two candidates:
        #   A. Three largest values            (nums[-3] * nums[-2] * nums[-1])
        #   B. Two smallest (most negative) * largest  (nums[0] * nums[1] * nums[-1])
        # Two negatives multiply to a large positive, which can beat three positives.
        nums.sort()
        return max(nums[-1] * nums[-2] * nums[-3],
                   nums[0]  * nums[1]  * nums[-1])


# Quick tests
if __name__ == "__main__":
    sol = Solution()

    print(sol.maximumProduct([1, 2, 3]))          # 6
    print(sol.maximumProduct([1, 2, 3, 4]))       # 24
    print(sol.maximumProduct([-1, -2, -3]))       # -6
    print(sol.maximumProduct([-100, -99, 1, 2]))  # 19800  (-100 * -99 * 2)
    print(sol.maximumProduct([-1, -2, 0, 3]))     # 6      (-1 * -2 * 3)
