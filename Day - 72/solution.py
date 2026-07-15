from math import gcd


class Solution:
    def gcdOfSums(self, n: int) -> int:
        # Sum of first n odd  numbers: 1+3+5+…+(2n-1) = n²
        # Sum of first n even numbers: 2+4+6+…+2n     = n(n+1)
        #
        # GCD(n², n(n+1)) = n · GCD(n, n+1) = n · 1 = n
        #
        # GCD(n, n+1) = 1 because consecutive integers are always coprime.
        return n


# ── Quick tests ───────────────────────────────────────────────────────────────
if __name__ == "__main__":
    sol = Solution()

    # Verify formula against brute-force for sanity
    for n in [1, 2, 3, 4, 5, 10, 100, 1000]:
        sum_odd  = sum(2*i - 1 for i in range(1, n + 1))  # n²
        sum_even = sum(2*i     for i in range(1, n + 1))  # n(n+1)
        expected = gcd(sum_odd, sum_even)
        got = sol.gcdOfSums(n)
        print(f"n={n:4d}  sumOdd={sum_odd:7d}  sumEven={sum_even:7d}  "
              f"expected={expected:4d}  got={got:4d}  {'✓' if got == expected else '✗'}")
