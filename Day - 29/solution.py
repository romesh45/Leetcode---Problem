class Solution:
    def earliestFinishTime(
        self,
        landStartTime: List[int],
        landDuration: List[int],
        waterStartTime: List[int],
        waterDuration: List[int],
    ) -> int:
        # We must do EXACTLY one land ride and one water ride, in EITHER order.
        #
        # For a fixed pair (land i, water j), the finish time of each order is:
        #
        #   land → water:  max(landStart[i] + landDur[i], waterStart[j]) + waterDur[j]
        #   water → land:  max(waterStart[j] + waterDur[j], landStart[i]) + landDur[i]
        #
        # The max() models "wait for the second ride to open": after finishing
        # the first at time t, we can only board the second at max(t, itsOpen).
        #
        # With n, m ≤ 100 there are ≤ 10^4 pairs — brute-force every pair and
        # both orders, keep the global minimum.
        best = float("inf")

        for i in range(len(landStartTime)):
            land_done = landStartTime[i] + landDuration[i]
            for j in range(len(waterStartTime)):
                water_done = waterStartTime[j] + waterDuration[j]

                # Order 1: land first, then water.
                f1 = max(land_done, waterStartTime[j]) + waterDuration[j]
                # Order 2: water first, then land.
                f2 = max(water_done, landStartTime[i]) + landDuration[i]

                best = min(best, f1, f2)

        return best


# ── O(n + m) variant (the two orders decouple) ───────────────────────────────
# land → water finish only depends on: (min land completion time) and the
# chosen water ride. Symmetric for water → land. So we can precompute the best
# completion time for each category independently.
class SolutionLinear:
    def earliestFinishTime(
        self, landStartTime, landDuration, waterStartTime, waterDuration
    ) -> int:
        # Best (earliest) completion time over all land rides / all water rides.
        best_land_done = min(s + d for s, d in zip(landStartTime, landDuration))
        best_water_done = min(s + d for s, d in zip(waterStartTime, waterDuration))

        ans = float("inf")

        # land → water: finish land as early as possible, then each water ride.
        for s, d in zip(waterStartTime, waterDuration):
            ans = min(ans, max(best_land_done, s) + d)

        # water → land: finish water as early as possible, then each land ride.
        for s, d in zip(landStartTime, landDuration):
            ans = min(ans, max(best_water_done, s) + d)

        return ans


# ── Quick tests ──────────────────────────────────────────────────────────────
if __name__ == "__main__":
    sol = Solution()
    print(sol.earliestFinishTime([2, 8], [4, 1], [6], [3]))     # 9
    print(sol.earliestFinishTime([5], [3], [1], [10]))          # 14
    print(sol.earliestFinishTime([1], [1], [1], [1]))           # 3   (1→2 then 2→3)
    print(sol.earliestFinishTime([10], [5], [1], [1]))          # 15  (water first: 1→2, then land 10→15)
    print(sol.earliestFinishTime([1, 2, 3], [1, 1, 1], [5], [2]))  # 7

    # Cross-check the linear variant matches brute force.
    sol2 = SolutionLinear()
    print(sol2.earliestFinishTime([2, 8], [4, 1], [6], [3]))    # 9
    print(sol2.earliestFinishTime([5], [3], [1], [10]))         # 14
    print(sol2.earliestFinishTime([1, 2, 3], [1, 1, 1], [5], [2]))  # 7
