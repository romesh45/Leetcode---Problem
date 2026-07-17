class Solution:
    def gcdValues(self, nums: List[int], queries: List[int]) -> List[int]:
        MAX_VAL = max(nums) + 1

        # 1. Frequency table
        freq = [0] * MAX_VAL
        for x in nums:
            freq[x] += 1

        # 2. cnt[d] = how many elements in nums are divisible by d
        #    (sieve-style, O(MAX_VAL log MAX_VAL) harmonic series)
        cnt = [0] * MAX_VAL
        for d in range(1, MAX_VAL):
            for k in range(d, MAX_VAL, d):
                cnt[d] += freq[k]

        # 3. exact[d] = number of pairs (i<j) with gcd(nums[i],nums[j]) == d
        #
        #    C(cnt[d], 2) counts pairs where BOTH elements are divisible by d,
        #    i.e. pairs whose GCD is any MULTIPLE of d. Subtracting the exact
        #    counts for all larger multiples leaves only pairs with GCD exactly d.
        #    Process d high-to-low so multiples are already computed.
        exact = [0] * MAX_VAL
        for d in range(MAX_VAL - 1, 0, -1):
            exact[d] = cnt[d] * (cnt[d] - 1) // 2
            for k in range(2 * d, MAX_VAL, d):
                exact[d] -= exact[k]

        # 4. prefix[g] = number of pairs with GCD <= g  (cumulative)
        prefix = [0] * MAX_VAL
        for d in range(1, MAX_VAL):
            prefix[d] = prefix[d - 1] + exact[d]

        # 5. Each query q: find smallest g with prefix[g] > q
        #    bisect_right on the prefix array gives this directly.
        return [bisect_right(prefix, q) for q in queries]


# Quick tests
if __name__ == "__main__":
    sol = Solution()

    print(sol.gcdValues([2, 3, 4], [0, 2, 2]))         # [1, 2, 2]
    print(sol.gcdValues([4, 4, 2, 1], [5, 3, 1, 0]))   # [4, 2, 1, 1]
    print(sol.gcdValues([2, 2], [0, 0]))                # [2, 2]

    # Edge cases
    print(sol.gcdValues([6, 10, 15], [0, 1, 2]))        # [1, 2, 3]  all coprime pairs + (6,10)=2, (6,15)=3
    print(sol.gcdValues([1, 1, 1], [0, 1, 2]))          # [1, 1, 1]
