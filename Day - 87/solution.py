class Solution:
    def minimumPushes(self, word: str) -> int:
        # All letters are distinct, so we optimally assign them to 8 keys (2-9).
        # The i-th letter (0-indexed) costs (i // 8) + 1 pushes:
        #   letters 0-7  -> 1 push each (first slot on each of 8 keys)
        #   letters 8-15 -> 2 pushes each (second slot on each key)
        #   letters 16-23 -> 3 pushes each
        #   letters 24-25 -> 4 pushes each
        return sum(i // 8 + 1 for i in range(len(word)))


# Quick tests
if __name__ == "__main__":
    sol = Solution()

    print(sol.minimumPushes("abcde"))       # 5
    print(sol.minimumPushes("xycdefghij"))  # 12
    print(sol.minimumPushes("a"))           # 1
    print(sol.minimumPushes("abcdefghijklmnopqrstuvwxyz"))  # 1*8+2*8+3*8+4*2 = 8+16+24+8 = 56
