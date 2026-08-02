from typing import List


class Solution:
    def stoneGame(self, piles: List[int]) -> bool:
        # Mathematical proof: Alice ALWAYS wins under these constraints.
        #
        # With an even number of piles, the positions split into two sets:
        #   Even-indexed: piles[0], piles[2], piles[4], ...
        #   Odd-indexed:  piles[1], piles[3], piles[5], ...
        #
        # Since the total is odd, one set has a strictly larger sum.
        # Before the game Alice checks which set is larger. She then adopts the
        # following strategy:
        #   - If even-indexed piles sum more, take piles[0] on her first move.
        #   - Whatever Bob takes (either current end), the new ends are both
        #     odd-indexed, so Alice again takes an even-indexed pile. Repeat.
        # Alice always gets every pile of her chosen parity. QED.
        return True


# Sanity check with DP (same as Predict the Winner)
def dp_check(piles):
    n = len(piles)
    dp = list(piles)
    for length in range(2, n + 1):
        for i in range(n - length + 1):
            j = i + length - 1
            dp[i] = max(piles[i] - dp[i + 1], piles[j] - dp[i])
    return dp[0] >= 0

if __name__ == "__main__":
    sol = Solution()

    cases = [[5, 3, 4, 5], [3, 7, 2, 3], [1, 3], [5, 1]]
    for piles in cases:
        formula = sol.stoneGame(piles)
        dp = dp_check(piles)
        print(f"{piles}: formula={formula} dp={dp} {'OK' if formula == dp else 'FAIL'}")
