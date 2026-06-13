from collections import deque
from typing import List


class Solution:
    def assignEdgeWeights(self, edges: List[List[int]]) -> int:
        MOD = 10**9 + 7

        # ── Step 1: find the maximum depth d via BFS from the root (node 1) ──
        # d = number of EDGES on the path from node 1 to any deepest node.
        # Which deepest node we pick doesn't matter — only the path LENGTH
        # enters the counting formula.
        n = len(edges) + 1
        adj = [[] for _ in range(n + 1)]
        for u, v in edges:
            adj[u].append(v)
            adj[v].append(u)

        depth = 0
        visited = [False] * (n + 1)
        visited[1] = True
        queue = deque([1])
        while queue:
            for _ in range(len(queue)):          # process one level at a time
                node = queue.popleft()
                for nxt in adj[node]:
                    if not visited[nxt]:
                        visited[nxt] = True
                        queue.append(nxt)
            if queue:                            # a deeper level exists
                depth += 1

        # ── Step 2: count assignments with odd total cost ────────────────────
        # Weight 1 is odd (flips parity), weight 2 is even (doesn't).
        # Cost is odd ⇔ an ODD number of the d edges receive weight 1.
        # #(odd-sized subsets of d items) = C(d,1)+C(d,3)+… = 2^(d-1).
        #
        # Why exactly half: flipping the FIRST edge's weight toggles the total
        # parity — a perfect bijection between odd-cost and even-cost
        # assignments. So half of the 2^d assignments are odd.
        return pow(2, depth - 1, MOD)


# ── Quick tests ──────────────────────────────────────────────────────────────
if __name__ == "__main__":
    sol = Solution()
    print(sol.assignEdgeWeights([[1, 2]]))                            # 1   (d=1)
    print(sol.assignEdgeWeights([[1, 2], [1, 3], [3, 4], [3, 5]]))    # 2   (d=2)
    print(sol.assignEdgeWeights([[1, 2], [2, 3], [3, 4]]))            # 4   (d=3 chain)
    print(sol.assignEdgeWeights([[1, 2], [1, 3]]))                    # 1   (d=1, star)

    # Long chain: d = 10 → 2^9 = 512.
    chain = [[i, i + 1] for i in range(1, 11)]
    print(sol.assignEdgeWeights(chain))                               # 512

    # Brute-force cross-check on small chains: enumerate all 2^d assignments.
    from itertools import product
    for d in range(1, 12):
        ways = sum(1 for combo in product((1, 2), repeat=d) if sum(combo) % 2 == 1)
        assert ways == pow(2, d - 1), (d, ways)
    print("brute-force parity check passed ✓")
