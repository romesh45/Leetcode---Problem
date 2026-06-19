from typing import List


class Solution:
    def largestAltitude(self, gain: List[int]) -> int:
        # The altitude at each point is a running PREFIX SUM of `gain`, starting
        # from 0 at point 0. We only need the maximum, so carry a running
        # altitude and a running best — no need to store the full array.
        altitude = 0
        highest = 0          # point 0 has altitude 0 and is always a candidate

        for g in gain:
            altitude += g    # advance to the next point
            if altitude > highest:
                highest = altitude

        return highest


# ── One-liner variant (same idea) ────────────────────────────────────────────
class SolutionOneLiner:
    def largestAltitude(self, gain: List[int]) -> int:
        from itertools import accumulate
        return max(0, *accumulate(gain))   # 0 guards the start point


# ── Quick tests ──────────────────────────────────────────────────────────────
if __name__ == "__main__":
    sol = Solution()
    print(sol.largestAltitude([-5, 1, 5, 0, -7]))           # 1
    print(sol.largestAltitude([-4, -3, -2, -1, 4, 3, 2]))   # 0
    print(sol.largestAltitude([1, 2, 3]))                   # 6  (0,1,3,6)
    print(sol.largestAltitude([-1, -2, -3]))                # 0  (start is highest)
    print(sol.largestAltitude([44, 32, -9, 52, 23, -50, 50, 33, -84, 47, -14, 48]))  # 175

    sol2 = SolutionOneLiner()
    print(sol2.largestAltitude([-5, 1, 5, 0, -7]))          # 1
    print(sol2.largestAltitude([-4, -3, -2, -1, 4, 3, 2]))  # 0
