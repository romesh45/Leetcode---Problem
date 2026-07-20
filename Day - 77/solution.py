class Solution:
    def shiftGrid(self, grid: List[List[int]], k: int) -> List[List[int]]:
        m, n = len(grid), len(grid[0])
        # Flatten the grid into a single list, shift by k (cyclic), reshape.
        flat = [v for row in grid for v in row]
        k %= m * n
        flat = flat[-k:] + flat[:-k]
        return [flat[i * n:(i + 1) * n] for i in range(m)]


# Quick tests
if __name__ == "__main__":
    sol = Solution()

    print(sol.shiftGrid([[1,2,3],[4,5,6],[7,8,9]], 1))
    # [[9,1,2],[3,4,5],[6,7,8]]

    print(sol.shiftGrid([[3,8,1,9],[19,7,2,5],[4,6,11,10],[12,0,21,13]], 4))
    # [[12,0,21,13],[3,8,1,9],[19,7,2,5],[4,6,11,10]]

    print(sol.shiftGrid([[1,2,3],[4,5,6],[7,8,9]], 9))
    # [[1,2,3],[4,5,6],[7,8,9]]  k % 9 == 0, no change

    # Edge cases
    print(sol.shiftGrid([[1]], 5))           # [[1]]  1x1 grid, any k
    print(sol.shiftGrid([[1,2],[3,4]], 0))   # [[1,2],[3,4]]  k=0
