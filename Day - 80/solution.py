"""
3501. Maximize Active Section with Trade II
https://leetcode.com/problems/maximize-active-section-with-trade-ii/
Difficulty: Hard

See README.md for the problem summary and approach write-up.

Complexity: O((n + q) log n) time, O(n log n) space.
"""

import bisect
from typing import List


class Solution:
    def maxActiveSectionsAfterTrade(self, s: str, queries: List[List[int]]) -> List[int]:
        n = len(s)
        ones = s.count('1')

        # zero_runs: (start, end) inclusive, for every maximal run of '0'
        zero_runs = []
        i = 0
        while i < n:
            if s[i] == '0':
                j = i
                while j < n and s[j] == '0':
                    j += 1
                zero_runs.append((i, j - 1))
                i = j
            else:
                i += 1

        m = len(zero_runs)
        if m < 2:
            # Fewer than 2 zero-runs anywhere in s -> no interior 1-run can
            # ever exist, so no trade is ever possible for any query.
            return [ones] * len(queries)

        starts = [z[0] for z in zero_runs]
        ends = [z[1] for z in zero_runs]
        sizes = [e - st + 1 for st, e in zero_runs]

        # pair_sum[i] = sizes[i] + sizes[i + 1]: the gain from the interior
        # 1-run that sits between zero_runs[i] and zero_runs[i + 1], assuming
        # neither zero-run needs to be clipped to a query boundary.
        pair_sum = [sizes[i] + sizes[i + 1] for i in range(m - 1)]
        k = len(pair_sum)

        # Sparse table for O(1) range-max queries over pair_sum.
        LOG = k.bit_length()
        sparse = [pair_sum[:]]
        for level in range(1, LOG + 1):
            half = 1 << (level - 1)
            length = half << 1
            if length > k:
                break
            prev = sparse[-1]
            sparse.append([max(prev[j], prev[j + half]) for j in range(k - length + 1)])

        def query_max(lo: int, hi: int) -> int:
            length = hi - lo + 1
            level = length.bit_length() - 1
            half = 1 << level
            return max(sparse[level][lo], sparse[level][hi - half + 1])

        res = []
        for l, r in queries:
            lo = bisect.bisect_left(ends, l)          # first zero-run with end >= l
            hi = bisect.bisect_right(starts, r) - 1   # last zero-run with start <= r

            if lo >= hi:
                # 0 or 1 zero-runs overlap [l, r] -> no interior 1-run possible.
                res.append(ones)
                continue

            left_clip = ends[lo] - max(starts[lo], l) + 1
            right_clip = min(ends[hi], r) - starts[hi] + 1

            if hi == lo + 1:
                best = left_clip + right_clip
            else:
                best = left_clip + sizes[lo + 1]
                best = max(best, sizes[hi - 1] + right_clip)
                if lo + 1 <= hi - 2:
                    best = max(best, query_max(lo + 1, hi - 2))

            res.append(ones + best)

        return res


if __name__ == "__main__":
    sol = Solution()
    print(sol.maxActiveSectionsAfterTrade("01", [[0, 1]]))
    print(sol.maxActiveSectionsAfterTrade("0100", [[0, 3], [0, 2], [1, 3], [2, 3]]))
    print(sol.maxActiveSectionsAfterTrade("1000100", [[1, 5], [0, 6], [0, 4]]))
    print(sol.maxActiveSectionsAfterTrade("01010", [[0, 3], [1, 4], [1, 3]]))
