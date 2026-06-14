class Solution:
    def mapWordWeights(self, words: List[str], weights: List[int]) -> str:
        result = []
        for word in words:
            total = sum(weights[ord(c) - 97] for c in word)   
            r = total % 26
            result.append(chr(122 - r))                        
        return "".join(result)


# ── Quick tests ───────────────────────────
if __name__ == "__main__":
    sol = Solution()

    w1 = [5, 3, 12, 14, 1, 2, 3, 2, 10, 6, 6, 9, 7, 8, 7, 10, 8, 9, 6, 9, 9, 8, 3, 7, 7, 2]
    print(sol.mapWordWeights(["abcd", "def", "xyz"], w1))       # "rij"

    w2 = [1] * 26
    print(sol.mapWordWeights(["a", "b", "c"], w2))              # "yyy"

    w3 = [7, 5, 3, 4, 3, 5, 4, 9, 4, 2, 2, 7, 10, 2, 5, 10, 6, 1, 2, 2, 4, 1, 3, 4, 4, 5]
    print(sol.mapWordWeights(["abcd"], w3))                     # "g"

    # Edge: weight multiple of 26 → r = 0 → 'z'.
    print(sol.mapWordWeights(["a"], [26] + [1] * 25))           # "z"

    # Edge: r = 25 → 'a'. Need weight % 26 == 25, e.g. weight 25 from one letter.
    print(sol.mapWordWeights(["a"], [25] + [1] * 25))           # "a"
