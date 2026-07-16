class Solution:
    def sumOfGcdPairs(self, nums: List[int]) -> int:
        # Step 1: build prefixGcd[i] = gcd(nums[i], max(nums[0..i]))
        prefix_gcd = []
        running_max = 0
        for x in nums:
            running_max = max(running_max, x)
            prefix_gcd.append(gcd(x, running_max))

        # Step 2: sort, then pair smallest with largest
        prefix_gcd.sort()

        result = 0
        lo, hi = 0, len(prefix_gcd) - 1
        while lo < hi:
            result += gcd(prefix_gcd[lo], prefix_gcd[hi])
            lo += 1
            hi -= 1

        return result


# Quick tests
if __name__ == "__main__":
    sol = Solution()

    print(sol.sumOfGcdPairs([2, 6, 4]))          # 2
    print(sol.sumOfGcdPairs([3, 6, 2, 8]))        # 5
    print(sol.sumOfGcdPairs([1]))                 # 0
    print(sol.sumOfGcdPairs([7, 7]))              # 7
    print(sol.sumOfGcdPairs([4, 8, 16, 2]))       # 6
