from typing import List


class Solution:
    def maximumElementAfterDecrementingAndRearranging(self, arr: List[int]) -> int:
        # We can rearrange freely and decrease any element.
        # Goal: build a valid sequence (arr[0]=1, |arr[i]-arr[i-1]|<=1)
        # that maximises its largest element.
        #
        # Key observation:
        #   To maximise the last value, we want the sequence to climb as
        #   fast as possible: 1, 2, 3, …
        #   Each position i (1-indexed) can hold at most value i.
        #   The element assigned to position i also can't exceed its
        #   original value (we can only decrease).
        #
        # Greedy on sorted array:
        #   Sort arr ascending. For each value v (in order), the best we
        #   can place at the current position is min(v, cur + 1), where
        #   cur is the value placed at the previous position.
        #
        #   - min(v, cur+1): we can't use more than v (only decrease),
        #     and we can't jump more than +1 from cur.
        #   - Sorting ensures we process the smallest values first,
        #     which is optimal: a small value can only block progress
        #     early; a large value can always be decreased to fill any gap.
        #
        # Result after processing all elements = maximum achievable value.
        #
        # Time:  O(n log n)  — dominated by sort
        # Space: O(1)        — sort in-place, single pass

        arr.sort()
        cur = 0
        for v in arr:
            cur = min(v, cur + 1)
        return cur


# ── Quick tests ───────────────────────────────────────────────────────────────
if __name__ == "__main__":
    sol = Solution()

    print(sol.maximumElementAfterDecrementingAndRearranging([2, 2, 1, 2, 1]))   # 2
    print(sol.maximumElementAfterDecrementingAndRearranging([100, 1, 1000]))     # 3
    print(sol.maximumElementAfterDecrementingAndRearranging([1, 2, 3, 4, 5]))   # 5

    # Extra cases
    print(sol.maximumElementAfterDecrementingAndRearranging([5, 5, 5, 5, 5]))   # 5
    print(sol.maximumElementAfterDecrementingAndRearranging([1, 1, 1, 100]))    # 2
    print(sol.maximumElementAfterDecrementingAndRearranging([1]))               # 1
    print(sol.maximumElementAfterDecrementingAndRearranging([1000000000]))      # 1

    import time, random
    random.seed(0)
    big = [random.randint(1, 10**9) for _ in range(10**5)]
    t0 = time.time()
    sol.maximumElementAfterDecrementingAndRearranging(big)
    print(f"n=10^5 timing: {time.time()-t0:.3f}s")
