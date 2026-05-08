from typing import List
from collections import defaultdict, deque


class Solution:
    def minJumps(self, nums: List[int]) -> int:
        n = len(nums)
        if n == 1:
            return 0

        max_val = max(nums)

        # ── Smallest Prime Factor Sieve ──────────────────────────────────
        spf = list(range(max_val + 1))
        i = 2
        while i * i <= max_val:
            if spf[i] == i:
                for j in range(i * i, max_val + 1, i):
                    if spf[j] == j:
                        spf[j] = i
            i += 1

        def prime_factors(x):
            factors = set()
            while x > 1:
                p = spf[x]
                factors.add(p)
                while x % p == 0:
                    x //= p
            return factors

        def is_prime(x):
            return x > 1 and spf[x] == x

        # ── Build Prime Buckets ──────────────────────────────────────────
        active_primes = {v for v in nums if is_prime(v)}

        prime_buckets = defaultdict(list)
        for j, v in enumerate(nums):
            for p in prime_factors(v):
                if p in active_primes:
                    prime_buckets[p].append(j)

        # ── BFS ─────────────────────────────────────────────────────────
        dist = [-1] * n
        dist[0] = 0
        queue = deque([0])

        while queue:
            i = queue.popleft()

            if i == n - 1:
                return dist[i]

            d = dist[i]

            for ni in (i - 1, i + 1):
                if 0 <= ni < n and dist[ni] == -1:
                    dist[ni] = d + 1
                    queue.append(ni)

            if is_prime(nums[i]):
                p = nums[i]
                bucket = prime_buckets[p]
                if bucket:
                    for j in bucket:
                        if dist[j] == -1:
                            dist[j] = d + 1
                            queue.append(j)
                    prime_buckets[p] = []

        return dist[n - 1]


if __name__ == "__main__":
    sol = Solution()
    print(sol.minJumps([1, 2, 4, 6]))        # 2
    print(sol.minJumps([2, 3, 4, 7, 9]))     # 2
    print(sol.minJumps([4, 6, 5, 8]))        # 3
    print(sol.minJumps([1]))                 # 0
    print(sol.minJumps([2, 1, 1, 1, 1, 4])) # 1
