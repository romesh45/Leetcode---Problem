from typing import List
from collections import deque


class Solution:
    def findSafeWalk(self, grid: List[List[int]], health: int) -> bool:
        # Reframe: each unsafe cell (1) costs 1 health; safe cells (0) cost 0.
        # "Can we reach (m-1,n-1) with health ≥ 1 remaining?"
        # ⟺ "Is the minimum total damage along any path < health?"
        #
        # This is a shortest-path problem with edge weights 0 or 1.
        # 0-1 BFS solves it in O(m*n) — faster than Dijkstra's O(m*n log(m*n)).
        #
        # 0-1 BFS trick:
        #   Moving to a safe cell (cost 0) → push to FRONT of deque (like free move)
        #   Moving to an unsafe cell (cost 1) → push to BACK  of deque (like normal step)
        # This maintains the deque sorted by cost so popleft() always gives
        # the cheapest unvisited cell, exactly like Dijkstra but O(1) per operation.
        #
        # cost[r][c] = minimum health lost to reach (r, c) from (0, 0)
        # Answer: cost[m-1][n-1] < health
        #   (need to absorb strictly fewer hits than health, keeping ≥ 1 remaining)

        m, n = len(grid), len(grid[0])

        cost = [[float('inf')] * n for _ in range(m)]
        cost[0][0] = grid[0][0]   # starting cell may itself be unsafe

        dq = deque([(0, 0)])
        dirs = [(0, 1), (0, -1), (1, 0), (-1, 0)]

        while dq:
            r, c = dq.popleft()
            for dr, dc in dirs:
                nr, nc = r + dr, c + dc
                if 0 <= nr < m and 0 <= nc < n:
                    new_cost = cost[r][c] + grid[nr][nc]
                    if new_cost < cost[nr][nc]:
                        cost[nr][nc] = new_cost
                        if grid[nr][nc] == 1:
                            dq.append((nr, nc))      # cost +1 → back
                        else:
                            dq.appendleft((nr, nc))  # cost +0 → front

        return cost[m - 1][n - 1] < health


# ── Reference: BFS tracking remaining health ─────────────────────────────────
class SolutionBrute:
    def findSafeWalk(self, grid: List[List[int]], health: int) -> bool:
        m, n = len(grid), len(grid[0])
        dirs = [(0,1),(0,-1),(1,0),(-1,0)]
        start_h = health - grid[0][0]
        if start_h <= 0:
            return False
        best = {(0, 0): start_h}
        q = deque([(0, 0, start_h)])
        while q:
            r, c, h = q.popleft()
            if r == m - 1 and c == n - 1:
                return True
            for dr, dc in dirs:
                nr, nc = r + dr, c + dc
                if 0 <= nr < m and 0 <= nc < n:
                    nh = h - grid[nr][nc]
                    if nh > 0 and best.get((nr, nc), 0) < nh:
                        best[(nr, nc)] = nh
                        q.append((nr, nc, nh))
        return False


# ── Quick tests ───────────────────────────────────────────────────────────────
if __name__ == "__main__":
    sol = Solution()

    print(sol.findSafeWalk([[0,1,0,0,0],[0,1,0,1,0],[0,0,0,1,0]], 1))              # True
    print(sol.findSafeWalk([[0,1,1,0,0,0],[1,0,1,0,0,0],[0,1,1,1,0,1],[0,0,1,0,1,0]], 3))  # False
    print(sol.findSafeWalk([[1,1,1],[1,0,1],[1,1,1]], 5))                           # True

    # Edge cases
    print(sol.findSafeWalk([[0,0],[0,0]], 1))    # True  (no damage, health stays 1)
    print(sol.findSafeWalk([[1]], 1))             # False (start=end is unsafe, health → 0)
    print(sol.findSafeWalk([[0]], 1))             # True  (single safe cell)

    # Randomised cross-check
    import random
    random.seed(0)
    ref = SolutionBrute()
    for _ in range(2000):
        m = random.randint(1, 6)
        n = random.randint(1, 6)
        if m * n < 2:
            continue
        grid = [[random.randint(0, 1) for _ in range(n)] for _ in range(m)]
        health = random.randint(1, m + n)
        a = sol.findSafeWalk(grid, health)
        b = ref.findSafeWalk(grid, health)
        assert a == b, f"MISMATCH grid={grid} health={health}: got {a} expected {b}"
    print("randomised cross-check passed ✓")
