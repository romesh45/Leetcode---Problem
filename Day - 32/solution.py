class Solution:
    def totalWaviness(self, num1: int, num2: int) -> int:
        # num2 ≤ 10^15 → enumeration is impossible (up to a quadrillion numbers).
        # Use DIGIT DP with a prefix-difference trick.
        #
        #   f(N) = total waviness summed over all numbers in [0, N]
        #   answer = f(num2) - f(num1 - 1)
        #
        # Build numbers digit by digit (most significant first), carrying the
        # previous TWO real digits. When we place a new digit `cur`, the triple
        # (p1, p2, cur) is complete — so we can test whether its middle digit p2
        # is a strict peak or valley. If so, it adds +1 to the waviness of EVERY
        # number that flows through this branch.

        def f(N: int) -> int:
            if N < 0:
                return 0
            digits = list(map(int, str(N)))
            n = len(digits)

            from functools import lru_cache

            @lru_cache(maxsize=None)
            def dp(pos: int, p1: int, p2: int, tight: bool, started: bool):
                # p1 = digit two back, p2 = digit one back; 10 = "none yet".
                # Returns (count_of_completions, total_waviness_over_them).
                if pos == n:
                    return (1, 0)

                limit = digits[pos] if tight else 9
                cnt = 0
                wav = 0

                for cur in range(0, limit + 1):
                    ntight = tight and (cur == limit)

                    if not started:
                        if cur == 0:
                            # Leading zero — the number hasn't begun.
                            c, w = dp(pos + 1, 10, 10, ntight, False)
                        else:
                            # First real digit; no triple possible yet.
                            c, w = dp(pos + 1, 10, cur, ntight, True)
                        cnt += c
                        wav += w
                    else:
                        # With two prior real digits, p2 is the middle of the
                        # triple (p1, p2, cur). Strict peak / valley check.
                        add = 0
                        if p1 != 10 and p2 != 10:
                            if p2 > p1 and p2 > cur:        # peak
                                add = 1
                            elif p2 < p1 and p2 < cur:      # valley
                                add = 1
                        c, w = dp(pos + 1, p2, cur, ntight, True)
                        cnt += c
                        wav += w + add * c                  # distribute +1 across branch

                return (cnt, wav)

            result = dp(0, 10, 10, True, False)[1]
            dp.cache_clear()
            return result

        return f(num2) - f(num1 - 1)


# ── Brute-force reference (Day 31 logic) — for cross-checking small ranges ────
class SolutionBrute:
    def totalWaviness(self, num1: int, num2: int) -> int:
        def waviness(n: int) -> int:
            d = list(map(int, str(n)))
            c = 0
            for i in range(1, len(d) - 1):
                if d[i] > d[i - 1] and d[i] > d[i + 1]:
                    c += 1
                elif d[i] < d[i - 1] and d[i] < d[i + 1]:
                    c += 1
            return c
        return sum(waviness(n) for n in range(num1, num2 + 1))


# ── Quick tests ──────────────────────────────────────────────────────────────
if __name__ == "__main__":
    sol = Solution()
    print(sol.totalWaviness(120, 130))       # 3
    print(sol.totalWaviness(198, 202))       # 3
    print(sol.totalWaviness(4848, 4848))     # 2

    # Large-range sanity (would be impossible to brute force):
    print(sol.totalWaviness(1, 10**15))      # huge number, just must not crash
    print(sol.totalWaviness(1, 999))         # all 3-digit waviness in [1, 999]

    # ── Randomized cross-check against brute force on small ranges ──
    import random
    brute = SolutionBrute()
    for _ in range(300):
        a = random.randint(1, 5000)
        b = random.randint(a, a + random.randint(0, 5000))
        assert sol.totalWaviness(a, b) == brute.totalWaviness(a, b), (a, b)
    print("randomized cross-check passed ✓")
