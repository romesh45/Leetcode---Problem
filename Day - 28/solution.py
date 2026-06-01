class Solution:
    def minimumCost(self, cost: List[int]) -> int:
        cost.sort(reverse=True)
        total = 0
        for i, c in enumerate(cost):
            if i % 3 != 2:          
                total += c
        return total


# ── Quick tests ───────────────────────
if __name__ == "__main__":
    sol = Solution()
    print(sol.minimumCost([1, 2, 3]))                 # 5
    print(sol.minimumCost([6, 5, 7, 9, 2, 2]))        # 23
    print(sol.minimumCost([5, 5]))                    # 10
    print(sol.minimumCost([1]))                       # 1
    print(sol.minimumCost([1, 1, 1]))                 # 2   (free one '1')
    print(sol.minimumCost([10, 10, 10, 10, 10, 10]))  # 40  (two free)
    print(sol.minimumCost([3, 1, 2, 4, 5, 6, 7]))     # 21  (sorted [7,6,5,4,3,2,1]; free 5 & 2)
