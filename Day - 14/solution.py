from collections import defaultdict, deque
from typing import List


class Solution:
    def minJumps(self, arr: List[int]) -> int:
        n = len(arr)
        if n == 1:
            # Already at the last index — zero jumps needed.
            return 0

        # ── Pre-compute value → list of indices (the "teleport buckets") ──
        # From any index i we can jump to any j with arr[i] == arr[j], so we
        # pre-group indices by value and look them up in O(1) during BFS.
        buckets = defaultdict(list)
        for i, v in enumerate(arr):
            buckets[v].append(i)

        # ── BFS for shortest unweighted path from 0 to n - 1 ──
        visited = [False] * n
        visited[0] = True
        queue = deque([(0, 0)])  # (index, steps_taken_to_reach_index)

        while queue:
            i, steps = queue.popleft()

            # Enumerate all neighbours of i:
            #   • i + 1, i - 1            (the linear moves)
            #   • every index in buckets[arr[i]]   (the teleport moves)
            for nxt in self._neighbors(i, n, arr, buckets):
                # Goal-on-enqueue: return as soon as we *see* n-1 as a neighbour.
                # Saves one queue rotation.
                if nxt == n - 1:
                    return steps + 1

                if not visited[nxt]:
                    visited[nxt] = True
                    queue.append((nxt, steps + 1))

            # CRITICAL O(n) trick — clear this value's bucket after first use.
            #
            # When we processed the first index with value v = arr[i], BFS just
            # enqueued every other index sharing that value (those edges are
            # bidirectional in unweighted BFS). A future index with the same
            # value v will iterate the same bucket again and find ALL entries
            # already visited — pure wasted work, O(n) per visit.
            #
            # Worst-case input without this line: [7,7,7,...,7] degrades to O(n²).
            buckets[arr[i]].clear()

        return -1  # Unreachable on valid inputs, but keep for safety.

    @staticmethod
    def _neighbors(i, n, arr, buckets):
        """Yield i+1, i-1, and all same-value indices for current i."""
        if i + 1 < n:
            yield i + 1
        if i - 1 >= 0:
            yield i - 1
        # Note: bucket may be empty here (cleared on a previous visit) — fine.
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
