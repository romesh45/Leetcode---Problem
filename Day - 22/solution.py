class Solution:
    def numberOfSpecialChars(self, word: str) -> int:
        lower_seen = set()   
        upper_seen = set()   
        for ch in word:
            if ch.islower():
                lower_seen.add(ch)
            else:
                upper_seen.add(ch)
        return sum(1 for c in lower_seen if c.upper() in upper_seen)


# ── One-liner equivalent (same complexity, terser) ─────────────────


class SolutionOneLiner:
    def numberOfSpecialChars(self, word: str) -> int:
        return len({c for c in word if c.islower() and c.upper() in word})


# ── Quick tests ────────────────────────
if __name__ == "__main__":
    sol = Solution()
    print(sol.numberOfSpecialChars("aaAbcBC"))   # 3  (a, b, c)
    print(sol.numberOfSpecialChars("abc"))       # 0  (no uppercase)
    print(sol.numberOfSpecialChars("abBCab"))    # 1  (only b)
    print(sol.numberOfSpecialChars(""))          # 0
    print(sol.numberOfSpecialChars("aA"))        # 1
    print(sol.numberOfSpecialChars("ABCabc"))    # 3  (a, b, c)
    print(sol.numberOfSpecialChars("AaBbCcDd"))  # 4

    sol2 = SolutionOneLiner()
    print(sol2.numberOfSpecialChars("aaAbcBC"))  # 3
    print(sol2.numberOfSpecialChars("abBCab"))   # 1
