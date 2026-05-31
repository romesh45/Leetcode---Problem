from sortedcontainers import SortedList
from typing import List


class SegTree:
    """Iterative max segment tree: point-assign + inclusive range-max query."""

    def __init__(self, n: int):
        self.size = 1
        while self.size < n:
            self.size <<= 1
        self.tree = [0] * (2 * self.size)

    def update(self, i: int, val: int) -> None:
        i += self.size
        self.tree[i] = val
        i >>= 1
        while i:
            self.tree[i] = max(self.tree[2 * i], self.tree[2 * i + 1])
            i >>= 1

    def query(self, l: int, r: int) -> int:        # inclusive [l, r]
        res = 0
        l += self.size
        r += self.size + 1
        while l < r:
            if l & 1:
                res = max(res, self.tree[l]); l += 1
            if r & 1:
                r -= 1; res = max(res, self.tree[r])
            l >>= 1; r >>= 1
        return res


class Solution:
    def getResults(self, queries: List[List[int]]) -> List[bool]:
        # ── Model ─────────────────────────────────────────────────────────────
        # Obstacles partition [0, ∞) into gaps. A block of size sz fits in
        # [0, x] iff some usable gap of length ≥ sz lies inside [0, x].
        #
        # Two kinds of usable gaps:
        #   (a) FULL gaps between two consecutive obstacles BOTH ≤ x.
        #       Store each at its RIGHT endpoint: seg[p] = p - prev(p).
        #       Then seg.query(0, x) = largest full gap entirely inside [0, x]
        #       (gaps whose right endpoint > x are naturally excluded).
        #   (b) The TRAILING partial gap from the last obstacle ≤ x up to x:
        #       partial = x - last.  (Segment tree can't model this — its right
        #       boundary is x, not an obstacle.)
        #
        # Answer: max(full_gap, partial_gap) ≥ sz.
        #
        # We keep an implicit obstacle at position 0 (the left boundary).

        MAXX = max(q[1] for q in queries)
        seg = SegTree(MAXX + 1)
        obstacles = SortedList([0])
        res = []

        for q in queries:
            if q[0] == 1:
                # ── Type 1: build obstacle at x → SPLIT the gap it lands in ──
                x = q[1]
                idx = obstacles.bisect_left(x)
                prev = obstacles[idx - 1]
                seg.update(x, x - prev)              # new gap ending at x
                if idx < len(obstacles):
                    nxt = obstacles[idx]
                    seg.update(nxt, nxt - x)         # successor's gap shrinks
                obstacles.add(x)
            else:
                # ── Type 2: can a block of size sz fit within [0, x]? ──
                x, sz = q[1], q[2]
                best = seg.query(0, x)               # (a) largest full gap ≤ x
                last = obstacles[obstacles.bisect_right(x) - 1]
                partial = x - last                   # (b) trailing partial gap
                res.append(max(best, partial) >= sz)

        return res


# ── Quick tests ──────────────────────────────────────────────────────────────
if __name__ == "__main__":
    sol = Solution()
    print(sol.getResults([[1, 2], [2, 3, 3], [2, 3, 1], [2, 2, 2]]))
    # [False, True, True]

    print(sol.getResults([[1, 7], [2, 7, 6], [1, 2], [2, 7, 5], [2, 7, 6]]))
    # [True, True, False]

    # No obstacles before the query → whole [0, x] is free.
    print(sol.getResults([[2, 5, 5], [2, 5, 6]]))          # [True, False]

    # Obstacle exactly at the boundary x → partial gap is 0.
    print(sol.getResults([[1, 4], [2, 4, 4], [2, 4, 5]]))  # [True, False]

    # Multiple obstacles carving the line.
    print(sol.getResults([[1, 5], [1, 10], [2, 10, 5], [2, 10, 6], [2, 7, 5]]))
    # gaps: 0-5 (=5), 5-10(=5). Q[2,10,5]: max full gap 5 ≥5 True.
    #       Q[2,10,6]: 5<6, partial 10-10=0 → False.
    #       Q[2,7,5]: full gaps ≤7 → seg[5]=5; partial 7-5=2 → max(5,2)=5≥5 True.
    # [True, False, True]
