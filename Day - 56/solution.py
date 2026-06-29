class Solution:
    def numOfStrings(self, patterns: List[str], word: str) -> int:
        return sum(p in word for p in patterns)


# ── Quick tests ────────────────────────────────────
if __name__ == "__main__":
    sol = Solution()

    print(sol.numOfStrings(["a", "abc", "bc", "d"], "abc"))        # 3
    print(sol.numOfStrings(["a", "b", "c"], "aaaaabbbbb"))          # 2
    print(sol.numOfStrings(["a", "a", "a"], "ab"))                  # 3

    # Edge cases
    print(sol.numOfStrings(["z"], "abc"))                           # 0  not present
    print(sol.numOfStrings(["abc"], "abc"))                         # 1  exact match
    print(sol.numOfStrings(["abcd"], "abc"))                        # 0  pattern longer
