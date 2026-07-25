class Solution:
    def maxProduct(self, n: int) -> int:
        digits = sorted(int(d) for d in str(n))
        return digits[-1] * digits[-2]


# Quick tests
if __name__ == "__main__":
    sol = Solution()

    print(sol.maxProduct(31))          # 3
    print(sol.maxProduct(22))          # 4
    print(sol.maxProduct(124))         # 8
    print(sol.maxProduct(9999))        # 81
    print(sol.maxProduct(1000000000))  # 1  (digits: 1,0,0,...,0)
