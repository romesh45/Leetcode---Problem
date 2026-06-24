from typing import List
import numpy as np

MOD = 10**9 + 7


class Solution:
    def zigZagArrays(self, n: int, l: int, r: int) -> int:
        M = r - l + 1
        size = 2 * M
        T = np.zeros((size, size), dtype=np.int64)
        for v in range(M):
            for u in range(v):          
                T[v][M + u] = 1
        for v in range(M):
            for u in range(v + 1, M):   
                T[M + v][u] = 1
        init = np.zeros(size, dtype=np.int64)
        for v in range(M):
            init[v]     = v          
            init[M + v] = M - 1 - v  
        def mat_mul(A: np.ndarray, B: np.ndarray) -> np.ndarray:
            """Modular matrix multiply with chunked k-axis to avoid int64 overflow."""
            CHUNK = 8   
            C = np.zeros((size, size), dtype=np.int64)
            for k0 in range(0, size, CHUNK):
                C = (C + A[:, k0:k0 + CHUNK] @ B[k0:k0 + CHUNK, :]) % MOD
            return C
        result = np.eye(size, dtype=np.int64)    
        base   = T.copy()
        exp    = n - 2
        while exp:
            if exp & 1:
                result = mat_mul(result, base)
            base = mat_mul(base, base)
            exp >>= 1
        state = np.zeros(size, dtype=np.int64)
        for k0 in range(0, size, 8):
            state = (state + result[:, k0:k0 + 8] @ init[k0:k0 + 8]) % MOD
        return int(state.sum() % MOD)


# ── Reference: O(n * M) DP — correct but only usable for small n ─────────────
class SolutionLinear:
    def zigZagArrays(self, n: int, l: int, r: int) -> int:
        MOD = 10**9 + 7
        M = r - l + 1
        up   = [v       for v in range(M)]
        down = [M-1-v   for v in range(M)]
        for _ in range(n - 2):
            prefix_down = [0] * (M + 1)
            for v in range(M):
                prefix_down[v + 1] = (prefix_down[v] + down[v]) % MOD
            suffix_up = [0] * (M + 1)
            for v in range(M - 1, -1, -1):
                suffix_up[v] = (suffix_up[v + 1] + up[v]) % MOD
            up   = [prefix_down[v]   for v in range(M)]
            down = [suffix_up[v + 1] for v in range(M)]
        return (sum(up) + sum(down)) % MOD


# ── Quick tests ───────────────────────────────────────────────────────────────
if __name__ == "__main__":
    sol = Solution()

    print(sol.zigZagArrays(3, 4, 5))   # 2
    print(sol.zigZagArrays(3, 1, 3))   # 10

    # Cross-check matrix exp vs linear DP for moderate n
    ref = SolutionLinear()
    import random
    random.seed(42)
    for _ in range(300):
        n = random.randint(3, 200)
        l = random.randint(1, 10)
        r = random.randint(l + 1, min(l + 10, 75))
        a = sol.zigZagArrays(n, l, r)
        b = ref.zigZagArrays(n, l, r)
        assert a == b, f"MISMATCH n={n} l={l} r={r}: matexp={a} linear={b}"
    print("cross-check (matexp vs linear DP) passed ✓")

    # Stress test: worst-case constraints
    import time
    t0 = time.time()
    ans = sol.zigZagArrays(10**9, 1, 75)
    print(f"n=10^9, l=1, r=75: {ans}  ({time.time()-t0:.3f}s)")
