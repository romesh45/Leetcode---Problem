class Solution:
    def smallestPalindrome(self, s: str) -> str:
        freq = Counter(s)

        # Build the sorted left half from floor(count/2) of each character.
        # At most one character has an odd count (guaranteed by input being palindromic).
        half = []
        mid = ""
        for ch in sorted(freq):
            half.append(ch * (freq[ch] // 2))
            if freq[ch] % 2 == 1:
                mid = ch

        left = "".join(half)
        return left + mid + left[::-1]


# Quick tests
if __name__ == "__main__":
    sol = Solution()

    print(sol.smallestPalindrome("z"))        # "z"
    print(sol.smallestPalindrome("babab"))    # "abbba"
    print(sol.smallestPalindrome("daccad"))   # "acddca"
    print(sol.smallestPalindrome("aa"))       # "aa"
    print(sol.smallestPalindrome("aabbaa"))   # "aabbaa"
