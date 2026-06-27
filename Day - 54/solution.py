class Solution:
    def maximumLength(self, nums: List[int]) -> int:
        cnt = Counter(nums)
        ans = 1  
        for x in cnt:
            if x == 1:
                c = cnt[1]
                ans = max(ans, c if c % 2 == 1 else c - 1)
                continue
            depth = 0
            v = x
            while cnt.get(v, 0) >= 2:
                depth += 1
                v = v * v
            if cnt.get(v, 0) >= 1:
                candidate = 2 * depth + 1
            else:
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
