class Solution:
    def longestCommonPrefix(self, arr1: List[int], arr2: List[int]) -> int:
        prefixes = set()
        for num in arr1:
            while num:
                prefixes.add(num)
                num //= 10
        best = 0
        for num in arr2:
            while num:
                if num in prefixes:
                    best = max(best, len(str(num)))
                    break              
                num //= 10

        return best


# ── Quick tests ──────────
if __name__ == "__main__":
    sol = Solution()
    print(sol.longestCommonPrefix([1, 10, 100], [1000]))          # 3
    print(sol.longestCommonPrefix([1, 2, 3], [4, 4, 4]))          # 0
    print(sol.longestCommonPrefix([1], [1]))                      # 1
    print(sol.longestCommonPrefix([12345], [12399]))              # 3  (prefix 123)
    print(sol.longestCommonPrefix([100000000], [100000000]))      # 9
    print(sol.longestCommonPrefix([5655359], [56554]))            # 4  (prefix 5655)
    print(sol.longestCommonPrefix([1223], [43456]))               # 0
