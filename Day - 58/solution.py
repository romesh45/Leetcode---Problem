from typing import List
from collections import deque


class Solution:
    def maximumSafenessFactor(self, grid: List[List[int]]) -> int:
        # ── Step 1: Multi-source BFS from every thief ────────────────────────
        # dist[r][c] = Manhattan distance from (r,c) to the nearest thief.
        # Launch BFS simultaneously from all thieves; the first time BFS
        # reaches a cell is the shortest distance (by BFS level property).
        n = len(grid)
        dist = [[-1] * n for _ in range(n)]
        q = deque()

        for r in range(n):
            for c in range(n):
                if grid[r][c] == 1:
                    dist[r][c] = 0
                    q.append((r, c))

        dirs = [(0, 1), (0, -1), (1, 0), (-1, 0)]
        while q:
            r, c = q.popleft()
            for dr, dc in dirs:
                nr, nc = r + dr, c + dc
                if 0 <= nr < n and 0 <= nc < n and dist[nr][nc] == -1:
                    dist[nr][nc] = dist[r][c] + 1
                    q.append((nr, nc))

        # ── Step 2: Binary search on the safeness factor k ──────────────────
        # We want the maximum k such that a path exists from (0,0) to (n-1,n-1)
        # using only cells where dist >= k.
        #
        # Feasibility check: BFS/DFS on the subgraph of cells with dist >= k.
        # If (0,0) or (n-1,n-1) have dist < k, it's immediately infeasible.

        def can_reach(k: int) -> bool:
            if dist[0][0] < k or dist[n - 1][n - 1] < k:
                return False
            visited = [[False] * n for _ in range(n)]
            visited[0][0] = True
            bfs = deque([(0, 0)])
            while bfs:
                r, c = bfs.popleft()
                if r == n - 1 and c == n - 1:
                    return True
                for dr, dc in dirs:
                    nr, nc = r + dr, c + dc
                    if (0 <= nr < n and 0 <= nc < n
                            and not visited[nr][nc]
                            and dist[nr][nc] >= k):
                        visited[nr][nc] = True
                        bfs.append((nr, nc))
            return False

        # k ranges from 0 (always reachable — any cell works) to n (max possible).
        # Binary search for the largest feasible k.
        lo, hi = 0, n
        while lo < hi:
            mid = (lo + hi + 1) // 2   # upper-mid to avoid infinite loop
            if can_reach(mid):
                lo = mid
            else:
                hi = mid - 1

        return lo


# ── Quick tests ───────────────────────────────────────────────────────────────
if __name__ == "__main__":
    sol = Solution()

    print(sol.maximumSafenessFactor([[1, 0, 0], [0, 0, 0], [0, 0, 1]]))              # 0
    print(sol.maximumSafenessFactor([[0, 0, 1], [0, 0, 0], [0, 0, 0]]))              # 2
    print(sol.maximumSafenessFactor([[0, 0, 0, 1], [0, 0, 0, 0],
                                     [0, 0, 0, 0], [1, 0, 0, 0]]))                   # 2

    # Edge: start/end are thieves → 0
    print(sol.maximumSafenessFactor([[1, 0], [0, 0]]))                               # 0

    # Timing on worst-case n=400
    import time
    n = 400
    big = [[0] * n for _ in range(n)]
    big[0][n - 1] = 1
    big[n - 1][0] = 1
    t0 = time.time()
    print(sol.maximumSafenessFactor(big))
    print(f"n=400 timing: {time.time()-t0:.3f}s")
