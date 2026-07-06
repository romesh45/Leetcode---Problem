from typing import List


class Solution:
    def removeCoveredIntervals(self, intervals: List[List[int]]) -> int:
        # [a,b] is covered by [c,d] if c <= a and b <= d.
        # Goal: count intervals NOT covered by any other.
        #
        # Sort by left ascending, right DESCENDING.
        # After sorting, every interval we've already seen has left <= current left.
        # So the only remaining question for coverage is the right endpoint:
        # if any previous interval's right >= current right, current is covered.
        # Tracking max_right seen so far captures this in O(1) per step.
        #
        # Why right descending on ties:
        # When two intervals share the same left, the wider one must come first.
        # That way the narrower one is immediately recognised as covered
        # (max_right from the wider interval already >= narrower's right).
        #
        # Time:  O(n log n) — sort
        # Space: O(1)       — single pass, no extra storage

        intervals.sort(key=lambda x: (x[0], -x[1]))

        remaining = 0
        max_right = 0

        for l, r in intervals:
            if r > max_right:       # not covered by anything seen so far
                remaining += 1
                max_right = r
            # else: a previous interval already spans [l, r] — covered, skip

        return remaining


# ── Reference: O(n²) brute force ─────────────────────────────────────────────
class SolutionBrute:
    def removeCoveredIntervals(self, intervals: List[List[int]]) -> int:
        count = 0
        for i, (a, b) in enumerate(intervals):
            if not any(c <= a and b <= d
                       for j, (c, d) in enumerate(intervals) if j != i):
                count += 1
        return count


# ── Quick tests ───────────────────────────────────────────────────────────────
if __name__ == "__main__":
    sol = Solution()

    print(sol.removeCoveredIntervals([[1,4],[3,6],[2,8]]))    # 2
    print(sol.removeCoveredIntervals([[1,4],[2,3]]))           # 1
    print(sol.removeCoveredIntervals([[1,2]]))                 # 1
    print(sol.removeCoveredIntervals([[1,4],[1,6],[1,8]]))    # 1  (all same left)
    print(sol.removeCoveredIntervals([[0,10],[5,12],[0,15]])) # 1  ([0,15] covers all)

    import random
    random.seed(0)
    ref = SolutionBrute()
    errors = 0
    for _ in range(2000):
        ivs = list({(random.randint(0, 10), random.randint(1, 11))
                    for _ in range(random.randint(1, 10))})
        ivs = [[l, r] for l, r in ivs if l < r]
        if not ivs:
            continue
        a = sol.removeCoveredIntervals([x[:] for x in ivs])
        b = ref.removeCoveredIntervals(ivs)
        if a != b:
            print(f"MISMATCH {ivs}: got {a} expected {b}")
            errors += 1
    print("2000 random tests passed ✓" if not errors else f"errors: {errors}")
