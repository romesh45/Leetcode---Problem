from typing import List


class Solution:
    def concatenateAndMultiply(self, s: str, queries: List[List[int]]) -> List[int]:
        MOD = 10**9 + 7
        m = len(s)

        # ── Prefix arrays (1-based: index i covers s[0..i-1]) ─────────────────
        # nz[i]  = count  of non-zero digits in s[0..i-1]
        # px[i]  = value  of x for s[0..i-1] (mod MOD)
        # ps[i]  = digit sum  of x for s[0..i-1]  (plain int — max 9*m = 9*10^5)
        nz = [0] * (m + 1)
        px = [0] * (m + 1)
        ps = [0] * (m + 1)

        for i, ch in enumerate(s):
            d = int(ch)
            nz[i+1] = nz[i]
            px[i+1] = px[i]
            ps[i+1] = ps[i]
            if d:
                nz[i+1]  = nz[i] + 1
                px[i+1]  = (px[i] * 10 + d) % MOD
                ps[i+1]  = ps[i] + d

        # Powers of 10 mod MOD (exponent up to m = 10^5)
        pow10 = [1] * (m + 1)
        for i in range(1, m + 1):
            pow10[i] = pow10[i-1] * 10 % MOD

        # ── Answer each query in O(1) ─────────────────────────────────────────
        #
        # Key formula:  px[r+1]  =  px[l] * 10^cnt  +  x   (mathematically)
        # where cnt = nz[r+1] - nz[l]  (non-zero digits in s[l..r])
        #
        # Rearranging:  x = px[r+1] - px[l] * 10^cnt   (mod MOD)
        #
        # Digit sum of x is just  ps[r+1] - ps[l]   (no overflow risk).
        result = []
        for l, r in queries:
            cnt = nz[r+1] - nz[l]
            x   = (px[r+1] - px[l] * pow10[cnt]) % MOD
            tot = ps[r+1] - ps[l]
            result.append(x * tot % MOD)

        return result


# ── Quick tests ───────────────────────────────────────────────────────────────
if __name__ == "__main__":
    sol = Solution()

    print(sol.concatenateAndMultiply("10203004", [[0,7],[1,3],[4,6]]))
    # [12340, 4, 9]

    print(sol.concatenateAndMultiply("1000", [[0,3],[1,1]]))
    # [1, 0]

    print(sol.concatenateAndMultiply("9876543210", [[0,9]]))
    # [444444137]

    # Edge cases
    print(sol.concatenateAndMultiply("0000", [[0,3]]))          # [0]   all zeros
    print(sol.concatenateAndMultiply("9", [[0,0]]))             # [81]  single digit
    print(sol.concatenateAndMultiply("12", [[0,0],[1,1],[0,1]])) # [1, 4, 36]
