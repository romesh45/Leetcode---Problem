class Solution:
    def asteroidsDestroyed(self, mass: int, asteroids: List[int]) -> bool:
        asteroids.sort()
        for a in asteroids:
            if mass < a:
                return False
            mass += a       
        return True


# ── Quick tests ───────────────────
if __name__ == "__main__":
    sol = Solution()
    print(sol.asteroidsDestroyed(10, [3, 9, 19, 5, 21]))     # True
    print(sol.asteroidsDestroyed(5, [4, 9, 23, 4]))          # False
    print(sol.asteroidsDestroyed(1, [1]))                    # True
    print(sol.asteroidsDestroyed(1, [2]))                    # False
    print(sol.asteroidsDestroyed(100, [1, 1, 1, 1]))         # True
    print(sol.asteroidsDestroyed(5, [5, 10, 20, 40]))        # True (5→10→20→40→80)
    print(sol.asteroidsDestroyed(2, [3]))                    # False
