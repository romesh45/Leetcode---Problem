class Solution:
    def processStr(self, s: str, k: int) -> str:
        # The "II" twist: |s| ≤ 10^5 and '#' DOUBLES the string, so the final
        # length can reach 10^15 — far too large to build. We only need the
        # character at index k, so:
        #   1) Forward pass: record the length BEFORE each operation.
        #   2) Backward pass: map k through each op in reverse until it lands on
        #      the original appended letter.
        CAP = 10**15 + 1          # defensive cap; valid lengths never exceed 10^15

        # ── Forward: before[i] = length just before processing s[i] ──────────
        before = [0] * len(s)
        length = 0
        for i, ch in enumerate(s):
            before[i] = length
            if ch == '*':
                length = max(0, length - 1)
            elif ch == '#':
                length = min(length * 2, CAP)
            elif ch == '%':
                pass                       # reverse leaves length unchanged
            else:
                length += 1

        # `length` is now the FINAL length. Out of bounds → '.'.
        if k >= length:
            return "."

        # ── Backward: undo each op, transforming k into an earlier index ─────
        for i in range(len(s) - 1, -1, -1):
            L = before[i]                  # length BEFORE this op
            ch = s[i]
            if ch == '*':
                # post-string is a prefix of the pre-string → k unchanged.
                pass
            elif ch == '#':
                # after = pre + pre; second copy maps back by -L.
                if k >= L:
                    k -= L
            elif ch == '%':
                # reverse: index k came from position L-1-k.
                k = L - 1 - k
            else:
                # letter append: new char occupies index L (last slot).
                if k == L:
                    return ch
                # else k < L → already an index into the pre-string, unchanged.

        return "."                          # unreachable for valid k


# ── Brute-force reference (Day-43 simulation) for cross-checking ─────────────
class SolutionBrute:
    def processStr(self, s: str, k: int) -> str:
        res = []
        for ch in s:
            if ch == '*':
                if res:
                    res.pop()
            elif ch == '#':
                res += res
            elif ch == '%':
                res.reverse()
            else:
                res.append(ch)
        return res[k] if 0 <= k < len(res) else "."


# ── Quick tests ──────────────────────────────────────────────────────────────
if __name__ == "__main__":
    sol = Solution()
    print(sol.processStr("a#b%*", 1))      # "a"
    print(sol.processStr("cd%#*#", 3))     # "d"
    print(sol.processStr("z*#", 0))        # "."
    print(sol.processStr("abc", 2))        # "c"
    print(sol.processStr("ab#", 3))        # "b"  (abab → index 3)
    print(sol.processStr("abc%", 0))       # "c"  (cba → index 0)

    # Randomized cross-check vs brute simulation (small strings, bounded '#').
    import random
    brute = SolutionBrute()
    chars = "abc***%##"   # weighted toward letters/specials but few '#'
    for _ in range(20000):
        m = random.randint(1, 12)
        s = "".join(random.choice(chars) for _ in range(m))
        # keep the simulated length sane for brute force
        full = brute.processStr(s, 0)
        # try several k including out-of-bounds
        for k in range(0, 16):
            assert sol.processStr(s, k) == brute.processStr(s, k), (s, k)
    print("randomized cross-check passed ✓")

    # Large-scale sanity: 10^5 ops, many '#', huge k — must run fast & not build.
    import time
    s = ("a#" * 50000)               # length explodes toward the cap
    t0 = time.time()
    out = sol.processStr(s, 10**15 - 1)
    print(f"n=1e5 with many '#', k≈1e15 → {out!r}  ({time.time()-t0:.3f}s)")
