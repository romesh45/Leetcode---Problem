class Solution:
    def winnerSquareGame(self, n: int) -> bool:
        # dp[i] = True if the current player wins with i stones remaining.
        # dp[0] = False (no move -> current player loses).
        # dp[i] = True if there exists a perfect square s^2 <= i such that
        #         dp[i - s^2] is False (opponent is put in a losing position).
        dp = [False] * (n + 1)
        for i in range(1, n + 1):
            s = 1
            while s * s <= i:
                if not dp[i - s * s]:
                    dp[i] = True
                    break
                s += 1
        return dp[n]


# Quick tests
if __name__ == "__main__":
    sol = Solution()

    print(sol.winnerSquareGame(1))    # True   (take 1)
    print(sol.winnerSquareGame(2))    # False  (any move leaves opponent winning)
    print(sol.winnerSquareGame(4))    # True   (take 4)
    print(sol.winnerSquareGame(7))    # False
    print(sol.winnerSquareGame(17))   # False
