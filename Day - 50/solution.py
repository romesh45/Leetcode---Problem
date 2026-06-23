from typing import List

MOD = 10**9 + 7


class Solution:
    def numberOfZigzagArrays(self, n: int, l: int, r: int) -> int:
        # Greedy insight: a zigzag array must alternate peaks and valleys.
        # After any UP move the next move must be DOWN, and vice versa —
        # no three consecutive elements may be strictly monotone.
        #
        # DP state after placing i+1 elements (0-indexed):
        #   up[v]   = # ways array ends at value (l + v) with last move UP
        #   down[v] = # ways array ends at value (l + v) with last move DOWN
        #
        # Transitions for a new element at value new_v:
        #   new_up[new_v]   = Σ down[cur_v]  for cur_v < new_v   (move UP from valley)
        #   new_down[new_v] = Σ up[cur_v]    for cur_v > new_v   (move DOWN from peak)
        #
        # Both sums are range sums → precompute prefix/suffix in O(M) per step.
        # Overall: O(n × M)  time,  O(M) space.

        M = r - l + 1  # number of distinct values in [l, r]

        # ── Initialise for the first TWO elements ────────────────────────────
        # Enumerate all (arr[0], arr[1]) pairs with arr[0] ≠ arr[1].
        # up[v]   counts pairs where arr[1] = l+v and arr[0] < arr[1]  → v choices
        # down[v] counts pairs where arr[1] = l+v and arr[0] > arr[1]  → M-1-v choices
        up   = [v       for v in range(M)]
        down = [M-1-v   for v in range(M)]

        # ── Extend one element at a time from position 2 … n-1 ──────────────
        for _ in range(n - 2):
            # prefix_down[v] = Σ down[0 .. v-1]
            prefix_down = [0] * (M + 1)
            for v in range(M):
                prefix_down[v + 1] = (prefix_down[v] + down[v]) % MOD

            # suffix_up[v] = Σ up[v .. M-1]
            suffix_up = [0] * (M + 1)
            for v in range(M - 1, -1, -1):
                suffix_up[v] = (suffix_up[v + 1] + up[v]) % MOD

            # new_up[new_v]   = prefix_down[new_v]       (sum over cur_v in [0, new_v-1])
            # new_down[new_v] = suffix_up[new_v + 1]     (sum over cur_v in [new_v+1, M-1])
            up   = [prefix_down[v]      for v in range(M)]
            down = [suffix_up[v + 1]    for v in range(M)]

        return (sum(up) + sum(down)) % MOD


# ── Reference: brute-force (for cross-checking small inputs) ─────────────────
class SolutionBrute:
    def numberOfZigzagArrays(self, n: int, l: int, r: int) -> int:
        from itertools import product
        MOD = 10**9 + 7
        count = 0
        for arr in product(range(l, r + 1), repeat=n):
            ok = all(arr[i] != arr[i - 1] for i in range(1, n))
            if not ok:
                continue
            ok = all(
                not (arr[i - 1] < arr[i] < arr[i + 1]) and
                not (arr[i - 1] > arr[i] > arr[i + 1])
                for i in range(1, n - 1)
            )
            if ok:
                count += 1
        return count % MOD


# ── Quick tests ───────────────────────────────────────────────────────────────
if __name__ == "__main__":
    sol = Solution()

    print(sol.numberOfZigzagArrays(3, 4, 5))   # 2
    print(sol.numberOfZigzagArrays(3, 1, 3))   # 10

    # Edge cases
    print(sol.numberOfZigzagArrays(3, 1, 2))   # 2  → [1,2,1], [2,1,2]
    print(sol.numberOfZigzagArrays(3, 1, 1))   # 0  → no valid array (all equal, no zigzag)
    print(sol.numberOfZigzagArrays(4, 1, 3))   # 16
    print(sol.numberOfZigzagArrays(5, 1, 3))   # 26

    # Randomised cross-check against brute force
    import random
    ref = SolutionBrute()
    for _ in range(500):
        n = random.randint(3, 6)
        l = random.randint(1, 4)
        r = random.randint(l + 1, l + 4)
        a = sol.numberOfZigzagArrays(n, l, r)
        b = ref.numberOfZigzagArrays(n, l, r)
        assert a == b, f"MISMATCH n={n} l={l} r={r}: dp={a} brute={b}"
    print("randomised cross-check passed ✓")
