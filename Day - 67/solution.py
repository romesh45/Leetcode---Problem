from typing import List


class Solution:
    def pathExistenceQueries(self, n: int, nums: List[int], maxDiff: int,
                             queries: List[List[int]]) -> List[int]:
        LOG = 17  # 2^17 = 131072 > 10^5

        # ── Step 1: sort nodes by value, record each node's sorted position ──
        order = sorted(range(n), key=lambda i: nums[i])
        svals = [nums[v] for v in order]   # sorted values
        pos = [0] * n
        for k, v in enumerate(order):
            pos[v] = k

        # ── Step 2: right[k] = rightmost sorted position reachable in 1 hop ─
        # Since svals is non-decreasing, a two-pointer gives this in O(n).
        # right[k] is itself non-decreasing (larger k → larger svals[k]
        # → window [svals[k], svals[k]+maxDiff] shifts right).
        right = [0] * n
        r = 0
        for k in range(n):
            r = max(r, k)
            while r + 1 < n and svals[r + 1] - svals[k] <= maxDiff:
                r += 1
            right[k] = r

        # ── Step 3: binary lifting ────────────────────────────────────────────
        # jump[p][k] = rightmost sorted position reachable from k in 2^p hops.
        # Recurrence: jump[p][k] = jump[p-1][ jump[p-1][k] ]
        #   (go as far right as possible in 2^(p-1) hops, then repeat)
        jump = [right[:]]
        for _ in range(1, LOG):
            prev = jump[-1]
            jump.append([prev[prev[k]] for k in range(n)])

        # ── Step 4: answer each query ─────────────────────────────────────────
        # Theorem: going LEFT in sorted order is never beneficial.
        # Proof: right[i] is non-decreasing, so from any i' < i, right[i'] <= right[i].
        # Any rightward jump reachable via a leftward detour i → i' → j can be
        # achieved directly from i in one hop, since j <= right[i'] <= right[i].
        # Therefore the minimum hops = minimum rightward jumps from pos[u] to pos[v].
        #
        # Algorithm (greedy / binary lifting):
        # Repeatedly take the largest power-of-2 jump that doesn't yet reach b.
        # One final hop completes the journey (if u and v are connected).
        results = []
        for u, v in queries:
            a, b = pos[u], pos[v]
            if a > b:
                a, b = b, a
            if a == b:
                results.append(0)
                continue

            steps, cur = 0, a
            for p in range(LOG - 1, -1, -1):
                if jump[p][cur] < b:
                    steps += 1 << p
                    cur = jump[p][cur]

            results.append(steps + 1 if right[cur] >= b else -1)

        return results


# ── Quick tests ───────────────────────────────────────────────────────────────
if __name__ == "__main__":
    sol = Solution()

    print(sol.pathExistenceQueries(5, [1,8,3,4,2], 3, [[0,3],[2,4]]))
    # [1, 1]

    print(sol.pathExistenceQueries(5, [5,3,1,9,10], 2, [[0,1],[0,2],[2,3],[4,3]]))
    # [1, 2, -1, 1]

    print(sol.pathExistenceQueries(3, [3,6,1], 1, [[0,0],[0,1],[1,2]]))
    # [0, -1, -1]

    # Edge cases
    print(sol.pathExistenceQueries(1, [5], 0, [[0,0]]))                        # [0]  single node
    print(sol.pathExistenceQueries(2, [1,1], 0, [[0,1],[1,0]]))                # [1, 1]  same val maxDiff=0
    print(sol.pathExistenceQueries(4, [1,2,3,4], 1, [[0,3],[0,1],[1,3]]))     # [3, 1, 2]  chain
    print(sol.pathExistenceQueries(3, [0,5,10], 4, [[0,1],[1,2],[0,2]]))      # [-1,-1,-1] gaps > maxDiff
