from typing import List


class Solution:
    def arrayRankTransform(self, arr: List[int]) -> List[int]:
        # Deduplicate, sort, assign rank 1..k, map back to original positions.
        # set(arr) removes duplicates so equal elements get the same rank automatically.
        rank = {v: i + 1 for i, v in enumerate(sorted(set(arr)))}
        return [rank[x] for x in arr]


# ── Quick tests ───────────────────────────────────────────────────────────────
if __name__ == "__main__":
    sol = Solution()

    print(sol.arrayRankTransform([40, 10, 20, 30]))              # [4, 1, 2, 3]
    print(sol.arrayRankTransform([100, 100, 100]))               # [1, 1, 1]
    print(sol.arrayRankTransform([37, 12, 28, 9, 100, 56, 80, 5, 12]))  # [5,3,4,2,8,6,7,1,3]

    # Edge cases
    print(sol.arrayRankTransform([]))                            # []   empty
    print(sol.arrayRankTransform([7]))                           # [1]  single element
    print(sol.arrayRankTransform([-1, -3, -2]))                  # [3, 1, 2] negatives
    print(sol.arrayRankTransform([0, 0, 0]))                     # [1, 1, 1] all same
