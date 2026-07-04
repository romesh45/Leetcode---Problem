from typing import List
from collections import deque


class Solution:
    def minScore(self, n: int, roads: List[List[int]]) -> int:
        # Key insight: since roads can be traversed multiple times in either
        # direction, any edge in the same connected component as city 1 (and
        # city n) is reachable and usable. The answer is simply the minimum
        # edge weight within that component.
        #
        # Why? If edge (a, b, d) is in the component, we can always construct
        # a valid path: 1 → ... → a → b → a → ... → n, reusing any roads
        # freely. So the minimum edge weight in the component is always
        # achievable.

        # Build adjacency list (1-indexed)
        adj = [[] for _ in range(n + 1)]
        for a, b, d in roads:
            adj[a].append((b, d))
            adj[b].append((a, d))

        # BFS from city 1 to identify every node in its connected component
        visited = {1}
        queue = deque([1])
        while queue:
            node = queue.popleft()
            for neighbor, _ in adj[node]:
                if neighbor not in visited:
                    visited.add(neighbor)
                    queue.append(neighbor)

        # Minimum edge weight among all edges in the component
        # (if one endpoint is visited, the other must be too — undirected graph)
        return min(d for a, b, d in roads if a in visited)


# ── Quick tests ───────────────────────────────────────────────────────────────
if __name__ == "__main__":
    sol = Solution()

    print(sol.minScore(4, [[1,2,9],[2,3,6],[2,4,5],[1,4,7]]))   # 5
    print(sol.minScore(4, [[1,2,2],[1,3,4],[3,4,7]]))            # 2

    # Edge cases
    print(sol.minScore(2, [[1,2,1]]))                            # 1   single edge
    print(sol.minScore(2, [[1,2,10000]]))                        # 10000  max distance
    print(sol.minScore(5, [[1,2,3],[2,3,1],[3,5,4],[4,5,2],[1,4,9]]))  # 1 all connected
