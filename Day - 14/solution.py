class Solution:
    def minJumps(self, arr: List[int]) -> int:
        n = len(arr)
        if n == 1:
            return 0
        buckets = defaultdict(list)
        for i, v in enumerate(arr):
            buckets[v].append(i)
        visited = [False] * n
        visited[0] = True
        queue = deque([(0, 0)])
        while queue:
            i, steps = queue.popleft()
            for nxt in self._neighbors(i, n, arr, buckets):
                if nxt == n - 1:
                    return steps + 1

                if not visited[nxt]:
                    visited[nxt] = True
                    queue.append((nxt, steps + 1))
            buckets[arr[i]].clear()

        return -1

    @staticmethod
    def _neighbors(i, n, arr, buckets):
        """Yield i+1, i-1, and all same-value indices for current i."""
        if i + 1 < n:
            yield i + 1
        if i - 1 >= 0:
            yield i - 1
        yield from buckets[arr[i]]


# ── Quick tests ──────────────────────────────────────────────────────────────
if __name__ == "__main__":
    sol = Solution()
    print(sol.minJumps([100, -23, -23, 404, 100, 23, 23, 23, 3, 404]))   # 3
    print(sol.minJumps([7]))                                              # 0
    print(sol.minJumps([7, 6, 9, 6, 9, 6, 9, 7]))                         # 1
    print(sol.minJumps([6, 1, 9]))                                        # 2  (6→1→9)
    print(sol.minJumps([11, 22, 7, 7, 7, 7, 7, 7, 7, 22, 13]))            # 3  (11→22(idx1)→22(idx9)→13)
    print(sol.minJumps([-76, 3, 66, -32, 64, 2, -19, -8, -5, -93, 80, -5, -76, -78, 64, 2, 16]))  # 5
