class Solution:
    def numberOfSpecialChars(self, word: str) -> int:
        # For each letter, we need just two pieces of information:
        #   • last_lower[c]  — the LATEST  index of lowercase c
        #   • first_upper[c] — the EARLIEST index of uppercase c
        #
        # Claim: letter c is special  ⇔  both exist  AND  last_lower[c] < first_upper[c.upper()]
        #
        # Why those two specifically?
        #   "Every lowercase before the first uppercase" must hold for the
        #   WORST-CASE lowercase (the last one) and the WORST-CASE upper bound
        #   (the first uppercase). If even those two pass the check, every
        #   actual pair does.
        last_lower = {}
        first_upper = {}

        for i, ch in enumerate(word):
            if ch.islower():
                # Overwrite — at end of loop this holds the LAST position
                # of each lowercase letter.
                last_lower[ch] = i
            else:
                # Write only on first sight — preserves the FIRST position
                # of each uppercase letter.
                if ch not in first_upper:
                    first_upper[ch] = i

        # Iterate the smaller scope (≤ 26 entries) and apply the ordering test.
        count = 0
        for c, lo_idx in last_lower.items():
            up = c.upper()
            if up in first_upper and lo_idx < first_upper[up]:
                count += 1
        return count


# ── Quick tests ──────────────────────────────────────────────────────────────
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
