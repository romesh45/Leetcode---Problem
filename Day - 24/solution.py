class Solution:
    def stringIndices(
        self, wordsContainer: List[str], wordsQuery: List[str]
    ) -> List[int]:
        n = len(wordsContainer)
        def better(a: int, b: int) -> int:
            la, lb = len(wordsContainer[a]), len(wordsContainer[b])
            if la != lb:
                return a if la < lb else b
            return a if a < b else b
        root = {"best": 0, "children": {}}
        for i in range(1, n):
            root["best"] = better(root["best"], i)
        for i, w in enumerate(wordsContainer):
            node = root
            for ch in reversed(w):
                if ch not in node["children"]:
                    node["children"][ch] = {"best": i, "children": {}}
                node = node["children"][ch]
                node["best"] = better(node["best"], i)
        ans = []
        for q in wordsQuery:
            node = root
            for ch in reversed(q):
                if ch in node["children"]:
                    node = node["children"][ch]
                else:
                    break               
            ans.append(node["best"])
        return ans


# ── Quick tests ──────────────────────────────────────────────────────────────
if __name__ == "__main__":
    sol = Solution()
    print(sol.stringIndices(
        ["abcd", "bcd", "xbcd"],
        ["cd", "bcd", "xyz"]
    ))   # [1, 1, 1]

    print(sol.stringIndices(
        ["abcdefgh", "poiuygh", "ghghgh"],
        ["gh", "acbfgh", "acbfegh"]
    ))   # [2, 0, 2]

    # Edge: single word in container
    print(sol.stringIndices(["abc"], ["xyz", "bc", "abc"]))         # [0, 0, 0]

    # Edge: empty common suffix everywhere
    print(sol.stringIndices(["aaaa", "bb", "c"], ["xyz"]))          # [2]
    # ("c" is shortest; everyone shares empty suffix)

    # Edge: identical container words
    print(sol.stringIndices(["abc", "abc"], ["abc"]))               # [0]
