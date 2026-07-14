class Solution:
    def subsequencePairCount(self, nums: List[int]) -> int:
        MOD = 10**9 + 7

        # DP state: (g1, g2) where
        #   g1 = running GCD of elements assigned to seq1  (0 → seq1 still empty)
        #   g2 = running GCD of elements assigned to seq2  (0 → seq2 still empty)
        #
        # For each element x we have exactly three choices:
        #   1. Skip x  →  (g1, g2) unchanged
        #   2. Assign to seq1  →  (gcd(g1, x), g2)     [gcd(0, x) = x by convention]
        #   3. Assign to seq2  →  (g1, gcd(g2, x))
        #
        # Number of distinct GCD values ≤ max(nums) ≤ 200, so active states stay
        # well within 201² ≈ 40 000 — the defaultdict only stores non-zero ones.
        dp = defaultdict(int)
        dp[(0, 0)] = 1

        for x in nums:
            new_dp = defaultdict(int)
            for (g1, g2), cnt in dp.items():
                new_dp[g1, g2]          = (new_dp[g1, g2]          + cnt) % MOD
                new_dp[gcd(g1, x), g2]  = (new_dp[gcd(g1, x), g2]  + cnt) % MOD
                new_dp[g1, gcd(g2, x)]  = (new_dp[g1, gcd(g2, x)]  + cnt) % MOD
            dp = new_dp

        # Both subsequences must be non-empty (g > 0) and share the same GCD
        return sum(cnt for (g1, g2), cnt in dp.items() if g1 == g2 > 0) % MOD


# ── Quick tests ───────────────────────────────────────────────────────────────
if __name__ == "__main__":
    sol = Solution()

    print(sol.subsequencePairCount([1, 2, 3, 4]))  # 10
    print(sol.subsequencePairCount([10, 20, 30]))  # 2
    print(sol.subsequencePairCount([1, 1, 1, 1]))  # 50

    # Edge cases
    print(sol.subsequencePairCount([1]))            # 0  can't form two disjoint non-empty seqs
    print(sol.subsequencePairCount([6, 6]))         # 1  only ({6},{6})
    print(sol.subsequencePairCount([2, 4, 6, 8]))  # verify manually: multiple GCD groups
