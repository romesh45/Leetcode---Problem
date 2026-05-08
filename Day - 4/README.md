# Day 4 — LeetCode Challenge

## 3629. Minimum Jumps to Reach End via Prime Teleportation

| Field | Details |
|---|---|
| **Difficulty** | Medium |
| **Topics** | BFS, Math, Number Theory, Sieve of Eratosthenes |
| **LeetCode Link** | [3629. Minimum Jumps to Reach End via Prime Teleportation](https://leetcode.com/problems/minimum-jumps-to-reach-end-via-prime-teleportation/) |

---

## Problem Statement

You are given an integer array `nums` of length `n`. Start at index `0`, reach index `n - 1`.

From any index `i`, you may:

1. **Adjacent Step** — jump to `i + 1` or `i - 1` (if in bounds).
2. **Prime Teleportation** — if `nums[i]` is prime `p`, instantly jump to **any** index `j ≠ i` where `nums[j] % p == 0`.

Return the **minimum number of jumps** to reach index `n - 1`.

---

## Examples

### Example 1

```
Input:  nums = [1, 2, 4, 6]
Output: 2
```

- Step to index 1 (adjacent).
- Teleport from index 1 (`nums[1]=2`, prime) to index 3 (`nums[3]=6`, divisible by 2).

### Example 2

```
Input:  nums = [2, 3, 4, 7, 9]
Output: 2
```

- Step to index 1 (adjacent).
- Teleport from index 1 (`nums[1]=3`, prime) to index 4 (`nums[4]=9`, divisible by 3).

### Example 3

```
Input:  nums = [4, 6, 5, 8]
Output: 3
```

- No teleportation connects index 2 (value 5, prime) to index 3 (value 8, not divisible by 5).
- Must walk: 0 → 1 → 2 → 3.

---

## Constraints

- `1 <= n <= 10^5`
- `1 <= nums[i] <= 10^6`

---

## Intuition

### Step 1 — It's a BFS problem

Every jump costs exactly 1. Minimum jumps = shortest path. BFS gives the answer.

### Step 2 — Naive BFS is O(n²)

For a prime like 2, half the array could be divisible by it. Every time we visit a "2-index", we'd scan all those divisible targets. That's O(n) work per node → O(n²) total.

### Step 3 — Bucket Clearing Trick

**Group all indices by their prime factors upfront.** Then when prime `p` is first activated during BFS:

1. Process its entire bucket (stamp all unvisited targets with `dist + 1`).
2. **Immediately clear the bucket.**

Any future index with `nums[i] = p` finds an empty bucket and does zero work. This is safe because BFS guarantees the first activation is via the shortest path — every target has already been given the optimal distance.

**Result:** Each index is processed from a bucket at most once → O(n log V) total.

### Step 4 — Smallest Prime Factor (SPF) Sieve

To know which prime-factor buckets index `j` belongs to, we need the prime factorization of `nums[j]`. A precomputed SPF sieve enables O(log V) factorization per number instead of O(√V).

```
SPF[1]  = 1
SPF[2]  = 2   (prime)
SPF[3]  = 3   (prime)
SPF[4]  = 2   (4 = 2²)
SPF[6]  = 2   (6 = 2 × 3)
SPF[12] = 2   (12 = 2² × 3)
```

---

## Algorithm

```
1. Build SPF sieve for [0, max(nums)].

2. Find active_primes = all primes that appear as a value in nums.
   (Only these can trigger teleportation — no need to care about others.)

3. Build prime_buckets[p] = indices j where p | nums[j],
   for every p in active_primes.

4. BFS from index 0:
   - For each node i dequeued:
     a. Enqueue unvisited i-1 and i+1 at dist+1.
     b. If nums[i] is prime p:
        - Enqueue all unvisited indices in prime_buckets[p] at dist+1.
        - Clear prime_buckets[p].          ← the key optimisation
```

---

## Solution

```python
from typing import List
from collections import defaultdict, deque


class Solution:
    def minJumps(self, nums: List[int]) -> int:
        n = len(nums)
        if n == 1:
            return 0

        max_val = max(nums)

        # ── Smallest Prime Factor Sieve ──────────────────────────────────
        # spf[i] = smallest prime that divides i
        # Lets us factorize any v in O(log v) instead of O(sqrt v)
        spf = list(range(max_val + 1))
        i = 2
        while i * i <= max_val:
            if spf[i] == i:           # i is prime
                for j in range(i * i, max_val + 1, i):
                    if spf[j] == j:
                        spf[j] = i
            i += 1

        def prime_factors(x):
            """Distinct prime factors of x in O(log x)."""
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

            # Adjacent steps
            for ni in (i - 1, i + 1):
                if 0 <= ni < n and dist[ni] == -1:
                    dist[ni] = d + 1
                    queue.append(ni)

            # Prime teleportation
            if is_prime(nums[i]):
                p = nums[i]
                bucket = prime_buckets[p]
                if bucket:
                    for j in bucket:
                        if dist[j] == -1:
                            dist[j] = d + 1
                            queue.append(j)
                    prime_buckets[p] = []   # ← clear: never re-process this prime
```

---

## Complexity Analysis

| | Complexity |
|---|---|
| **Time** | O(V log log V + n log V) — sieve + BFS with bucket clearing |
| **Space** | O(V + n) — SPF array + BFS structures |

Where `V = max(nums)` (up to 10⁶) and `n` is array length (up to 10⁵).

The bucket clearing ensures each index is enqueued at most once from a prime bucket. Each index appears in at most O(log V) buckets (number of distinct prime factors). Total bucket work = O(n log V).

---

## Dry Run — Example 2: `[2, 3, 4, 7, 9]`

**Setup:**
```
active_primes = {2, 3, 7}
prime_buckets[2] = [0, 2]     (nums[0]=2, nums[2]=4)
prime_buckets[3] = [1, 4]     (nums[1]=3, nums[4]=9)
prime_buckets[7] = [3]        (nums[3]=7)
dist = [0, -1, -1, -1, -1]
```

| Dequeue | dist | Action | Queue after |
|---|---|---|---|
| i=0 (2) | 0 | adj→1 (dist=1); prime 2: stamp 0(skip),2→dist=1; clear bucket[2] | [1, 2] |
| i=1 (3) | 1 | adj→0(skip),2(skip); prime 3: stamp 1(skip),4→dist=2; clear bucket[3] | [2, 4] |
| i=2 (4) | 1 | adj→1(skip),3→dist=2; nums[2]=4 not prime | [4, 3] |
| i=4 (9) | 2 | **i == n-1 → return 2** ✓ | — |

---

## Why Clearing the Bucket Works

```
Queue (BFS level by level):
Level 0: [0]
Level 1: [1, 2]         ← index 1 via step, index 2 via prime-2 teleport
Level 2: [4, 3]         ← index 4 via prime-3 teleport, index 3 via step
```

When index 2 (value 4) is dequeued at dist=1, it checks prime factors of 4 = {2}. But `prime_buckets[2]` was already cleared when index 0 was dequeued. Zero extra work. ✓

---

## Approach Tags

`BFS` · `Number Theory` · `SPF Sieve` · `Bucket Clearing` · `Graph Shortest Path`

---

*Day 4 of the LeetCode Daily Challenge*
