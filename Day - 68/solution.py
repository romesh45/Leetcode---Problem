from typing import List
from collections import defaultdict


class Solution:
    def countCompleteComponents(self, n: int, edges: List[List[int]]) -> int:
        # A component with k nodes is complete iff it has exactly k*(k-1)//2 edges.
        # So: find components, count nodes and edges per component, check the formula.

        # Union-Find with path compression + union by rank
        parent = list(range(n))
        rank   = [0] * n

        def find(x: int) -> int:
            while parent[x] != x:
                parent[x] = parent[parent[x]]  # path halving
                x = parent[x]
            return x

        def union(x: int, y: int) -> None:
            px, py = find(x), find(y)
            if px == py:
                return
            if rank[px] < rank[py]:
                px, py = py, px
            parent[py] = px
            if rank[px] == rank[py]:
                rank[px] += 1

        for a, b in edges:
            union(a, b)

        # Tally nodes and edges per component root
        node_cnt = defaultdict(int)
        edge_cnt = defaultdict(int)

        for i in range(n):
            node_cnt[find(i)] += 1

        for a, b in edges:
            edge_cnt[find(a)] += 1  # find(a) == find(b) inside same component

        # Count complete components
        return sum(
            1
            for root, k in node_cnt.items()
            if edge_cnt[root] == k * (k - 1) // 2
        )


# ── Quick tests ───────────────────────────────────────────────────────────────
if __name__ == "__main__":
    sol = Solution()

    print(sol.countCompleteComponents(6, [[0,1],[0,2],[1,2],[3,4]]))        # 3
    print(sol.countCompleteComponents(6, [[0,1],[0,2],[1,2],[3,4],[3,5]]))  # 1

    # Edge cases
    print(sol.countCompleteComponents(1, []))                               # 1  single node
    print(sol.countCompleteComponents(3, []))                               # 3  all isolated
    print(sol.countCompleteComponents(4, [[0,1],[1,2],[2,3],[3,0],[0,2],[1,3]]))  # 1  K4
    print(sol.countCompleteComponents(4, [[0,1],[2,3]]))                    # 2  two K2s
