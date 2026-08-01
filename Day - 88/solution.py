from collections import Counter


class Solution:
    def minimumPushes(self, word: str) -> int:
        # Sort letter frequencies descending so the most-used letters get
        # the cheapest slots (1 push each on the 8 available keys).
        freq = sorted(Counter(word).values(), reverse=True)
        return sum(count * (i // 8 + 1) for i, count in enumerate(freq))


# Quick tests
if __name__ == "__main__":
    sol = Solution()

    print(sol.minimumPushes("abcde"))                     # 5
    print(sol.minimumPushes("xyzxyzxyzxyz"))              # 12
    print(sol.minimumPushes("aabbccddeeffgghhiiiiii"))    # 24
    print(sol.minimumPushes("a"))                         # 1
