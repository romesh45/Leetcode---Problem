from typing import List


class Solution:
    def minimumEffort(self, tasks: List[List[int]]) -> int:
        # Sort by (minimum - actual) descending.
        # Intuition: tasks with a bigger "buffer" (minimum - actual) should be done first.
        tasks.sort(key=lambda x: x[1] - x[0], reverse=True)

        energy = 0      # total initial energy required (this is the answer)
        current = 0     # energy in hand right now

        for actual, minimum in tasks:
            # If we can't start this task, top up just enough to satisfy its minimum.
            # The amount we top up gets added to our required initial energy.
            if current < minimum:
                energy  += minimum - current
                current  = minimum
            # Spend `actual` energy completing the task.
            current -= actual

        return energy


# ── Quick tests ──────────────────────────────────────────────────────────────
if __name__ == "__main__":
    sol = Solution()
    print(sol.minimumEffort([[1, 2], [2, 4], [4, 8]]))                          # 8
    print(sol.minimumEffort([[1, 3], [2, 4], [10, 11], [10, 12], [8, 9]]))      # 32
    print(sol.minimumEffort([[1, 7], [2, 8], [3, 9], [4, 10], [5, 11], [6, 12]]))# 27
    print(sol.minimumEffort([[1, 1]]))                                          # 1
    print(sol.minimumEffort([[5, 10], [5, 10]]))                                # 15
