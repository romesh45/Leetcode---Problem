from math import comb


class Solution:
    def smallestPalindrome(self, s: str, k: int) -> str:
        n = len(s)
        half = n // 2
        freq = [0] * 26
        for i in range(half):
            freq[ord(s[i]) - ord('a')] += 1

        def perm(rem):
            # Multinomial coefficient of the current freq with `rem` slots.
            # Returns early (capped) once the count exceeds k.
            acc = 1
            for ci in range(26):
                f = freq[ci]
                if not f:
                    continue
                if f > rem:
                    return 0          # more of this char than slots -- invalid
                acc *= comb(rem, f)
                if acc > k:
                    return acc        # only need to know it's > k
                rem -= f
            return acc

        left = []
        start = 0                     # cumulative count of skipped permutations

        for i in range(half):
            selected = False
            for ci in range(26):
                if not freq[ci]:
                    continue
                freq[ci] -= 1         # tentatively place this character

                p = perm(half - i - 1)

                if start + p >= k:    # k-th perm falls in this group
                    left.append(chr(ci + ord('a')))
                    selected = True
                    break

                freq[ci] += 1         # restore and skip this group
                start += p

            if not selected:
                return ""

        h1 = "".join(left)
        mid = s[n // 2] if n % 2 == 1 else ''
        h2 = "".join(left[::-1])
        return h1 + mid + h2


# Quick tests
if __name__ == "__main__":
    sol = Solution()

    print(sol.smallestPalindrome("abba", 2))     # "baab"
    print(sol.smallestPalindrome("aa", 2))        # ""
    print(sol.smallestPalindrome("bacab", 1))     # "abcba"
    print(sol.smallestPalindrome("aabbaa", 3))    # "baaaab"
    print(sol.smallestPalindrome("a", 1))         # "a"
    print(sol.smallestPalindrome("aabbaa", 4))    # ""
