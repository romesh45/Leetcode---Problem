from typing import List


class Solution:
    def minElement(self, nums: List[int]) -> int:
        # Replace each element with the sum of its digits, then return the min.
        # The problem only asks for the min of the new array — we can compute
        # each digit sum on the fly and feed it straight into min(), no
        # intermediate list needed.
        def digit_sum(x: int) -> int:
            # Strip digits right-to-left:
            #   x % 10 → last digit
            #   x // 10 → drop that digit
            # For x ≤ 10⁴ this loops at most 5 times.
            s = 0
            while x:
                s += x % 10
                x //= 10
            return s

        return min(digit_sum(x) for x in nums)


# ── One-liner (string-based, equivalent) ─────────────────────────────────────
class SolutionString:
    def minElement(self, nums: List[int]) -> int:
        return min(sum(int(d) for d in str(x)) for x in nums)


# ── Quick tests ──────────────────────────────────────────────────────────────
if __name__ == "__main__":
    sol = Solution()
    print(sol.minElement([10, 12, 13, 14]))       # 1   (→ [1, 3, 4, 5])
    print(sol.minElement([1, 2, 3, 4]))           # 1   (→ [1, 2, 3, 4])
    print(sol.minElement([999, 19, 199]))         # 10  (→ [27, 10, 19])
    print(sol.minElement([1]))                    # 1
    print(sol.minElement([10000]))                # 1
    print(sol.minElement([9999]))                 # 36
    print(sol.minElement([100, 1000, 10000]))     # 1

    sol2 = SolutionString()
    print(sol2.minElement([999, 19, 199]))        # 10
    print(sol2.minElement([10, 12, 13, 14]))      # 1
