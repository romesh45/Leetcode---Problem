from typing import List
from collections import deque, defaultdict


class Solution:
    def remainingMethods(self, n: int, k: int, invocations: List[List[int]]) -> List[int]:
        # Build call graph
        adj = defaultdict(list)
        for a, b in invocations:
            adj[a].append(b)

        # BFS from k to find all suspicious methods (k + everything it reaches)
        suspicious = {k}
        queue = deque([k])
        while queue:
            node = queue.popleft()
            for nb in adj[node]:
                if nb not in suspicious:
                    suspicious.add(nb)
                    queue.append(nb)

        # If any non-suspicious method calls a suspicious one, removal is blocked
        for a, b in invocations:
            if a not in suspicious and b in suspicious:
                return list(range(n))

        # Safe to remove -- return everything outside the suspicious group
        return [m for m in range(n) if m not in suspicious]


# Quick tests
if __name__ == "__main__":
    sol = Solution()

    print(sol.remainingMethods(4, 1, [[1,2],[0,1],[3,2]]))    # [0,1,2,3]
    print(sol.remainingMethods(5, 0, [[1,2],[0,2],[0,1],[3,4]]))  # [3,4]
    print(sol.remainingMethods(3, 2, [[1,2],[0,1],[2,0]]))    # []
