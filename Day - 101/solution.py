from typing import List


class Solution:
    def longestRepeating(self, s: str, queryCharacters: str, queryIndices: List[int]) -> List[int]:
        n = len(s)
        s = list(s)

        # Segment tree -- each node stores for its range:
        #   lc : leftmost character
        #   rc : rightmost character
        #   ll : length of the uniform run at the LEFT end
        #   rl : length of the uniform run at the RIGHT end
        #   ml : maximum run length anywhere in the range
        #   ln : total length of the range
        lc = [''] * (4 * n)
        rc = [''] * (4 * n)
        ll = [0] * (4 * n)
        rl = [0] * (4 * n)
        ml = [0] * (4 * n)
        ln = [0] * (4 * n)

        def pull(v):
            L, R = v << 1, v << 1 | 1
            lc[v] = lc[L];  rc[v] = rc[R];  ln[v] = ln[L] + ln[R]
            # Left run may extend into R if all of L is the same char as lc[R]
            ll[v] = ll[L] + ll[R] if ll[L] == ln[L] and lc[L] == lc[R] else ll[L]
            # Right run may extend into L if all of R is the same char as rc[L]
            rl[v] = rl[R] + rl[L] if rl[R] == ln[R] and rc[R] == rc[L] else rl[R]
            # Cross-boundary run at the seam
            cross = rl[L] + ll[R] if rc[L] == lc[R] else 0
            ml[v] = max(ml[L], ml[R], cross)

        def build(v, lo, hi):
            if lo == hi:
                lc[v] = rc[v] = s[lo]
                ll[v] = rl[v] = ml[v] = ln[v] = 1
                return
            mid = (lo + hi) >> 1
            build(v << 1, lo, mid);  build(v << 1 | 1, mid + 1, hi)
            pull(v)

        def update(v, lo, hi, idx, ch):
            if lo == hi:
                lc[v] = rc[v] = ch
                return
            mid = (lo + hi) >> 1
            if idx <= mid:
                update(v << 1, lo, mid, idx, ch)
            else:
                update(v << 1 | 1, mid + 1, hi, idx, ch)
            pull(v)

        build(1, 0, n - 1)

        ans = []
        for ch, idx in zip(queryCharacters, queryIndices):
            s[idx] = ch
            update(1, 0, n - 1, idx, ch)
            ans.append(ml[1])
        return ans


# Quick tests
if __name__ == "__main__":
    sol = Solution()

    print(sol.longestRepeating("babacc", "bcb", [1, 3, 3]))   # [3, 3, 4]
    print(sol.longestRepeating("abyzz",  "aa",  [2, 1]))      # [2, 3]
