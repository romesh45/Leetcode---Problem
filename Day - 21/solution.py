class Solution:
    def canReach(self, s: str, minJump: int, maxJump: int) -> bool:
        n = len(s)
        if s[-1] != '0':
            return False
        queue = deque([0])
        farthest = 0   
        while queue:
            i = queue.popleft()
            lo = max(i + minJump, farthest + 1)
            hi = min(i + maxJump, n - 1)
            for j in range(lo, hi + 1):
                if s[j] == '0':
                    if j == n - 1:
                        return True
                    queue.append(j)
            farthest = max(farthest, hi)
        return False


# ── Quick tests ──────────────────────────
if __name__ == "__main__":
    sol = Solution()
    print(sol.canReach("011010", 2, 3))                       # True
    print(sol.canReach("01101110", 2, 3))                     # False
    print(sol.canReach("00", 1, 1))                           # True
    print(sol.canReach("01", 1, 1))                           # False (s[-1] is '1')
    print(sol.canReach("0000000000", 1, 1))                   # True
    print(sol.canReach("0" + "1" * 8 + "0", 1, 2))            # False (a wall of 1's blocks)
    print(sol.canReach("0" * 100000, 1, 5))                   # True
