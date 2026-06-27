from typing import List
from collections import Counter


class Solution:
    def maximumLength(self, nums: List[int]) -> int:
        # The pattern [x, x², x⁴, ..., xᵏ, ..., x⁴, x², x] is a palindrome
        # whose sorted form is:
        #
        #   [x, x, x², x², x⁴, x⁴, ..., xᵏ]
        #   └──┘ └───┘ └────┘       └──┘
        #    pair  pair   pair     single middle (largest)
        #
        # So: every value except the middle appears EXACTLY twice,
        # and each value squared equals the next value in the chain.
        #
        # Strategy: for each unique starting value x, greedily extend the
        # chain  x → x² → x⁴ → …  as long as each value appears ≥ 2 times
        # in nums.  The first value that appears ≥ 1 time (but possibly < 2)
        # becomes the middle (singleton), adding 1 to the count.
        #
        # Chain length → subset size:
        #   depth pairs found → 2*depth elements from pairs
        #   +1 for the middle  →  2*depth + 1 total
        #   If no middle available, use the deepest pair as middle instead:
        #   2*(depth-1) + 1 = 2*depth - 1
        #
        # Special case x = 1:
        #   1² = 1, so the chain never grows; the whole pattern is [1,1,…,1].
        #   Any odd-length run of 1s is valid.  Pick the largest odd count ≤ cnt[1].
        #
        # Time: O(n + U · log_max) where U = unique values and log_max ≤ 30
        # (because squaring doubles the exponent, so the chain length for any
        # starting value x ≥ 2 is at most log₂(log₂(10⁹)) ≈ 5).

        cnt = Counter(nums)
        ans = 1  # single element always valid

        for x in cnt:

            # ── Special case: x = 1 ─────────────────────────────────────────
            if x == 1:
                c = cnt[1]
                # Largest odd number ≤ c
                ans = max(ans, c if c % 2 == 1 else c - 1)
                continue

            # ── General case: x ≥ 2 ─────────────────────────────────────────
            # Walk the chain x, x², x⁴, …
            # Extend as long as the current value appears ≥ 2 times (can be a pair).
            depth = 0
            v = x
            while cnt.get(v, 0) >= 2:
                depth += 1
                v = v * v   # Python ints don't overflow; huge v just won't be in cnt

            # v is now the candidate for the middle singleton.
            if cnt.get(v, 0) >= 1:
                # v itself can serve as the middle.
                candidate = 2 * depth + 1
            else:
                # v unavailable; reuse the last pair's value as the middle
                # (needs only 1 occurrence, and we had ≥ 2, so it's fine).
                candidate = max(1, 2 * depth - 1)

            ans = max(ans, candidate)

        return ans


# ── Reference: brute-force (for cross-checking small inputs) ─────────────────
class SolutionBrute:
    def maximumLength(self, nums: List[int]) -> int:
        from itertools import combinations

        def is_valid(sub: list) -> bool:
            s = sorted(sub)
            n = len(s)
            if n % 2 == 0:
                return False
            # Pairs at positions (0,1), (2,3), …, (n-3, n-2); middle at n-1.
            for i in range(0, n - 1, 2):
                if s[i] != s[i + 1]:
                    return False
            # Squaring chain: s[0]² == s[2], s[2]² == s[4], …
            for i in range(0, n - 2, 2):
                if s[i] * s[i] != s[i + 2]:
                    return False
            return True

        best = 1
        n = len(nums)
        for size in range(1, n + 1, 2):
            for idxs in combinations(range(n), size):
                if is_valid([nums[i] for i in idxs]):
                    best = max(best, size)
        return best


# ── Quick tests ───────────────────────────────────────────────────────────────
if __name__ == "__main__":
    sol = Solution()

    print(sol.maximumLength([5, 4, 1, 2, 2]))          # 3
    print(sol.maximumLength([1, 3, 2, 4]))              # 1

    # Manual edge cases
    print(sol.maximumLength([2, 4, 16, 4, 2]))          # 5
    print(sol.maximumLength([1, 1, 1, 1, 1]))           # 5  (five 1s, all odd)
    print(sol.maximumLength([1, 1, 1, 1]))              # 3  (four 1s, largest odd = 3)
    print(sol.maximumLength([2, 2]))                    # 1  (only one pair, no middle available? depth=1, no v=4 in cnt → 2*1-1=1)
    print(sol.maximumLength([2, 4, 2]))                 # 3
    print(sol.maximumLength([3, 9, 3]))                 # 3

    # Randomised cross-check
    import random
    random.seed(0)
    ref = SolutionBrute()
    for _ in range(2000):
        n = random.randint(2, 12)
        nums = [random.randint(1, 25) for _ in range(n)]
        a = sol.maximumLength(nums)
        b = ref.maximumLength(nums)
        assert a == b, f"MISMATCH nums={nums}: got {a} expected {b}"
    print("randomised cross-check passed ✓")

    # Timing
    import time
    import random
    big = [random.randint(1, 10**9) for _ in range(10**5)]
    t0 = time.time()
    sol.maximumLength(big)
    print(f"n=10^5 timing: {time.time()-t0:.3f}s")
