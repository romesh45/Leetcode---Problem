from typing import List
from collections import deque


class Solution:
    def findMaxPathScore(self, edges: List[List[int]], online: List[bool], k: int) -> int:
        INF = float('inf')
        n = len(online)  # n == online.length per constraints

        # Build adjacency list and compute in-degrees for topological sort
        adj = [[] for _ in range(n)]
        in_deg = [0] * n
        for u, v, c in edges:
            adj[u].append((v, c))
            in_deg[v] += 1

        # Topological sort via Kahn's algorithm — computed ONCE and reused
        queue = deque(i for i in range(n) if in_deg[i] == 0)
        topo = []
        while queue:
            node = queue.popleft()
            topo.append(node)
            for v, _ in adj[node]:
                in_deg[v] -= 1
                if in_deg[v] == 0:
                    queue.append(v)

        last = n - 1

        def feasible(min_cost: int) -> bool:
            """
            True iff a path 0 → n-1 exists satisfying all three constraints:
              1. Every edge on the path has cost >= min_cost.
              2. Every intermediate node is online.
              3. Total edge cost <= k.

            Strategy: DAG DP in topological order.
              dp[v] = minimum total cost to reach v from 0, using only
                      edges with cost >= min_cost and online intermediate nodes.
            """
            dp = [INF] * n
            dp[0] = 0
            for node in topo:
                if dp[node] == INF:
                    continue
                # Offline intermediate nodes are forbidden on any valid path
                if node != 0 and node != last and not online[node]:
                    continue
                for v, c in adj[node]:
                    if c < min_cost:
                        continue
                    if v != last and not online[v]:
                        continue
                    new_cost = dp[node] + c
                    if new_cost < dp[v]:
                        dp[v] = new_cost
            return dp[last] <= k

        # Quick check: does any valid path exist at all (no min-cost filter)?
        if not feasible(0):
            return -1

        # Binary search over sorted unique edge costs.
        #
        # Why binary search works:
        #   If feasible(v) is True, then feasible(v') is also True for all v' < v
        #   (a valid path for min_cost v remains valid when we lower the threshold).
        #   So feasible is monotonically non-increasing → classic binary search.
        #
        # Why the answer must be an edge cost:
        #   The path score = min edge cost along the path, which equals
        #   the cost of some actual edge.  Searching only unique edge costs is exact.
        costs = sorted(set(c for _, _, c in edges))
        lo, hi = 0, len(costs) - 1
        result = -1
        while lo <= hi:
            mid = (lo + hi) // 2
            if feasible(costs[mid]):
                result = costs[mid]
                lo = mid + 1   # try for an even higher minimum edge cost
            else:
                hi = mid - 1

        return result


# ── Quick tests ───────────────────────────────────────────────────────────────
if __name__ == "__main__":
    sol = Solution()

    # Provided examples
    print(sol.findMaxPathScore([[0,1,5],[1,3,10],[0,2,3],[2,3,4]],
                               [True,True,True,True], 10))                             # 3

    print(sol.findMaxPathScore([[0,1,7],[1,4,5],[0,2,6],[2,3,6],[3,4,2],[2,4,6]],
                               [True,True,True,False,True], 12))                       # 6

    # Edge cases
    print(sol.findMaxPathScore([[0,1,5]], [True,True], 4))                             # -1  exceeds k
    print(sol.findMaxPathScore([[0,1,5]], [True,True], 5))                             # 5   exact k
    print(sol.findMaxPathScore([[0,1,3],[1,2,3]], [True,False,True], 10))              # -1  middle offline
    print(sol.findMaxPathScore([[0,1,3],[1,2,3],[0,2,10]], [True,False,True], 10))     # 10  bypass offline
    print(sol.findMaxPathScore([], [True,True], 100))                                  # -1  no edges
