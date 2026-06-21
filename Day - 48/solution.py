from typing import List


class Solution:
    def maxIceCream(self, costs: List[int], coins: int) -> int:
        # Greedy: buy the CHEAPEST bars first to maximize the COUNT.
        # The problem mandates COUNTING SORT — a natural fit since costs[i] is
        # bounded by 10^5, so we tally counts and sweep prices ascending instead
        # of doing an O(n log n) comparison sort.
        MAX_COST = max(costs)
        count = [0] * (MAX_COST + 1)
        for c in costs:
            count[c] += 1                       # bars priced exactly c

        bars = 0
        for price in range(1, MAX_COST + 1):    # ascending = cheapest first
            if count[price] == 0:
                continue
            if coins < price:
                break                           # can't afford this price → nor any higher
            # Buy as many at this price as coins allow, capped by availability.
            buyable = min(count[price], coins // price)
            bars += buyable
            coins -= buyable * price

        return bars


# ── Reference: sort-based greedy (for cross-checking) ────────────────────────
class SolutionSort:
    def maxIceCream(self, costs: List[int], coins: int) -> int:
        bars = 0
        for c in sorted(costs):
            if coins < c:
                break
            coins -= c
            bars += 1
        return bars


# ── Quick tests ──────────────────────────────────────────────────────────────
if __name__ == "__main__":
    sol = Solution()
    print(sol.maxIceCream([1, 3, 2, 4, 1], 7))           # 4
    print(sol.maxIceCream([10, 6, 8, 7, 7, 8], 5))       # 0
    print(sol.maxIceCream([1, 6, 3, 1, 2, 5], 20))       # 6
    print(sol.maxIceCream([5], 5))                       # 1
    print(sol.maxIceCream([2, 2, 2, 2], 7))              # 3  (three 2's = 6)
    print(sol.maxIceCream([100000], 100000000))          # 1

    # Randomized cross-check against the sort-based greedy.
    import random
    ref = SolutionSort()
    for _ in range(3000):
        n = random.randint(1, 50)
        costs = [random.randint(1, 30) for _ in range(n)]
        coins = random.randint(1, 200)
        assert sol.maxIceCream(costs[:], coins) == ref.maxIceCream(costs[:], coins), (costs, coins)
    print("randomized cross-check passed ✓")
