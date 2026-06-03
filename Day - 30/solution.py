class Solution:
    def earliestFinishTime(self,landStartTime: List[int],landDuration: List[int],waterStartTime: List[int],waterDuration: List[int],) -> int:
        best_land_done = min(s + d for s, d in zip(landStartTime, landDuration))
        best_water_done = min(s + d for s, d in zip(waterStartTime, waterDuration))
        ans = float("inf")
        for s, d in zip(waterStartTime, waterDuration):
            ans = min(ans, max(best_land_done, s) + d)
        for s, d in zip(landStartTime, landDuration):
            ans = min(ans, max(best_water_done, s) + d)
        return ans


# ── Brute-force reference (O(n·m)) — only for cross-checking on small inputs ──
class SolutionBrute:
    def earliestFinishTime(self, landStartTime, landDuration, waterStartTime, waterDuration) -> int:
        best = float("inf")
        for i in range(len(landStartTime)):
            ld = landStartTime[i] + landDuration[i]
            for j in range(len(waterStartTime)):
                wd = waterStartTime[j] + waterDuration[j]
                f1 = max(ld, waterStartTime[j]) + waterDuration[j]
                f2 = max(wd, landStartTime[i]) + landDuration[i]
                best = min(best, f1, f2)
        return best


# ── Quick tests ──────────────────────────────────────────────────────────────
if __name__ == "__main__":
    sol = Solution()
    print(sol.earliestFinishTime([2, 8], [4, 1], [6], [3]))        # 9
    print(sol.earliestFinishTime([5], [3], [1], [10]))             # 14
    print(sol.earliestFinishTime([1], [1], [1], [1]))              # 3
    print(sol.earliestFinishTime([10], [5], [1], [1]))             # 15
    print(sol.earliestFinishTime([1, 2, 3], [1, 1, 1], [5], [2]))  # 7

    # Randomized cross-check: linear must equal brute force everywhere.
    import random
    brute = SolutionBrute()
    for _ in range(2000):
        n = random.randint(1, 6)
        m = random.randint(1, 6)
        ls = [random.randint(1, 20) for _ in range(n)]
        ld = [random.randint(1, 20) for _ in range(n)]
        ws = [random.randint(1, 20) for _ in range(m)]
        wd = [random.randint(1, 20) for _ in range(m)]
        a = sol.earliestFinishTime(ls, ld, ws, wd)
        b = brute.earliestFinishTime(ls, ld, ws, wd)
        assert a == b, (ls, ld, ws, wd, a, b)
    print("randomized cross-check passed ✓")
