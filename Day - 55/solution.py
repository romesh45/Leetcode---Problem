class Solution:
    def maximumElementAfterDecrementingAndRearranging(self, arr: List[int]) -> int:
        arr.sort()
        cur = 0
        for v in arr:
            cur = min(v, cur + 1)
        return cur


# ── Quick tests ───────────────────────────────────────────────────────────────
if __name__ == "__main__":
    sol = Solution()

    print(sol.maximumElementAfterDecrementingAndRearranging([2, 2, 1, 2, 1]))   # 2
    print(sol.maximumElementAfterDecrementingAndRearranging([100, 1, 1000]))     # 3
    print(sol.maximumElementAfterDecrementingAndRearranging([1, 2, 3, 4, 5]))   # 5

    # Extra cases
    print(sol.maximumElementAfterDecrementingAndRearranging([5, 5, 5, 5, 5]))   # 5
    print(sol.maximumElementAfterDecrementingAndRearranging([1, 1, 1, 100]))    # 2
    print(sol.maximumElementAfterDecrementingAndRearranging([1]))               # 1
    print(sol.maximumElementAfterDecrementingAndRearranging([1000000000]))      # 1

    import time, random
    random.seed(0)
    big = [random.randint(1, 10**9) for _ in range(10**5)]
    t0 = time.time()
    sol.maximumElementAfterDecrementingAndRearranging(big)
    print(f"n=10^5 timing: {time.time()-t0:.3f}s")
