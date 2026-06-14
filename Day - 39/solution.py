from collections import deque
from typing import List


class Solution:
    def assignEdgeWeights(self, edges: List[List[int]], queries: List[List[int]]) -> List[int]:
        MOD = 10**9 + 7
        n = len(edges) + 1

        # ── The parity math carries over from version I ───────────────────────
        # A path with d edges has an odd total cost ⇔ an odd number of its
        # edges receive weight 1 → 2^(d-1) assignments (first-edge flip
        # bijection). d == 0 (u == v) → cost 0, even → 0 ways.
        #
        # ── What's new in version II ──────────────────────────────────────────
        # Up to 10^5 arbitrary (u, v) queries. The path length is
        #     d(u, v) = depth[u] + depth[v] - 2 * depth[LCA(u, v)]
        # so we need fast LCA → binary lifting, O(log n) per query.
        adj = [[] for _ in range(n + 1)]
        for u, v in edges:
            adj[u].append(v)
            adj[v].append(u)

        LOG = max(1, n.bit_length())
        depth = [0] * (n + 1)
        up = [[0] * (n + 1) for _ in range(LOG)]   # up[j][v] = 2^j-th ancestor of v

        # BFS from root 1: fills depth[] and immediate parents up[0][].
        visited = [False] * (n + 1)
        visited[1] = True
        up[0][1] = 1                                # root's parent = itself (safe lift)
        queue = deque([1])
        while queue:
            node = queue.popleft()
            for nxt in adj[node]:
                if not visited[nxt]:
                    visited[nxt] = True
                    depth[nxt] = depth[node] + 1
                    up[0][nxt] = node
                    queue.append(nxt)

        # Binary-lifting table: the 2^j-th ancestor is the 2^(j-1)-th ancestor
        # of the 2^(j-1)-th ancestor.
        for j in range(1, LOG):
            upj, upj1 = up[j], up[j - 1]
            for v in range(1, n + 1):
                upj[v] = upj1[upj1[v]]

        def lca(u: int, v: int) -> int:
            if depth[u] < depth[v]:
                u, v = v, u
            # 1) Lift the deeper node up to the same depth.
            diff = depth[u] - depth[v]
            j = 0
            while diff:
                if diff & 1:
                    u = up[j][u]
                diff >>= 1
                j += 1
            if u == v:
                return u
            # 2) Lift both in decreasing powers while they differ; they end
            #    one step below the LCA.
            for j in range(LOG - 1, -1, -1):
                if up[j][u] != up[j][v]:
                    u, v = up[j][u], up[j][v]
            return up[0][u]

        # Precompute powers of 2 — d can reach n - 1; avoids per-query pow().
        pow2 = [1] * n
        for i in range(1, n):
            pow2[i] = pow2[i - 1] * 2 % MOD

        ans = []
        for u, v in queries:
            d = depth[u] + depth[v] - 2 * depth[lca(u, v)]
            ans.append(0 if d == 0 else pow2[d - 1])
        return ans


# ── Brute-force reference for cross-checking (BFS path length per query) ─────
class SolutionBrute:
    def assignEdgeWeights(self, edges, queries):
        MOD = 10**9 + 7
        n = len(edges) + 1
        adj = [[] for _ in range(n + 1)]
        for u, v in edges:
            adj[u].append(v)
            adj[v].append(u)

        def dist(s, t):
            if s == t:
                return 0
            seen = {s}
            q = deque([(s, 0)])
            while q:
                node, d = q.popleft()
                for nxt in adj[node]:
                    if nxt == t:
                        return d + 1
                    if nxt not in seen:
                        seen.add(nxt)
                        q.append((nxt, d + 1))

        out = []
        for u, v in queries:
            d = dist(u, v)
            out.append(0 if d == 0 else pow(2, d - 1, MOD))
        return out


# ── Quick tests ──────────────────────────────────────────────────────────────
if __name__ == "__main__":
    sol = Solution()
    print(sol.assignEdgeWeights([[1, 2]], [[1, 1], [1, 2]]))
    # [0, 1]
    print(sol.assignEdgeWeights([[1, 2], [1, 3], [3, 4], [3, 5]], [[1, 4], [3, 4], [2, 5]]))
    # [2, 1, 4]

    # Randomized cross-check on small random trees.
    import random
    brute = SolutionBrute()
    for _ in range(200):
        n = random.randint(2, 30)
        edges = [[random.randint(1, i), i + 1] for i in range(1, n)]
        qs = [[random.randint(1, n), random.randint(1, n)] for _ in range(20)]
        a = sol.assignEdgeWeights(edges, qs)
        b = brute.assignEdgeWeights(edges, qs)
        assert a == b, (edges, qs, a, b)
    print("randomized cross-check passed ✓")

    # Large-input timing sanity: chain of 10^5 nodes, 10^5 queries.
    import time
    N = 10**5
    chain = [[i, i + 1] for i in range(1, N)]
    qs = [[random.randint(1, N), random.randint(1, N)] for _ in range(10**5)]
    t0 = time.time()
    sol.assignEdgeWeights(chain, qs)
    print(f"n=1e5 chain, q=1e5 → {time.time() - t0:.2f}s")
