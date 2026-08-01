from typing import List


class Solution:
    def predictTheWinner(self, nums: List[int]) -> bool:
        n = len(nums)
        # dp[i][j] = best score difference (current player - opponent)
        # achievable from the subarray nums[i..j], both playing optimally.
        # Taking nums[i] gives nums[i] - dp[i+1][j] (opponent now leads on rest).
        # Taking nums[j] gives nums[j] - dp[i][j-1].
        dp = [[0] * n for _ in range(n)]
        for i in range(n):
            dp[i][i] = nums[i]
        for length in range(2, n + 1):
            for i in range(n - length + 1):
                j = i + length - 1
                dp[i][j] = max(nums[i] - dp[i + 1][j],
                               nums[j] - dp[i][j - 1])
        return dp[0][n - 1] >= 0


# Quick tests
if __name__ == "__main__":
    sol = Solution()

    print(sol.predictTheWinner([1, 5, 2]))        # False
    print(sol.predictTheWinner([1, 5, 233, 7]))   # True
    print(sol.predictTheWinner([1]))              # True  single element
    print(sol.predictTheWinner([1, 2]))           # True  P1 takes 2, wins
    print(sol.predictTheWinner([0, 0, 0]))        # True  tie -> P1 wins
