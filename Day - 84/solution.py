class Solution:
    def maxProduct(self, nums: List[int]) -> int:
        nums.sort()
        return (nums[-1] - 1) * (nums[-2] - 1)


# Quick tests
if __name__ == "__main__":
    sol = Solution()

    print(sol.maxProduct([3, 4, 5, 2]))   # 12
    print(sol.maxProduct([1, 5, 4, 5]))   # 16
    print(sol.maxProduct([3, 7]))          # 12
    print(sol.maxProduct([1, 1]))          # 0
