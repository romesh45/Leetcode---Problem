class Solution:
    def processStr(self, s: str) -> str:
        # Direct left-to-right simulation. The four ops map straight to list ops:
        #   lowercase → append
        #   '*'       → pop last char (only if buffer non-empty: the "if exists" rule)
        #   '#'       → duplicate (append a copy of the buffer to itself)
        #   '%'       → reverse in place
        # A list (not a string) keeps append/pop/reverse cheap and mutable.
        # With |s| ≤ 20 the result stays small even after a few '#' doublings.
        result = []

        for ch in s:
            if ch == '*':
                if result:
                    result.pop()
            elif ch == '#':
                result += result            # duplicate
            elif ch == '%':
                result.reverse()
            else:
                result.append(ch)

        return "".join(result)


# ── Quick tests ──────────────────────────────────────────────────────────────
if __name__ == "__main__":
    sol = Solution()
    print(repr(sol.processStr("a#b%*")))     # 'ba'
    print(repr(sol.processStr("z*#")))       # ''
    print(repr(sol.processStr("*")))         # ''   (remove from empty → no-op)
    print(repr(sol.processStr("abc")))       # 'abc'
    print(repr(sol.processStr("ab#")))       # 'abab'
    print(repr(sol.processStr("abc%")))      # 'cba'
    print(repr(sol.processStr("a#%*")))      # 'a'  (a → aa → aa(rev) → a)
    print(repr(sol.processStr("ab*c")))      # 'ac'
