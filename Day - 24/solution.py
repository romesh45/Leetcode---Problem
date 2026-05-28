from typing import List


class Solution:
    def stringIndices(
        self, wordsContainer: List[str], wordsQuery: List[str]
    ) -> List[int]:
        # ── The big idea ──────────────────────────────────────────────────────
        # "Longest common suffix" is "longest common prefix of the reverses."
        # So we build a TRIE over reversed wordsContainer. Each trie node N
        # remembers the BEST container index whose reversed form passes
        # through N, where "best" means:
        #     (1) smallest length, then
        #     (2) earliest index on length ties.
        #
        # To answer a query: walk reversed(query) down the trie as far as the
        # characters match. The `best` stored at the deepest node reached is
        # the answer — that's the container word with the longest common
        # suffix with the query, tie-broken correctly.
        #
        # The empty-suffix fallback drops out for free: queries whose first
        # reversed char doesn't exist in the trie stay at the root, and the
        # root's `best` is computed over ALL container words (everyone shares
        # the empty suffix).

        n = len(wordsContainer)

        def better(a: int, b: int) -> int:
            """Return whichever index represents the better container word."""
            la, lb = len(wordsContainer[a]), len(wordsContainer[b])
            if la != lb:
                return a if la < lb else b
            return a if a < b else b   # earlier index wins on length ties

        # ── Build trie ────────────────────────────────────────────────────────
        # A node is a dict with two keys: "best" (int) and "children" (dict).
        # Initialize root.best to be the globally-best container index.
        root = {"best": 0, "children": {}}
        for i in range(1, n):
            root["best"] = better(root["best"], i)

        for i, w in enumerate(wordsContainer):
            node = root
            for ch in reversed(w):
                if ch not in node["children"]:
                    # New node — its initial best is just this index.
                    node["children"][ch] = {"best": i, "children": {}}
                node = node["children"][ch]
                # Even if the node already existed, update its best with i.
                node["best"] = better(node["best"], i)

        # ── Answer queries ────────────────────────────────────────────────────
        ans = []
        for q in wordsQuery:
            node = root
            for ch in reversed(q):
                if ch in node["children"]:
                    node = node["children"][ch]
                else:
                    break               # no further suffix match; stop here
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
