# 1914. Cyclically Rotating a Grid
# https://leetcode.com/problems/cyclically-rotating-a-grid/
# Difficulty: Medium | Time: O(m*n) | Space: O(m*n)

from typing import List

class Solution:
    def rotateGrid(self, grid: List[List[int]], k: int) -> List[List[int]]:
        m, n = len(grid), len(grid[0])

        def extract_layer(layer: int) -> List[int]:
            r1, c1 = layer, layer
            r2, c2 = m - 1 - layer, n - 1 - layer
            elements = []

            # Top row: left → right
            for c in range(c1, c2 + 1):
                elements.append(grid[r1][c])
            # Right col: top+1 → bottom
            for r in range(r1 + 1, r2 + 1):
                elements.append(grid[r][c2])
            # Bottom row: right-1 → left
            for c in range(c2 - 1, c1 - 1, -1):
                elements.append(grid[r2][c])
            # Left col: bottom-1 → top+1
            for r in range(r2 - 1, r1, -1):
                elements.append(grid[r][c1])

            return elements

        def place_layer(layer: int, elements: List[int]) -> None:
            r1, c1 = layer, layer
            r2, c2 = m - 1 - layer, n - 1 - layer
            idx = 0

            for c in range(c1, c2 + 1):
                grid[r1][c] = elements[idx]; idx += 1
            for r in range(r1 + 1, r2 + 1):
                grid[r][c2] = elements[idx]; idx += 1
            for c in range(c2 - 1, c1 - 1, -1):
                grid[r2][c] = elements[idx]; idx += 1
            for r in range(r2 - 1, r1, -1):
                grid[r][c1] = elements[idx]; idx += 1

        num_layers = min(m, n) // 2

        for layer in range(num_layers):
            elements = extract_layer(layer)
            L = len(elements)
            k_eff = k % L                            # avoid redundant full rotations
            rotated = elements[k_eff:] + elements[:k_eff]
            place_layer(layer, rotated)

        return grid


# ── Tests ────────────────────────────────────────────────────────────────────

if __name__ == "__main__":
    import copy

    sol = Solution()

    test_cases = [
        ([[40,10],[30,20]], 1, [[10,20],[40,30]]),
        ([[1,2,3,4],[5,6,7,8],[9,10,11,12],[13,14,15,16]], 2,
         [[3,4,8,12],[2,11,10,16],[1,7,6,15],[5,9,13,14]]),
        ([[1,2,3,4],[5,6,7,8],[9,10,11,12],[13,14,15,16]], 12,
         [[1,2,3,4],[5,6,7,8],[9,10,11,12],[13,14,15,16]]),
    ]

    all_pass = True
    for grid, k, expected in test_cases:
        result = sol.rotateGrid(copy.deepcopy(grid), k)
        status = "PASS" if result == expected else "FAIL"
        if status == "FAIL":
            all_pass = False
        print(f"[{status}] k={k} → {result[0]}...")

    print("\nAll tests passed ✓" if all_pass else "\nSome tests failed ✗")
