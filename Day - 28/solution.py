from typing import List


class Solution:
    def minimumCost(self, cost: List[int]) -> int:
        # Greedy: sort DESCENDING and skip every 3rd candy.
        #
        # Promotion rule recap: for every two candies bought, you may take a
        # third FREE, but only if it costs ≤ the cheaper of the two bought.
        # ⇒ In any valid triple, the free candy is the cheapest of the three.
        #
        # To save the most money we want the FREE candies to be as expensive as
        # possible. Sorting descending and grouping in threes (buy the two
        # priciest, free the next) makes every index ≡ 2 (mod 3) the free one —
        # the largest candies we're ever permitted to get for free.
        cost.sort(reverse=True)

        total = 0
        for i, c in enumerate(cost):
            if i % 3 != 2:          # positions 2, 5, 8, … are free → skip them
                total += c

        return total


# ── Quick tests ──────────────────────────────────────────────────────────────
if __name__ == "__main__":
    sol = Solution()
    print(sol.minimumCost([1, 2, 3]))                 # 5
    print(sol.minimumCost([6, 5, 7, 9, 2, 2]))        # 23
    print(sol.minimumCost([5, 5]))                    # 10
    print(sol.minimumCost([1]))                       # 1
    print(sol.minimumCost([1, 1, 1]))                 # 2   (free one '1')
    print(sol.minimumCost([10, 10, 10, 10, 10, 10]))  # 40  (two free)
    print(sol.minimumCost([3, 1, 2, 4, 5, 6, 7]))     # 21  (sorted [7,6,5,4,3,2,1]; free 5 & 2)
