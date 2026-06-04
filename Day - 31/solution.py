class Solution:
    def totalWaviness(self, num1: int, num2: int) -> int:
        # The range is tiny (num2 ≤ 10^5), so brute force every number:
        # turn it into its digits and count interior peaks/valleys.
        def waviness(n: int) -> int:
            d = list(map(int, str(n)))
            count = 0
            # Only INTERIOR digits (index 1 .. len-2) can be peaks/valleys —
            # the first and last digit are excluded by definition. For numbers
            # with < 3 digits this range is empty → waviness 0, no special case.
            for i in range(1, len(d) - 1):
                if d[i] > d[i - 1] and d[i] > d[i + 1]:        # strict peak
                    count += 1
                elif d[i] < d[i - 1] and d[i] < d[i + 1]:      # strict valley
                    count += 1
            return count

        return sum(waviness(n) for n in range(num1, num2 + 1))


# ── Quick tests ──────────────────────────────────────────────────────────────
if __name__ == "__main__":
    sol = Solution()
    print(sol.totalWaviness(120, 130))     # 3
    print(sol.totalWaviness(198, 202))     # 3
    print(sol.totalWaviness(4848, 4848))   # 2
    print(sol.totalWaviness(1, 99))        # 0   (no 3-digit numbers)
    print(sol.totalWaviness(100, 100))     # 0   (1,0,0 — middle 0 is not strict)
    print(sol.totalWaviness(121, 121))     # 1
    print(sol.totalWaviness(12121, 12121)) # 3   (1,2,1,2,1 → peak,valley,peak)
