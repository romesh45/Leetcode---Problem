class Solution:
    def smallestSubsequence(self, s: str) -> str:
        # Greedy monotonic-stack approach:
        # For each character c, pop larger characters off the top of the stack
        # only if they appear again later (so we won't lose them permanently).
        # Skip c if it's already in the stack (we already have the best position for it).

        last = {c: i for i, c in enumerate(s)}  # last index each char appears
        stack = []
        in_stack = set()

        for i, c in enumerate(s):
            if c in in_stack:
                continue
            # Pop characters that are lexicographically larger and can still be
            # added later (their last occurrence is beyond the current index).
            while stack and stack[-1] > c and last[stack[-1]] > i:
                in_stack.discard(stack.pop())
            stack.append(c)
            in_stack.add(c)

        return ''.join(stack)


# Quick tests
if __name__ == "__main__":
    sol = Solution()

    print(sol.smallestSubsequence("bcabc"))      # "abc"
    print(sol.smallestSubsequence("cbacdcbc"))   # "acdb"

    # Edge cases
    print(sol.smallestSubsequence("a"))          # "a"   single char
    print(sol.smallestSubsequence("abcd"))       # "abcd" already distinct and sorted
    print(sol.smallestSubsequence("dcba"))       # "dcba" distinct, reverse sorted -- all must stay
    print(sol.smallestSubsequence("aabbcc"))     # "abc"
    print(sol.smallestSubsequence("bbcaac"))     # "bac" -- verify manually
