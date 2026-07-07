class Solution:
    def concatenateAndMultiply(self, n: int) -> int:
        # Pull out the non-zero digit characters in order
        digits = [d for d in str(n) if d != '0']

        if not digits:
            return 0  # n = 0 → x = 0 → result = 0

        x     = int(''.join(digits))          # concatenation
        total = sum(int(d) for d in digits)   # digit sum (same digits as x)
        return x * total


# ── Quick tests ──────────────────────────────────────────
if __name__ == "__main__":
    sol = Solution()

    print(sol.concatenateAndMultiply(10203004))  # 12340
    print(sol.concatenateAndMultiply(1000))       # 1

    # Edge cases
    print(sol.concatenateAndMultiply(0))          # 0   no non-zero digits
    print(sol.concatenateAndMultiply(9))          # 81  single digit: 9 * 9
    print(sol.concatenateAndMultiply(100000000))  # 1   only one non-zero digit
    print(sol.concatenateAndMultiply(123456789))  # 123456789 * 45
