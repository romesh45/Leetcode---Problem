# 13. Roman to Integer
# https://leetcode.com/problems/roman-to-integer/
# Difficulty: Easy | Time: O(n) | Space: O(1)

class Solution:
    def romanToInt(self, s: str) -> int:
        values = {
            'I': 1,   'V': 5,
            'X': 10,  'L': 50,
            'C': 100, 'D': 500,
            'M': 1000
        }

        result = 0

        for i in range(len(s)):
            curr = values[s[i]]
            next_val = values[s[i + 1]] if i + 1 < len(s) else 0

            # If current value is less than next → subtraction case (IV, IX, XL, XC, CD, CM)
            if curr < next_val:
                result -= curr
            else:
                result += curr

        return result


# ── Alternative: right-to-left scan (no index peek needed) ──────────────────

class SolutionRTL:
    def romanToInt(self, s: str) -> int:
        values = {
            'I': 1,   'V': 5,
            'X': 10,  'L': 50,
            'C': 100, 'D': 500,
            'M': 1000
        }

        result = 0
        prev = 0

        for ch in reversed(s):
            curr = values[ch]
            # If smaller than what came after it → subtract
            result += -curr if curr < prev else curr
            prev = curr

        return result


# ── Tests ────────────────────────────────────────────────────────────────────

if __name__ == "__main__":
    sol = Solution()

    test_cases = [
        ("III",     3),
        ("LVIII",   58),
        ("MCMXCIV", 1994),
        ("IV",      4),
        ("IX",      9),
        ("XL",      40),
        ("XC",      90),
        ("CD",      400),
        ("CM",      900),
        ("MMMCMXCIX", 3999),
    ]

    all_pass = True
    for roman, expected in test_cases:
        result = sol.romanToInt(roman)
        status = "PASS" if result == expected else "FAIL"
        if status == "FAIL":
            all_pass = False
        print(f"[{status}] {roman:>12} → {result:>4}  (expected {expected})")

    print("\nAll tests passed ✓" if all_pass else "\nSome tests failed ✗")
