from typing import List


class Solution:
    def maximumJumps(self, nums: List[int]) -> List[int]:
        n = len(nums)
        parent = list(range(n))
        size   = [1] * n
        mx     = nums[:]          # max value in each component (tracked at root)

        def find(x):
            while parent[x] != x:
                parent[x] = parent[parent[x]]  # path compression (halving)
                x = parent[x]
            return x

        def union(x, y):
            rx, ry = find(x), find(y)
            if rx == ry:
                return
            if size[rx] < size[ry]:
                rx, ry = ry, rx              # union by size
            parent[ry] = rx
            size[rx] += size[ry]
            mx[rx] = max(mx[rx], mx[ry])    # propagate max to new root

        # Pass 1: union each index with its Previous Greater Element (PGE)
        # Stack stays decreasing; pop while top <= current value
        stack = []
        for i in range(n):
            while stack and nums[stack[-1]] <= nums[i]:
                stack.pop()
            if stack:
                union(i, stack[-1])
            stack.append(i)

        # Pass 2: union each index with its Next Smaller Element (NSE)
        # Stack stays increasing; pop while top >= current value
        stack = []
        for i in range(n - 1, -1, -1):
            while stack and nums[stack[-1]] >= nums[i]:
                stack.pop()
            if stack:
                union(i, stack[-1])
            stack.append(i)

        return [mx[find(i)] for i in range(n)]


# ---------- quick tests ----------
if __name__ == "__main__":
    sol = Solution()
    print(sol.maximumJumps([2, 1, 3]))   # [2, 2, 3]
    print(sol.maximumJumps([2, 3, 1]))   # [3, 3, 3]
    print(sol.maximumJumps([5]))         # [5]
    print(sol.maximumJumps([1, 2, 3]))   # [1, 2, 3]  (strictly increasing — no jumps)
    print(sol.maximumJumps([3, 5, 1, 4])) # [5, 5, 5, 5]
