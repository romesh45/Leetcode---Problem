class Solution:
    def countSubarrays(self, nums: List[int], target: int) -> int:
        n = len(nums)
        prefix = [0] * (n + 1)
        for i in range(n):
            prefix[i + 1] = prefix[i] + (1 if nums[i] == target else -1)
        sorted_vals = sorted(set(prefix))
        rank = {v: i + 1 for i, v in enumerate(sorted_vals)}   
        m = len(sorted_vals)
        bit = [0] * (m + 1)
        def update(i: int) -> None:
            """Increment position i by 1."""
            while i <= m:
                bit[i] += 1
                i += i & (-i)
        def query(i: int) -> int:
            """Sum of positions 1..i (i.e., count of values with rank ≤ i)."""
            s = 0
            while i > 0:
                s += bit[i]
                i -= i & (-i)
            return s
        count = 0
        for k in range(n + 1):
            r = rank[prefix[k]]
            if k > 0:
                count += query(r - 1)
            update(r)   
        return count


# ── Reference: O(n²) from Part I — correct, only usable for small n ──────────
class SolutionBrute:
    def countSubarrays(self, nums: List[int], target: int) -> int:
        n = len(nums)
        count = 0
        for i in range(n):
            for j in range(i, n):
                sub = nums[i:j + 1]
                if sub.count(target) * 2 > len(sub):
                    count += 1
        return count


# ── Quick tests ───────────────────────────────────────────────────────────────
if __name__ == "__main__":
    sol = Solution()

    print(sol.countSubarrays([1, 2, 2, 3], 2))   # 5
    print(sol.countSubarrays([1, 1, 1, 1], 1))   # 10
    print(sol.countSubarrays([1, 2, 3], 4))       # 0

    # Edge cases
    print(sol.countSubarrays([5], 5))             # 1
    print(sol.countSubarrays([5], 3))             # 0
    print(sol.countSubarrays([2, 2, 2, 2], 2))   # 10

    # Randomised cross-check
    import random
    random.seed(42)
    ref = SolutionBrute()
    for _ in range(2000):
        n = random.randint(1, 20)
        nums = [random.randint(1, 5) for _ in range(n)]
        t = random.randint(1, 5)
        a = sol.countSubarrays(nums, t)
        b = ref.countSubarrays(nums, t)
        assert a == b, f"MISMATCH nums={nums} target={t}: got {a} expected {b}"
    print("randomised cross-check passed ✓")

    # Timing on worst-case n
    import time
    big = [random.randint(1, 10**9) for _ in range(10**5)]
    t0 = time.time()
    sol.countSubarrays(big, big[0])
    print(f"n=10^5 timing: {time.time()-t0:.3f}s")
