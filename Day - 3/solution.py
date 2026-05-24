class Solution:
    def maxValue(self, nums: List[int]) -> List[int]:
        n = len(nums)
        parent = list(range(n))
        size   = [1] * n
        mx     = nums[:]
        def find(x):
            while parent[x] != x:
                parent[x] = parent[parent[x]]
                x = parent[x]
            return x
        def union(x, y):
            rx, ry = find(x), find(y)
            if rx == ry:
                return
            if size[rx] < size[ry]:
                rx, ry = ry, rx
            parent[ry] = rx
            size[rx]  += size[ry]
            mx[rx]     = max(mx[rx], mx[ry])
        stack = []
        for i in range(n):
            comp_max = nums[i]
            while stack and stack[-1][1] > nums[i]:
                rep, m = stack.pop()
                union(i, rep)
                comp_max = max(comp_max, m)
            stack.append([find(i), comp_max])
        return [mx[find(i)] for i in range(n)]
