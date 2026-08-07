from math import prod


class Solution:
    def smallestNumber(self, n: int, t: int) -> int:
        # Note: any number containing a 0 digit has digit product 0,
        # which is divisible by every t -- so the loop terminates quickly.
        while prod(int(d) for d in str(n)) % t != 0:
            n += 1
        return n


# Quick tests
if __name__ == "__main__":
    sol = Solution()

    print(sol.smallestNumber(10, 2))   # 10  (digit product 0, div by 2)
    print(sol.smallestNumber(15, 3))   # 16  (digit product 6, div by 3)
    print(sol.smallestNumber(1, 10))   # 10  (digit product 0)
    print(sol.smallestNumber(99, 9))   # 99  (9*9=81, div by 9)
