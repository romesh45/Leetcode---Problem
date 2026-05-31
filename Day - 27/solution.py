from typing import List


class Solution:
    def asteroidsDestroyed(self, mass: int, asteroids: List[int]) -> bool:
        # Greedy: always destroy the SMALLEST remaining asteroid first.
        #
        # Key facts:
        #   • Destroying an asteroid only INCREASES our mass (never decreases).
        #   • Therefore mass is monotonically non-decreasing as we proceed.
        #   • Tackling the smallest reachable asteroid maximizes our mass before
        #     facing the bigger ones — the best possible chance against each.
        #
        # Sort ascending, then sweep:
        asteroids.sort()

        for a in asteroids:
            if mass < a:
                # The smallest remaining asteroid already exceeds our mass.
                # Every ordering absorbs the same total mass, so at this point
                # we hold the MAXIMUM mass achievable before confronting an
                # asteroid this large — if it's not enough, nothing is.
                return False
            mass += a       # destroy it, absorb its mass

        return True


# ── Quick tests ──────────────────────────────────────────────────────────────
if __name__ == "__main__":
    sol = Solution()
    print(sol.asteroidsDestroyed(10, [3, 9, 19, 5, 21]))     # True
    print(sol.asteroidsDestroyed(5, [4, 9, 23, 4]))          # False
    print(sol.asteroidsDestroyed(1, [1]))                    # True
    print(sol.asteroidsDestroyed(1, [2]))                    # False
    print(sol.asteroidsDestroyed(100, [1, 1, 1, 1]))         # True
    print(sol.asteroidsDestroyed(5, [5, 10, 20, 40]))        # True (5→10→20→40→80)
    print(sol.asteroidsDestroyed(2, [3]))                    # False
