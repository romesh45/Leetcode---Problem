from typing import List


class Solution:
    def stoneGameIII(self, stoneValue: List[int]) -> str:
        n = len(stoneValue)
        # dp[i] = best score difference (current player - opponent) from index i onward.
        # From i, the current player can take 1, 2, or 3 stones:
        #   take k stones -> gain sum(stoneValue[i:i+k]), opponent faces dp[i+k]
        #   net = sum - dp[i+k]   (opponent's gain is subtracted)
        dp = [0] * (n + 1)   # dp[n] = 0 (nothing left)
        for i in range(n - 1, -1, -1):
            best = float('-inf')
            total = 0
            for k in range(1, 4):
                if i + k > n:
                    break
                total += stoneValue[i + k - 1]
                best = max(best, total - dp[i + k])
            dp[i] = best

        if dp[0] > 0:
            return "Alice"
        if dp[0] < 0:
            return "Bob"
        return "Tie"


# Quick tests
if __name__ == "__main__":
    sol = Solution()

    print(sol.stoneGameIII([1, 2, 3, 7]))    # "Bob"
    print(sol.stoneGameIII([1, 2, 3, -9]))   # "Alice"
    print(sol.stoneGameIII([1, 2, 3, 6]))    # "Tie"
    print(sol.stoneGameIII([1]))             # "Alice"
    print(sol.stoneGameIII([-1, -2, -3]))    # "Tie"  both forced to take negatives
