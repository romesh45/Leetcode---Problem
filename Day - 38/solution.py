class Solution:
    def assignEdgeWeights(self, edges: List[List[int]]) -> int:
        MOD = 10**9 + 7
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
            for _ in range(len(queue)):          
                node = queue.popleft()
                for nxt in adj[node]:
                    if not visited[nxt]:
                        visited[nxt] = True
                        queue.append(nxt)
            if queue:                            
                depth += 1
        return pow(2, depth - 1, MOD)


# ── Quick tests ─────────────────────────────────────
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
