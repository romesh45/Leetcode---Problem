class Solution:
    def numberOfSubstrings(self, s: str) -> int:
        # Track the most recent index at which each of 'a', 'b', 'c' was seen.
        # For a fixed right endpoint `i`, every substring that starts at or
        # before min(last_a, last_b, last_c) and ends at `i` is guaranteed to
        # contain all three characters. So the count of valid substrings
        # ending exactly at `i` is (min(last_a, last_b, last_c) + 1).
        # Summing this over every `i` gives the total in one O(n) pass.
        last = {'a': -1, 'b': -1, 'c': -1}
        count = 0

        for i, ch in enumerate(s):
            last[ch] = i
            count += min(last['a'], last['b'], last['c']) + 1

        return count


# ── Quick tests ───────────────────────────────────────────────────────────────
if __name__ == "__main__":
    sol = Solution()

    print(sol.numberOfSubstrings("abcabc"))   # 10
    print(sol.numberOfSubstrings("aaacb"))    # 3
    print(sol.numberOfSubstrings("abc"))      # 1

    # Edge cases
    print(sol.numberOfSubstrings("aaa"))      # 0  never all three present
    print(sol.numberOfSubstrings("cba"))      # 1  reverse order still works
    print(sol.numberOfSubstrings("abcabcabc")) # 28 longer repeating pattern
