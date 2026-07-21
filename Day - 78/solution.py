class Solution:
    def maxActiveSectionsAfterTrade(self, s: str) -> int:
        # The trade picks a '1' run in s (surrounded by '0's) and converts it
        # to '0', merging it with the adjacent '0' runs. The merged '0' block
        # is then converted to '1's. Net gain = left_0_run + right_0_run.
        #
        # In augmented t = '1' + s + '1', the '1' run at index k in s is a
        # valid trade target iff it is INTERIOR to the runs list of s
        # (not at position 0 or the last position), i.e. it has a '0' run on
        # both sides. The augmented '1's at the edges do NOT act as '0' borders.
        #
        # Strategy: parse s into runs, find the interior '1' run maximising
        # left_0 + right_0, add that to the base count of '1's.

        base = s.count('1')
        n = len(s)

        # Parse s into (char, length) runs
        runs = []
        i = 0
        while i < n:
            j = i
            while j < n and s[j] == s[i]:
                j += 1
            runs.append((s[i], j - i))
            i = j

        # Check interior '1' runs (index 1 .. len(runs)-2)
        max_gain = 0
        for k in range(1, len(runs) - 1):
            if runs[k][0] == '1':
                gain = runs[k - 1][1] + runs[k + 1][1]
                if gain > max_gain:
                    max_gain = gain

        return base + max_gain


# Quick tests
if __name__ == "__main__":
    sol = Solution()

    print(sol.maxActiveSectionsAfterTrade("01"))       # 1
    print(sol.maxActiveSectionsAfterTrade("0100"))     # 4
    print(sol.maxActiveSectionsAfterTrade("1000100"))  # 7
    print(sol.maxActiveSectionsAfterTrade("01010"))    # 4

    # Edge cases
    print(sol.maxActiveSectionsAfterTrade("111"))      # 3  no 0-bordered 1-block
    print(sol.maxActiveSectionsAfterTrade("000"))      # 0  no 1-block at all
    print(sol.maxActiveSectionsAfterTrade("010"))      # 3  gain = 1+1 = 2, base = 1
    print(sol.maxActiveSectionsAfterTrade("0110"))     # 4  gain = 1+1 = 2, base = 2
