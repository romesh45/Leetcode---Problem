class Solution:
    def uniqueXorTriplets(self, nums: List[int]) -> int:
        # Unlike Part I, nums is NOT a permutation -- any integers 1..1500.
        # The same triple analysis applies:
        #   i=j=k  -> a XOR a XOR a = a         (single element)
        #   i=j<k  -> a XOR a XOR b = b          (single element)
        #   i<j=k  -> a XOR b XOR b = a          (single element)
        #   i<j<k  -> a XOR b XOR c              (new values)
        #
        # So achievable = {a XOR b XOR c : a, b, c taken from nums}.
        # For distinct values a,b,c in A, they have distinct indices (one each),
        # so every such triple is formable. Non-distinct value triples reduce to
        # single elements already in A.
        #
        # Compute in two passes over the DISTINCT value set A:
        #   pairs = {a XOR b : a, b in A}           <= 2048 values (nums[i] <= 1500 < 2048)
        #   triples = {p XOR c : p in pairs, c in A} <= 2048 values
        #
        # Total: O(|A|^2 + |pairs| * |A|) ~ O(1500^2 + 2048 * 1500) ~ 5M ops.

        A = set(nums)
        pairs = {a ^ b for a in A for b in A}
        return len({p ^ c for p in pairs for c in A})


# Quick tests
if __name__ == "__main__":
    sol = Solution()

    print(sol.uniqueXorTriplets([1, 3]))          # 2
    print(sol.uniqueXorTriplets([6, 7, 8, 9]))    # 4

    # Extra checks
    print(sol.uniqueXorTriplets([1]))              # 1  single element
    print(sol.uniqueXorTriplets([1, 2]))           # 2  n=2
    print(sol.uniqueXorTriplets([1, 2, 3]))        # 4  {0,1,2,3}

    # Brute force for n=3 case
    def brute(nums):
        n = len(nums)
        seen = set()
        for i in range(n):
            for j in range(i, n):
                for k in range(j, n):
                    seen.add(nums[i] ^ nums[j] ^ nums[k])
        return len(seen)

    for test in [[1,3],[6,7,8,9],[1,2,3],[1,2,3,4],[1,3,5,7]]:
        formula = sol.uniqueXorTriplets(test)
        bf = brute(test)
        print(f"{test}: formula={formula} brute={bf} {'OK' if formula==bf else 'FAIL'}")
