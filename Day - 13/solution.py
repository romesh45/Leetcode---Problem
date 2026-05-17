from collections import deque
from typing import List


class Solution:
    def canReach(self, arr: List[int], start: int) -> bool:
        n = len(arr)
        visited = [False] * n
        queue = deque([start])
        visited[start] = True

        while queue:
            i = queue.popleft()
            if arr[i] == 0:
                return True
            for nxt in (i + arr[i], i - arr[i]):
                if 0 <= nxt < n and not visited[nxt]:
                    visited[nxt] = True
                    queue.append(nxt)
        return False



if __name__ == "__main__":
    sol = Solution()
    print(sol.canReach([4, 2, 3, 0, 3, 1, 2], 5))   
    print(sol.canReach([4, 2, 3, 0, 3, 1, 2], 0))   
    print(sol.canReach([3, 0, 2, 1, 2], 2))         
    print(sol.canReach([0], 0))                     
    print(sol.canReach([1, 1, 1, 1, 1, 0], 0))      
    print(sol.canReach([2, 0, 1], 1))               
    print(sol.canReach([1, 0], 1))                  
