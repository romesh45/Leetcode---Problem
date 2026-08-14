from collections import defaultdict


class Solution:
    def maximumLengthSubstring(self, s: str) -> int:
        # Same sliding window as problem 2958 with k fixed at 2
        freq = defaultdict(int)
        left = ans = 0
        for right, c in enumerate(s):
            freq[c] += 1
            while freq[c] > 2:
                freq[s[left]] -= 1
                left += 1
            ans = max(ans, right - left + 1)
        return ans


# Quick tests
if __name__ == "__main__":
    sol = Solution()

    print(sol.maximumLengthSubstring("bcbbbcba"))   # 4
    print(sol.maximumLengthSubstring("aaaa"))        # 2
    print(sol.maximumLengthSubstring("abcdef"))      # 6  all distinct
    print(sol.maximumLengthSubstring("aabbcc"))      # 6
