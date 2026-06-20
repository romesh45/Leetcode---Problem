from typing import List


class Solution:
    def maxBuilding(self, n: int, restrictions: List[List[int]]) -> int:
        # n can be up to 10^9, so we CANNOT touch every building. We only work
        # with the O(m) "anchor" points (the restrictions, plus building 1 fixed
        # at height 0, plus building n with its natural ceiling).
        #
        # Idea: between two anchors the heights form a tent — rising at most +1
        # per step from each side. After tightening each anchor's cap by what
        # its neighbours allow, the tallest building in each gap is closed-form.

        r = [list(x) for x in restrictions]
        r.append([1, 0])                       # building 1 is fixed at height 0
        if all(x[0] != n for x in r):
            r.append([n, n - 1])               # unrestricted n → natural max n-1
        r.sort()
        m = len(r)

        # Forward pass: from a height h at position p, a building d steps to the
        # right can be at most h + d. Tighten each cap by the left neighbour.
        for i in range(1, m):
            r[i][1] = min(r[i][1], r[i - 1][1] + (r[i][0] - r[i - 1][0]))

        # Backward pass: symmetric tightening from the right neighbour.
        for i in range(m - 2, -1, -1):
            r[i][1] = min(r[i][1], r[i + 1][1] + (r[i + 1][0] - r[i][0]))

        # Peak between each adjacent anchor pair.
        ans = 0
        for i in range(1, m):
            lid, lh = r[i - 1]
            rid, rh = r[i]
            # height(pos) ≤ min(lh + (pos-lid), rh + (rid-pos)); the two rising
            # lines meet at height (lh + rh + (rid - lid)) / 2 — floor for ints.
            peak = (lh + rh + (rid - lid)) // 2
            ans = max(ans, peak)

        return ans


# ── Brute force (O(n)) for cross-checking on small n ─────────────────────────
class SolutionBrute:
    def maxBuilding(self, n: int, restrictions: List[List[int]]) -> int:
        INF = float("inf")
        cap = [INF] * (n + 1)
        cap[1] = 0
        for idx, h in restrictions:
            cap[idx] = min(cap[idx], h)
        # Forward then backward relaxation of the |diff| ≤ 1 rule.
        h = [0] * (n + 1)
        h[1] = 0
        for i in range(2, n + 1):
            h[i] = min(cap[i], h[i - 1] + 1)
        for i in range(n - 1, 0, -1):
            h[i] = min(h[i], h[i + 1] + 1)
        return max(h[1:])


# ── Quick tests ──────────────────────────────────────────────────────────────
if __name__ == "__main__":
    sol = Solution()
    print(sol.maxBuilding(5, [[2, 1], [4, 1]]))                       # 2
    print(sol.maxBuilding(6, []))                                     # 5
    print(sol.maxBuilding(10, [[5, 3], [2, 5], [7, 4], [10, 3]]))     # 5
    print(sol.maxBuilding(2, []))                                     # 1
    print(sol.maxBuilding(3, [[2, 0]]))                               # 1  (0,0,1)

    # Randomized cross-check against the O(n) brute force.
    import random
    brute = SolutionBrute()
    for _ in range(3000):
        n = random.randint(2, 40)
        ids = random.sample(range(2, n + 1), random.randint(0, n - 1))
        rs = [[i, random.randint(0, n)] for i in ids]
        a = sol.maxBuilding(n, [r[:] for r in rs])
        b = brute.maxBuilding(n, [r[:] for r in rs])
        assert a == b, (n, rs, a, b)
    print("randomized cross-check passed ✓")

    # Huge-n sanity: 10^9 buildings, a handful of restrictions — must be instant.
    import time
    t0 = time.time()
    res = sol.maxBuilding(10**9, [[2, 0], [10**9, 0], [5 * 10**8, 100]])
    print(f"n=1e9 → {res}  ({time.time() - t0:.4f}s)")
