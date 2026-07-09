class Solution:
    def pathExistenceQueries(self, n: int, nums: List[int], maxDiff: int,
                             queries: List[List[int]]) -> List[bool]:
        # Key insight: nums is sorted, so connected components are
        # CONTIGUOUS index ranges.
        #
        # Why? For any i < k < j, nums[i] <= nums[k] <= nums[j], so
        # |nums[i] - nums[k]| <= |nums[i] - nums[j]|. If i and j are
        # connected, k is automatically reachable from i too.
        #
        # Consequence: we only need to check consecutive pairs.
        # Nodes i and i+1 are in the same component iff
        # nums[i+1] - nums[i] <= maxDiff.
        # (If this gap is too large, NO node left of i can ever reach
        # any node right of i, because all such differences are even larger.)
        #
        # Build a component ID per node in one pass:
        group = [0] * n
        for i in range(1, n):
            same = nums[i] - nums[i - 1] <= maxDiff
            group[i] = group[i - 1] if same else group[i - 1] + 1

        return [group[u] == group[v] for u, v in queries]


# ── Quick tests ───────────────────────────────────────────────────────────────
if __name__ == "__main__":
    sol = Solution()

    print(sol.pathExistenceQueries(2, [1, 3], 1, [[0,0],[0,1]]))
    # [True, False]

    print(sol.pathExistenceQueries(4, [2, 5, 6, 8], 2, [[0,1],[0,2],[1,3],[2,3]]))
    # [False, False, True, True]

    # Edge cases
    print(sol.pathExistenceQueries(1, [7], 0, [[0,0]]))              # [True]  single node
    print(sol.pathExistenceQueries(3, [1,1,1], 0, [[0,1],[1,2],[0,2]]))  # [True,True,True] all equal
    print(sol.pathExistenceQueries(3, [0,5,10], 4, [[0,1],[1,2],[0,2]]))  # [False,False,False] all isolated
    print(sol.pathExistenceQueries(5, [1,2,3,10,11], 1, [[0,2],[3,4],[0,4]]))  # [True,True,False]
