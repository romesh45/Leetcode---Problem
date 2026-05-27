class Solution:
    def numberOfSpecialChars(self, word: str) -> int:
        last_lower = {}
        first_upper = {}
        for i, ch in enumerate(word):
            if ch.islower():
                last_lower[ch] = i
            else:
                if ch not in first_upper:
                    first_upper[ch] = i
        count = 0
        for c, lo_idx in last_lower.items():
            up = c.upper()
            if up in first_upper and lo_idx < first_upper[up]:
                count += 1
        return count


# ── Quick tests ──────────────────────────
if __name__ == "__main__":
    sol = Solution()
    print(sol.numberOfSpecialChars("aaAbcBC"))   # 3   (a, b, c — all lowercase before uppercase)
    print(sol.numberOfSpecialChars("abc"))       # 0   (no uppercase)
    print(sol.numberOfSpecialChars("AbBCab"))    # 0   (every letter has lowercase after its uppercase)
    print(sol.numberOfSpecialChars("aA"))        # 1
    print(sol.numberOfSpecialChars("Aa"))        # 0   (lowercase after uppercase)
    print(sol.numberOfSpecialChars("abABab"))    # 0   (lowercase a,b appear after A,B)
    print(sol.numberOfSpecialChars("aabbCCAB"))  # 2   (a: last lower 1 < first A 6 ✓;  b: last lower 3 < first B 7 ✓;  c: no lowercase)
    print(sol.numberOfSpecialChars("abABCab"))   # 0
    print(sol.numberOfSpecialChars("zZ"))        # 1
