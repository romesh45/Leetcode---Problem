from typing import List


class Solution:
    def longestCommonPrefix(self, arr1: List[int], arr2: List[int]) -> int:
        # ── Build phase ──────────────────────────────────────────────────────
        # Insert EVERY prefix of EVERY number in arr1 into a hash set.
        # Repeated integer division by 10 strips the last digit, so the
        # sequence num, num//10, num//100, ... is exactly all prefixes of num.
        #   e.g. 100 → {100, 10, 1}
        prefixes = set()
        for num in arr1:
            while num:
                prefixes.add(num)
                num //= 10

        # ── Query phase ──────────────────────────────────────────────────────
        # For each number in arr2, strip digits from the right (// 10),
        # i.e. test its prefixes from LONGEST to SHORTEST. The first prefix
        # found in the set is this number's longest common prefix with some
        # element of arr1 — record its digit length and stop.
        best = 0
        for num in arr2:
            while num:
                if num in prefixes:
                    best = max(best, len(str(num)))
                    break               # longest checked first → no need to continue
                num //= 10

        return best


# ── Quick tests ──────────────────────────────────────────────────────────────
if __name__ == "__main__":
    sol = Solution()
    print(sol.longestCommonPrefix([1, 10, 100], [1000]))          # 3
    print(sol.longestCommonPrefix([1, 2, 3], [4, 4, 4]))          # 0
    print(sol.longestCommonPrefix([1], [1]))                      # 1
    print(sol.longestCommonPrefix([12345], [12399]))              # 3  (prefix 123)
    print(sol.longestCommonPrefix([100000000], [100000000]))      # 9
    print(sol.longestCommonPrefix([5655359], [56554]))            # 4  (prefix 5655)
    print(sol.longestCommonPrefix([1223], [43456]))               # 0
