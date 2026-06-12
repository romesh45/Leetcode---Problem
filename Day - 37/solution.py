class Solution:
    def maxTotalValue(self, nums: List[int], k: int) -> int:
        n = len(nums)
        max_st = [nums[:]]
        min_st = [nums[:]]
        j = 1
        while (1 << j) <= n:
            half = 1 << (j - 1)
            pm, pn = max_st[-1], min_st[-1]
            size = n - (1 << j) + 1
            max_st.append([max(pm[i], pm[i + half]) for i in range(size)])
            min_st.append([min(pn[i], pn[i + half]) for i in range(size)])
            j += 1
        def value(l: int, r: int) -> int:
            """max(nums[l..r]) - min(nums[l..r]) in O(1) via two overlapping blocks."""
            j = (r - l + 1).bit_length() - 1
            hi = max(max_st[j][l], max_st[j][r - (1 << j) + 1])
            lo = min(min_st[j][l], min_st[j][r - (1 << j) + 1])
            return hi - lo
        heap = [(-value(l, n - 1), l, n - 1) for l in range(n)]
        heapq.heapify(heap)
        total = 0
        for _ in range(k):
            v, l, r = heapq.heappop(heap)
            if v == 0:
                break
            total += -v
            if r - 1 >= l:
                heapq.heappush(heap, (-value(l, r - 1), l, r - 1))

        return total


# ── Brute-force reference (O(n²)) — only for cross-checking small inputs ─────
class SolutionBrute:
    def maxTotalValue(self, nums: List[int], k: int) -> int:
        n = len(nums)
        vals = []
        for l in range(n):
            hi = lo = nums[l]
            for r in range(l, n):
                hi = max(hi, nums[r])
                lo = min(lo, nums[r])
                vals.append(hi - lo)
        vals.sort(reverse=True)
        return sum(vals[:k])


# ── Quick tests ────────────────────────────────────────
if __name__ == "__main__":
    sol = Solution()
    print(sol.maxTotalValue([1, 3, 2], 2))          # 4
    print(sol.maxTotalValue([4, 2, 5, 1], 3))       # 12
    print(sol.maxTotalValue([7, 7, 7], 6))          # 0   (all values are 0)
    print(sol.maxTotalValue([5], 1))                # 0   (single element)
    print(sol.maxTotalValue([0, 10**9], 3))         # 10^9 (values: [0]=0, [1e9]=0, [0,1e9]=1e9)

    # Randomized cross-check against brute force.
    import random
    brute = SolutionBrute()
    for _ in range(500):
        n = random.randint(1, 12)
        arr = [random.randint(0, 50) for _ in range(n)]
        kk = random.randint(1, n * (n + 1) // 2)
        a = sol.maxTotalValue(arr, kk)
        b = brute.maxTotalValue(arr, kk)
        assert a == b, (arr, kk, a, b)
    print("randomized cross-check passed ✓")

    # Large-input timing sanity.
    import time
    big = [random.randint(0, 10**9) for _ in range(5 * 10**4)]
    t0 = time.time()
    res = sol.maxTotalValue(big, 10**5)
    print(f"n=5e4, k=1e5 → {res}  ({time.time() - t0:.2f}s)")
