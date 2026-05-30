class Solution:
    def minElement(self, nums: List[int]) -> int:
        def digit_sum(x: int) -> int:
            s = 0
            while x:
                s += x % 10
                x //= 10
            return s
        return min(digit_sum(x) for x in nums)





# ── One-liner (string-based, equivalent) ──────────────────────
class SolutionString:
    def minElement(self, nums: List[int]) -> int:
        return min(sum(int(d) for d in str(x)) for x in nums)






# ── Quick tests ──────────────────────────────────
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
