from typing import List


class Solution:
    def sequentialDigits(self, low: int, high: int) -> List[int]:
        # Every sequential-digit number is a contiguous substring of "123456789".
        # Generate all such substrings (lengths 2–9), keep those in [low, high].
        # Iterating length-first, then left-to-right within each length, gives a
        # naturally sorted result — no explicit sort needed.
        source = "123456789"
        result = []
        for length in range(2, 10):                    # 2-digit … 9-digit
            for start in range(9 - length + 1):        # valid start positions
                num = int(source[start : start + length])
                if low <= num <= high:
                    result.append(num)
        return result


# ── Quick tests ───────────────────────────────────────────────────────────────
if __name__ == "__main__":
    sol = Solution()

    print(sol.sequentialDigits(100, 300))          # [123, 234]
    print(sol.sequentialDigits(1000, 13000))        # [1234,2345,3456,4567,5678,6789,12345]

    # Edge cases
    print(sol.sequentialDigits(10, 89))             # [12,23,34,45,56,67,78,89]  all 2-digit
    print(sol.sequentialDigits(58, 155))            # [67,78,89,123]
    print(sol.sequentialDigits(100000000, 10**9))   # [123456789]
    print(sol.sequentialDigits(10, 10))             # []  low==high, no sequential
