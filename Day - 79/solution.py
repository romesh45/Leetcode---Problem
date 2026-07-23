from typing import List


class Solution:
    def uniqueXorTriplets(self, nums: List[int]) -> int:
        n = len(nums)

        # nums is a permutation of {1,...,n}, so the SET of values is exactly {1,...,n}.
        # The achievable XOR triplet values depend only on n, not the order of nums.
        #
        # A triplet (i,j,k) with i<=j<=k produces:
        #   i=j=k  ->  a XOR a XOR a = a          (any single element)
        #   i=j<k  ->  a XOR a XOR b = b           (any single element)
        #   i<j=k  ->  a XOR b XOR b = a           (any single element)
        #   i<j<k  ->  a XOR b XOR c (all distinct) (new values)
        #
        # So the achievable set = {1,...,n} U {a XOR b XOR c : a,b,c distinct in {1,...,n}}.
        #
        # n=1: only {1}.                  Output = 1.
        # n=2: no triple of distinct elems possible.  Output = 2.
        # n>=3: {1,...,n} contains 1,2,4,...,2^(k-1) as a GF(2) basis where
        #        k = n.bit_length().  With n>=3 elements, XOR triplets can reach
        #        every value in {0,...,2^k - 1}.  Output = 2^k.

        if n <= 2:
            return n
        return 1 << n.bit_length()


# Quick tests
if __name__ == "__main__":
    sol = Solution()

    print(sol.uniqueXorTriplets([1, 2]))         # 2
    print(sol.uniqueXorTriplets([3, 1, 2]))      # 4

    # Extra verification
    print(sol.uniqueXorTriplets([1]))            # 1
    print(sol.uniqueXorTriplets([2, 1, 4, 3]))  # 8  (n=4, 2^3)
    print(sol.uniqueXorTriplets(list(range(1, 8))))   # 8  (n=7, 2^3)
    print(sol.uniqueXorTriplets(list(range(1, 9))))   # 16 (n=8, 2^4)

    # Brute-force check for n=3 and n=4
    from itertools import product
    for perm in [[1,2,3], [1,2,3,4]]:
        n2 = len(perm)
        vals = set()
        for i in range(n2):
            for j in range(i, n2):
                for k in range(j, n2):
                    vals.add(perm[i] ^ perm[j] ^ perm[k])
        print(f"n={n2} brute={len(vals)} formula={1 << n2.bit_length()}")
