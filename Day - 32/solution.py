class Solution:
    def totalWaviness(self, num1: int, num2: int) -> int:
        def f(N: int) -> int:
            if N < 0:
                return 0
            digits = list(map(int, str(N)))
            n = len(digits)
            from functools import lru_cache
            @lru_cache(maxsize=None)
            def dp(pos: int, p1: int, p2: int, tight: bool, started: bool):
                if pos == n:
                    return (1, 0)
                limit = digits[pos] if tight else 9
                cnt = 0
                wav = 0
                for cur in range(0, limit + 1):
                    ntight = tight and (cur == limit)
                    if not started:
                        if cur == 0:
                            c, w = dp(pos + 1, 10, 10, ntight, False)
                        else:
                            c, w = dp(pos + 1, 10, cur, ntight, True)
                        cnt += c
                        wav += w
                    else:
                        add = 0
                        if p1 != 10 and p2 != 10:
                            if p2 > p1 and p2 > cur:        
                                add = 1
                            elif p2 < p1 and p2 < cur:     
                                add = 1
                        c, w = dp(pos + 1, p2, cur, ntight, True)
                        cnt += c
                        wav += w + add * c                  
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


# ── Quick tests ────────────────────────────────────
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
